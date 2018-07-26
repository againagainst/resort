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
        res = list(dictdiffer.diff(etalon_d, snap_d, ignore=self.ignored))

        return {
            'changes': len(res),
            'difftext': BaseComparator.human_readable(res)
        }

    @staticmethod
    def human_readable(dictdiffer_result: list):
        """TODO [summary]

        Args:
            dictdiffer_result (list): [description]

        Returns:
            [type]: [description]
        """

        if not dictdiffer_result:
            return "Nothing changed."
        return '\n'.join(
            '{0} "{1}": "{2[0]}" -> "{2[1]}"'.format(*d) for d in dictdiffer_result
        )

    @staticmethod
    def bin_result(diff_map: dict) -> bool:
        """TODO: [summary]

        Args:
            diff_map (dict): [description]

        Returns:
            bool: [description]
        """
        return diff_map.get('changes', 1) == 0
