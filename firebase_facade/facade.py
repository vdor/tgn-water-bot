import json
import logging
from typing import Optional

import firebase_admin
from firebase_admin import App, db
from firebase_admin.db import Reference

from firebase_facade.base import FirebaseFacadeABC

logger = logging.getLogger(__name__)


class FirebaseFacade(FirebaseFacadeABC):
    _firebase_admin_secret_json_content: str
    _firebase_db_uri: str
    _app: Optional[App]

    def __init__(self, firebase_db_uri: str, firebase_admin_secret_json_content: str):
        self._app = None
        self._firebase_db_uri = firebase_db_uri
        self._firebase_admin_secret_json_content = firebase_admin_secret_json_content

    def get_issues_ref(self) -> Reference:
        return self._get_root_ref().child("issues")

    def get_telegram_ref(self) -> Reference:
        return self._get_root_ref().child("telegram")

    def get_telegram_chat_ids_ref(self) -> Reference:
        return self.get_telegram_ref().child("active_chat_ids")

    def _get_root_ref(self) -> Reference:
        return db.reference("/", app=self._firebase_app)

    @property
    def _firebase_app(self) -> App:
        if self._app is not None:
            return self._app

        logger.info("initializing firebase app")
        cred = firebase_admin.credentials.Certificate(
            json.loads(self._firebase_admin_secret_json_content)
        )
        self._app = firebase_admin.initialize_app(
            cred,
            {
                "databaseURL": self._firebase_db_uri,
            },
        )
        return self._app
