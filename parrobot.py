# Parro(Bo)t
"""
This is a bot for Telegram which stores every message that users sent it
and let manage them. It is intended as a CRUD of small notes of text.
"""
import json
import requests
import urllib
import time
import logging

from config import DB_NAME, BASE_URL
from dbhelper import DBHelper

# Connects to the database
db = DBHelper(DB_NAME)


def get_url(url, payload):
    """
    Do a post request to the API URL and return the response as text
        @URL: API URL
        @payload: dictionary with parameters for acknowledging, long polling...
    """
    response = requests.post(url, payload)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url, payload):
    """
    Get the json response from the API URL and return it as a dict
        @URL: API URL
        @payload: dictionary with parameters for acknowledging, long polling...
    """
    content = get_url(url, payload)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    """
    Build payload parameters and send the update request,
    returning the response as a dict
        @offset: Expected update_id (parameter for acknowledging)
    """
    url = BASE_URL + "getUpdates"
    payload = {"timeout": 100, "offset": offset}
    js = get_json_from_url(url, payload)
    return js


def build_keyboard(items):
    """
    Build a keyboard from the notes showing each note id in a row,
    and return the required json to display it
        @items: dictionary with notes to display
    """
    keyboard = [[str(key)] for key in items.keys()]
    reply_markup = {"keyboard": keyboard, "one_time_keyboard": True}
    return json.dumps(reply_markup)


def send_message(text, chat_id, reply_markup=None):
    """
    Send a message to a chat
        @text: message text to be sent
        @chat_id: chat_id where the message will be sent
        @reply_markup: json to display keyboard
    """
    url = BASE_URL + "sendMessage"
    payload = {"text": text, "chat_id": chat_id, "parse_mode": "Markdown"}
    if reply_markup:
        payload["reply_markup"] = reply_markup
    try:
        get_url(url, payload)
    except requests.exceptions.RequestException as e:
        logging.error(e)


def handle_updates(updates):
    """
    Given a list of updates, build and send messages depending on the
    commands the user sent in those updates
        @updates: list of updates retrieved from the API
    """
    for update in updates["result"]:
        try:
            message = ""
            keyboard = None
            text = update["message"]["text"]  # id to delete or text to add
            chat = update["message"]["chat"]["id"]  # user
            items = dict(db.get_items(chat))  # ((id, text),) => {id:text,}
            try:
                id_note = int(text)
            except ValueError:  # Not integer
                if text.startswith(("/", "@")):  # Command
                    if text == "/del":  # Commmand to delete note
                        keyboard = build_keyboard(items)
                        if keyboard[13:15] != "[]":  # There are notes
                            message = "*Select a note to delete:*\n"
                    elif text == "/start":
                        message = """Hello! I will remember what you say.

Enter their number or type /del for deleting your notes.\n"""
                    elif text == "/help":
                        message = """Enter text to create a new note.
You will see a list of all the notes that you have created until now.
Enter their number or type /del for deleting a specific note.\n"""
                    else:
                        continue  # Ignore this update
                else:  # Create note
                    db.add_item(chat, text)
            else:
                if id_note in items.keys():  # Delete
                    db.delete_item(chat, id_note)
                else:
                    message = f"*Note {id_note} not found.*\n"
            items = db.get_items(chat)
            message += "\n".join(f"*{key}:* {value}" for key, value in items)
            if not message:
                message = "There are no notes. Add one by sending a message."
            send_message(message, chat, keyboard)
        except KeyError:
            logging.debug("User message is not a new text.")


def get_last_update_id(updates):
    """
    Return last update_id from the list of updates
        @updates: list of updates retrieved from the API
    """
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def main():
    format = "%(asctime)-15s %(levelname)s: %(message)s"
    logging.basicConfig(format=format, level=logging.DEBUG)
    db.setup()
    last_update_id = None
    while True:
        logging.debug("Getting updates...")
        try:
            updates = get_updates(last_update_id)
        except requests.exceptions.RequestException as e:
            logging.error(e)
        else:
            if updates["ok"] and updates["result"]:
                last_update_id = get_last_update_id(updates) + 1
                handle_updates(updates)
            elif not updates["ok"]:
                logging.error(f"No OK response: {updates}")  # Test
        time.sleep(2)

if __name__ == "__main__":
    main()
