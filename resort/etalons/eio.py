import json
import copy

import daiquiri

from .base import BaseEtalon
from ..project import ResortProject
from ..errors import EtalonPathError

LOG = daiquiri.getLogger(__name__)


class EtalonIO:
    """File system layer. Reads/writes etalons.

    Args:
        project (ResortProject): a project instance
        make_dir [bool, False]: If True, resort won't complain
        about missing directories, but try to create them.

    Raises:
        NotADirectoryError: if :project_dir: is a file
    """

    def __init__(self, project: ResortProject, make_dir=False):
        self.project = project
        self.project_dir = self.project.resolve_project_dir(make_dir=make_dir)

    def save(self, etalon: BaseEtalon):
        """Writes :etalon: to the file

        Args:
          etalon: BaseEtalon
        """
        etadir = self.project.etalons_dir
        etapath = etadir.joinpath(etalon.file_name)

        etadir.mkdir(parents=True, exist_ok=True)
        with etapath.open(mode='w') as f:
            LOG.info("Writing to {0}".format(etapath))
            json.dump(etalon.dump(), f, indent=2)

    def restore(self, snapshot: BaseEtalon):
        """Makes a copy of the given snapshot, then
        restores it's data from the etalon file.

        Args:
            snapshot (BaseEtalon): etalon structure to restore from the disk

        Returns:
            BaseEtalon: etalon object
        """
        etalon = copy.deepcopy(snapshot)
        etapath = self.project.etalons_dir.joinpath(etalon.file_name)

        try:
            with etapath.open(mode='r') as f:
                LOG.info("Reading from {0}".format(etapath))
                etalon.restore_from_dict(json.load(f))
        except FileNotFoundError:
            raise EtalonPathError(etapath)
        return etalon
