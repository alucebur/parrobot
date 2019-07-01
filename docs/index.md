# Parro(Bo)t

This is a bot for Telegram which stores every message that users sent it and let them manage them. It is intended as a CRUD of small notes of text.

- [Libraries used](#libraries-used)
- [Requirements](#requirements)
- [List of commands](#commands)
- [License](#license)

---

### Libraries used
- sqlite3
- requests
- urllib
- json
- logging
- time

Python 3.6+ is also required.
This library uses the logging module to send info to standard output. By default the log level is set to DEBUG. You can change it to INFO editing this line as follow:
```python
    logging.basicConfig(format=format, level=logging.INFO)
```

---

### Requirements
- Create a bot account in Telegram:
    - Search `@BotFather` in Telegram and start a conversation with it. It will display a list of commands.
    - Write or press `/newbot`, choose a name for your bot, and then choose an unused username, which must end with "bot" (e.g. rubeculabot).
    - Take note of the authorization token that BotFather gives you, you will use it to access the Telegram API.

- Create a file named `config.py`. Inside it, define the following constants:
    - TOKEN = `"123456789:XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"` # Telegram authorization token (keep it secret!)
    - DB_NAME = `"notes.sqlite3"` # SQLite database file where notes will be stored
    - BASE_URL = `f"https://api.telegram.org/bot{TOKEN}/"` # API URL

More info in [Telegram](https://core.telegram.org/bots#3-how-do-i-create-a-bot)

---

### Commands
- `/start` - Let the bot to send you messages
- `/help` - A list of these commands
- `/delete` - Opens a keyboard that let us select the note to delete.

---

### License
This project is Unlicensed. Feel free to use it and modify it as you wish. Enjoy!