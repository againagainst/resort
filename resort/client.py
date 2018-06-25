import urllib.parse
from typing import Type

import requests

from etalons import BaseEtalon, BasicHTTPResponseEtalon
from server_spec import ServerSpecReader
from errors import ConnectionError


class BasicClient(object):
    """Establishes connection to the url from the server_spec
    It can make snapshots of entries that described in the spec.

    Args:
        server_spec (ServerSpecReader)
    """

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
        for method, each_entry in self.server_spec.paths_and_methods():
            yield self.snapshot(each_entry, method)

    def snapshot(self, entry: str, method: str,
                 Etalon: Type[BaseEtalon]=BasicHTTPResponseEtalon):
        """Makes etalon, a "snapshot" of response from the server
        to request on the :entry: with the HTTP :method:

        Args:
          entry: str: part of the url that describes an API entry
          method: str: HTTP method: GET - supported, TODO: POST, PUT...
          Etalon: Constructor (Default is BasicHTTPResponseEtalon)

        Returns:

        """
        url = urllib.parse.urljoin(self.server_spec.url, entry)
        try:
            response = requests.request(method, url)
        except requests.exceptions.ConnectionError:
            raise ConnectionError(url)
        return Etalon(entry=entry, response=response, name=self.server_spec.test_name)
