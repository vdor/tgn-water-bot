import environ

env = environ.Env()
env.read_env("./.env")

TELEGRAM_BOT_TOKEN = env.str("TELEGRAM_BOT_TOKEN")
URI_WATER_ISSUES_SOURCE_HTML = env.str(
    "URI_WATER_ISSUES_SOURCE_HTML", "http://www.tgnvoda.ru/avarii.php"
)

FIREBASE_ADMIN_SECRET_JSON_CONTENT = env.str("FIREBASE_ADMIN_SECRET_JSON_CONTENT")
FIREBASE_DB_URI = env.str("FIREBASE_DB_URI")

LOG_LEVEL = env.str("LOG_LEVEL", "INFO")
