import asyncio
import warnings
import time
import os
import pytgcalls
import pyrogram
from pyrogram.errors.rpc_error import RPCError
from pyrogram.errors import FloodWait
from pyrogram.errors.exceptions.bad_request_400 import GroupCallInvalid
from pyrogram import Client
from pytgcalls.utils import AudioStream
from sqlite3 import OperationalError

API_ID = 'ID'
API_HASH = 'HASH'
CHAT_ID = '@GroupUsername' # it can be a channel too
directory = os.getcwd()

my_apps = []
for foldername, subfolders, filenames in os.walk(directory):
           for f in filenames:
              fl = f.split(".")[1]
              if (fl == 'session'):
                  base = f.split('.')[0]
                  my_apps.append(base)
#
# proxy = {
#  "scheme": "socks5",
#  "hostname": "31.42.57.1",
#  "port": 3699,
#  "username": "username",
#  "password": "password"
# }
async def start_audio(self, source=None, repeat=True, video_stream=None):
    if self._audio_stream and self._audio_stream.is_running:
        self._audio_stream.stop()
    if source:
        self._audio_stream = AudioStream(
            source, repeat, self.__combined_audio_trigger, video_stream=video_stream
        ).start()

        if self.is_connected:
            await self.edit_group_call(muted=False)

async def main(client):
    group_call = pytgcalls.GroupCallFactory(client).get_group_call()
    await group_call.join(CHAT_ID)
    group_call.start_audio = start_audio
    await group_call.start_audio(group_call, None)
    await pyrogram.idle()

def runtime():
    loop.create_task(asyncio.gather(main(tele_client)))
while True:
    for num in my_apps:
        tele_client = Client(f'{num}', int(API_ID), API_HASH)
        try:
            tele_client.start()
            loop = asyncio.get_event_loop()
            loop.run_until_complete(runtime())
        except Exception as e:
            pass
        except OperationalError as e:
            pass
        except GroupCallInvalid as e:
            pass
        except TimeoutError as e:
            print("Time Out")
            pass
        except RuntimeWarning as e:
            pass
        except FloodWait as e:
            pass

