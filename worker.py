import asyncio

import firebase_admin
from firebase_admin import db
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from src.env import TELEGRAM_BOT_TOKEN, FIREBASE_ADMIN_CERT, FIREBASE_DB_URI, URI_WATER_ISSUES_SOURCE_HTML
from src.bots.tg import TelegramBot
from src.issue_sender.telegram import IssueSenderTelegram
from src.issues_collector import IssuesCollector
from src.issues_html_repository.http import IssuesHTMLRepositoryHTTP
from src.issues_parser.html import IssuesParserHTML
from src.issues_repository.firebase import IssuesRepositoryFirebase
from src.telegram_chat_ids_repository.firebase import TelegramChatIdsRepositoryFirebase

if __name__ == "__main__":
    cred = firebase_admin.credentials.Certificate(FIREBASE_ADMIN_CERT)
    firebase_admin.initialize_app(cred, {
        'databaseURL': FIREBASE_DB_URI,
    })
    firebase_root_ref = db.reference('/')

    chats_repo = TelegramChatIdsRepositoryFirebase(reference=firebase_root_ref)
    issues_repo = IssuesRepositoryFirebase(reference=firebase_root_ref)
    issues_html_repo = IssuesHTMLRepositoryHTTP(uri=URI_WATER_ISSUES_SOURCE_HTML)
    issues_html_parser = IssuesParserHTML(repo=issues_html_repo)

    issues_collector = IssuesCollector(parser=issues_html_parser, repo=issues_repo)
    issue_sender = IssueSenderTelegram(bot_token=TELEGRAM_BOT_TOKEN, chats_repo=chats_repo, issue_repo=issues_repo)
    tg_bot = TelegramBot(token=TELEGRAM_BOT_TOKEN, chats_repo=chats_repo)

    loop = asyncio.get_event_loop()
    scheduler = AsyncIOScheduler({'event_loop': loop})

    scheduler.add_job(issues_collector.collect, 'interval', minutes=.1)
    scheduler.add_job(issue_sender.send, 'interval', minutes=.2)
    scheduler.start()

    try:
        loop.run_until_complete(tg_bot.start())
    except (KeyboardInterrupt, SystemExit):
        pass
