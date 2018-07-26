import dictdiffer

from .base import BaseEtalon


class BaseComparator(object):

    def __init__(self, ignored: set=None):
        self.ignored = ignored

    def check(self, etalon: BaseEtalon, snapshot: BaseEtalon):
        """TODO: [summary]
        
        Args:
            etalon (BaseEtalon): [description]
            snapshot (BaseEtalon): [description]
        
        Returns:
            [type]: [description]
        """

        etalon_d = etalon.dump()
        snap_d = snapshot.dump()
        res = dictdiffer.diff(etalon_d, snap_d, ignore=self.ignored)
        bin_res = res is None  # none diff is good (True)
        return BaseComparator.human_readable(list(res)), bin_res

    @staticmethod
    def human_readable(diff_result: list):
        if not diff_result:
            return "Nothing changed."
        return '\n'.join(
            '{0} "{1}": "{2[0]}" -> "{2[1]}"'.format(*d) for d in diff_result
        )
