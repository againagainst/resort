import dictdiffer

from etalons.base import BaseEtalon


class BaseComparator(object):

    def __init__(self, ignored: set=None):
        self.ignored = ignored

    def check(self, etalon: BaseEtalon, snapshot: BaseEtalon):
        etalon_d = etalon.dump()
        snap_d = snapshot.dump()
        res = dictdiffer.diff(etalon_d, snap_d, ignore=self.ignored)
        return BaseComparator.human_readable(list(res))

    @staticmethod
    def human_readable(diff_result: list):
        if not diff_result:
            return "Nothing changed."
        return '\n'.join(
            '{0} "{1}": "{2[0]}" -> "{2[1]}"'.format(*d) for d in diff_result
        )
