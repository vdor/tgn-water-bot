import logging
from typing import List

from firebase_admin.db import Reference

from src.domain.water_issue import WaterIssue
from src.issues_repository.base import IssuesRepositoryABC

logger = logging.getLogger(__name__)


class IssuesRepositoryFirebase(IssuesRepositoryABC):
    _reference: Reference

    def __init__(self, reference: Reference):
        self._reference = reference

    @property
    def _issues_ref(self):
        return self._reference.child("issues")

    async def get_unsent_tg_issues(self) -> List[WaterIssue]:
        issues = (
            self._issues_ref.order_by_child("is_sent_telegram").equal_to(False).get()
        )

        result = []

        if hasattr(issues, "values"):
            for issue in issues.values():  # noqa
                result.append(WaterIssue.create_from_dict(issue))

        return result

    async def mark_as_sent_tg_by_hashes(self, issue_hashes: List[str]):
        payload = {}

        for h in issue_hashes:
            payload[f"{h}/is_sent_telegram"] = True

        if payload:
            self._issues_ref.update(payload)

    async def try_add_issues(self, issues: List[WaterIssue]):
        for issue in issues:
            issue_ref = self._issues_ref.child(issue.hash)
            if issue_ref.get() is None:
                logger.info('adding new issue with hash "{%s}"', issue.hash)
                issue_ref.set(issue.asdict)
