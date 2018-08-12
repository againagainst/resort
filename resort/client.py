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
        for entryid, method, each_entry, payload in self.server_spec.paths():
            yield self.snapshot(entry=each_entry,
                                method=method,
                                name=self.server_spec.make_name(entryid),
                                requests_kw=dict(json=payload))

    def snapshot(self, entry: str, method: str, name: str,
                 requests_kw=None,
                 Etalon: Type[BaseEtalon]=BasicHTTPResponseEtalon):
        """Makes etalon, a "snapshot" of response from the server
        to request on the :entry: with the HTTP :method:

        Args:
          entry: str: part of the url that describes an API entry
          method: str: HTTP method: GET, POST, PUT...
          Etalon: Constructor (Default is BasicHTTPResponseEtalon)

        Returns:

        """
        url = urllib.parse.urljoin(self.server_spec.url, entry)
        try:
            response = self.session.request(method=method, url=url, **requests_kw)
        except requests.exceptions.ConnectionError:
            raise ConnectionError(url)
        return Etalon(entry=entry, name=name, response=response)

    def make_session(self, session_desc):
        session_type = session_desc.get('type', None)
        if session_type == 'post-request':
            session = requests.Session()
            resource, method, payload = session_desc['create']
            url = urllib.parse.urljoin(self.server_spec.url, resource)
            session.request(method=method, url=url, json=payload)
        else:
            session = requests
        return session, session_type

    def disconnect(self):
        if self.session_type == 'post-request':
            self.session.close()
