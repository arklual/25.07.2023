from pyrogram import Client, filters, enums
from pyrogram.types import Message
import pygsheets
from datetime import datetime, date
import zoneinfo
import asyncio
import aiofiles

from settings import *

app = Client("bot", api_id=api_id, api_hash=api_hash)
app.start()
zone = zoneinfo.ZoneInfo("Europe/Moscow")
gc = pygsheets.authorize(service_account_file='sheets_key.json')
ws = gc.open('База писывших людей').worksheet()

ids = ws.get_col(1)
for n,i in enumerate(ids):
    if i == '':
        ids = ids[:n]
        break

for dialog in app.get_dialogs(limit=100):
    if dialog.chat.type == enums.ChatType.PRIVATE:
        if str(dialog.chat.id) not in ids:
            ids.append(str(dialog.chat.id))
            ws.update_row(len(ids), [dialog.chat.id, dialog.chat.first_name, dialog.chat.last_name, dialog.chat.username, '', str(datetime.now(zone).date())]) 
app.stop()