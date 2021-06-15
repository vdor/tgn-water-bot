# f-water-tgn

This is a telegram bot. It notifies about water issues in Taganrog

## Production

Telegram bot -  [@TgnWaterBot](https://t.me/TgnWaterBot)

Telegram [channel](https://t.me/tgnwater) with the bot

## Usage

Send `/start` message to the bot, use it as administrator in your channel or add to a group

## Source code usage

- create venv `virtual venv -p $(which python3.9)`
- activate venv `source venv/bin/activate`

### Display issues to the console

`python3 display_issues.py`

### Run bot

- create `.env` based on `.env.example`
- fill in `.env`
- `python3 worker.py`

## TODO

- Create `manage.py` helper
