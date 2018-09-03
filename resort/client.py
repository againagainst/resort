import urllib.parse
import contextlib
from typing import Type

import requests

from . import errors
from .etalons import BaseEtalon, BasicHTTPResponseEtalon
from .server_spec import ServerSpecReader


class BasicClient(object):
    """Establishes connection to the url from the server_spec
    It can make snapshots of entries that described in the spec.

    Args:
        server_spec (ServerSpecReader)
    """
    Etalon = BasicHTTPResponseEtalon

    def __init__(self, server_spec: ServerSpecReader):
        self.server_spec = server_spec

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
            with self.make_session() as session:
                response = session.request(method=method, url=url, **params)
        except requests.exceptions.ConnectionError:
            raise errors.ConnectionError(url)
        except TypeError as err:
            raise errors.SpecFormatError(fname=name, err=err)
        return self.Etalon(entry=uri, name=name, response=response)

    @contextlib.contextmanager
    def make_session(self):
        if self.server_spec.session_type == 'post-request':
            session = requests.Session()
            uri, params = self.server_spec.session['create']
            url = urllib.parse.urljoin(self.server_spec.host, uri)
            method = self.pop_method(params)
            session.request(method=method, url=url, **params)
        else:
            session = requests

        yield session

        if self.server_spec.session_type == 'post-request':
            uri, params = self.server_spec.session['delete']
            url = urllib.parse.urljoin(self.server_spec.host, uri)
            method = self.pop_method(params)
            session.request(method=method, url=url, **params)
            session.close()

    @classmethod
    def pop_method(cls, params: dict):
        return params.pop('method', 'GET')
