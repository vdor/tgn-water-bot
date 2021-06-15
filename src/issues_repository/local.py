import itertools
import json
from collections.abc import Iterable as IterableABC
from typing import Iterable, List

from ..domain.water_issue import WaterIssue
from ..packages.json_encoders import DataClassJSONEncoder
from .base import IssuesRepositoryABC


class IssuesRepositoryLocal(IssuesRepositoryABC):
    _file_path: str

    def __init__(self, file_path: str):
        self._file_path = file_path

    async def get_unsent_tg_issues(self) -> List[WaterIssue]:
        result = []

        for issue in self._get_stored_issues():
            if not issue.is_sent_telegram:
                result.append(issue)

        return result

    async def mark_as_sent_tg_by_hashes(self, issue_hashes: List[str]):
        stored_issues_map = self._get_hash_map_issues()

        for hash_ in issue_hashes:
            issue = stored_issues_map.get(hash_)

            if issue is not None:
                issue.is_sent_telegram = True

        self._set_issues(stored_issues_map.values())

    async def try_add_issues(self, issues: List[WaterIssue]):
        stored_issues_map = self._get_hash_map_issues()
        issues_to_add = filter(
            lambda issue: issue.hash not in stored_issues_map, issues
        )
        self._set_issues(itertools.chain(stored_issues_map.values(), issues_to_add))

    def _get_hash_map_issues(self):
        hash_map = dict()

        for issue in self._get_stored_issues():
            hash_map[issue.hash] = issue

        return hash_map

    def _get_stored_issues(self) -> Iterable[WaterIssue]:
        with open(self._file_path, "r") as f:
            content = "\n".join(f.readlines())
            try:
                issues_json = json.loads(content)
                if isinstance(issues_json, IterableABC):
                    for i_json in issues_json:
                        yield WaterIssue.create_from_dict(i_json)
            except json.JSONDecodeError as e:
                pass

    def _set_issues(self, issues: Iterable[WaterIssue]):
        with open(self._file_path, "w") as f:
            issues_list = list(issues)
            f.write(json.dumps(issues_list, cls=DataClassJSONEncoder))
