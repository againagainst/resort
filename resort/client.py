import urllib.parse
from typing import Type

import requests

from .etalons import BaseEtalon, BasicHTTPResponseEtalon
from .server_spec import ServerSpecReader
from .errors import ConnectionError


class BasicClient(object):
    """Establishes connection to the url from the server_spec
    It can make snapshots of entries that described in the spec.

    Args:
        server_spec (ServerSpecReader)
    """
    Etalon = BasicHTTPResponseEtalon

    def __init__(self, server_spec: ServerSpecReader):
        self.server_spec = server_spec
        self.session, self.session_type = self.make_session(self.server_spec.session)

    def snapshot_etalons(self, Etalon: Type[BaseEtalon]=BasicHTTPResponseEtalon):
        """Make etalon (a "snapshot") for each entry in the spec
        which was read from the spec_file.
        see: snapshot

        Args:
          Etalon: Constructor (Default is BasicHTTPResponseEtalon)

        Returns: A generator of etalons

        """
        for entry_id, uri, params in self.server_spec.fetch_signatures():
            yield self.snapshot(uri=uri,
                                params=params,
                                name=self.server_spec.make_name(entry_id)
                                )

    def snapshot(self, uri: str, params: dict, name: str):
        """Makes etalon, a "snapshot" of response from the server
        to request on the :entry: with the HTTP :method:

        Args:
          uri: str: part of the url that describes an resource
          params: HTTP parametres method (GET, POST, PUT), body, headers
          name: str - name of the snapshot

        Returns: BasicHTTPResponseEtalon

        """
        url = urllib.parse.urljoin(self.server_spec.host, uri)
        method = self.pop_method(params)
        try:
            response = self.session.request(method=method, url=url, **params)
        except requests.exceptions.ConnectionError:
            raise ConnectionError(url)
        return self.Etalon(entry=uri, name=name, response=response)

    def make_session(self, session_desc):
        session_type = session_desc.get('type', None)
        if session_type == 'post-request':
            session = requests.Session()
            uri, params = session_desc['create']
            url = urllib.parse.urljoin(self.server_spec.host, uri)
            method = self.pop_method(params)
            session.request(method=method, url=url, **params)
        else:
            session = requests
        return session, session_type

    def disconnect(self):
        if self.session_type == 'post-request':
            self.session.close()

    @classmethod
    def pop_method(cls, params: dict):
        return params.pop('method', 'GET')
