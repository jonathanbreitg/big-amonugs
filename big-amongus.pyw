import os
import pickle
from dotenv import load_dotenv,set_key
load_dotenv('.env')
#user variables here
CHANNEL = os.environ.get("CHANNEL")
TOKEN = os.environ.get("TOKEN")
OWNER = os.environ.get("OWNER")
if os.path.exists('.STARTUP'):
    f = open(".STARTUP",'r')
    instructs = f.read()
    instructs = eval(instructs)

if os.path.exists('.ALLOWED'):
    f = open(".ALLOWED","rb")
    ALLOWED = pickle.load(f)
    print(ALLOWED)
else:
    ALLOWED = set()
# ALLOWED = os.environ.get("ALLOWED")
# if type(ALLOWED) != set:
#     ALLOWED = set(ALLOWED)

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


def update_config(set_obj:set):
    f = open('.ALLOWED',"wb")
    pickle.dump(set_obj,f)


def add_to_set(set_obj:set,list_obj:list):
    for obj in list_obj:
        set_obj.add(obj.id)
    update_config(set_obj)
    return set_obj

def remove_from_set(set_obj:set,list_obj:list,message):
    for obj in list_obj:
        try:
            set_obj.remove(obj.id)
        except Exception as e:
            message.channel.send(f"{message.author.mention} user:{obj.mention} never had acces to execute commands on `{os.getlogin()}` ")
    update_config(set_obj)
    return set_obj

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
    global OWNER
    global ALLOWED
    id_managing()
    async def on_ready(self):
        self.owner = await self.fetch_user(OWNER)
        print("owner is ",self.owner)
        print("ALLOWED:",ALLOWED)
        if (len(ALLOWED) > 1):
            self.exec_perms = ALLOWED
        else:
            self.exec_perms = {self.owner.id}
        print("self.exec_perms",self.exec_perms)
        print(f'Logged on as {self.user}!')
        channel = self.get_channel(int(CHANNEL))
        print(self.owner)
        await channel.send(f"{self.owner.mention} new user!\n`{os.getlogin()}` : ***{id}***\nowner is: {self.owner}")
        self.in_session = False

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content} : {message.channel}')
        if message.author == self.owner:
            print("from owner")
        if message.author != self.user and message.author.id in self.exec_perms:
            if self.in_session:
                if message.content.startswith("-@") and (message.content[2:] == os.getlogin() or message.content[2:] == id):
                    self.in_session = False
                    await message.channel.send(f"```diff\n-{os.getlogin()} has stopped listening for commands!\n```",reference=message)
                    return
                elif message.content.startswith("+!") and message.author == self.owner:
                    print("self exec perms",self.exec_perms)
                    self.exec_perms = add_to_set(self.exec_perms,message.mentions)
                    print(self.exec_perms)
                    tag = ""
                    for person in message.mentions:
                        tag += person.mention
                        await person.send(f"you have been granted acces by {message.author} to execute commands on `{os.getlogin()}` : ***{id}***!")
                    await message.channel.send(f"{tag} have been granted acces to execute commands on `{os.getlogin()}` : ***{id}***!")
                elif message.content.startswith("-!") and message.author == self.owner:
                    self.exec_perms = remove_from_set(self.exec_perms,message.mentions,message)
                    print(self.exec_perms)
                    tag = ""
                    for person in message.mentions:
                        tag += person.mention
                        await person.send(f"you have been removed acces by {message.author} to execute commands on `{os.getlogin()}` : ***{id}***!")
                    await message.channel.send(f"{tag} have been removed acces to execute commands on `{os.getlogin()}` : ***{id}***!")
                else:
                    if message.author.id in self.exec_perms:

                        t = threading.Thread(target=executer,args=(message,self,))
                        t.start()
                    else:
                        await message.channel.send(f"you don't have acces to execute commands on `{os.getlogin()}` : ***{id}***",reference=message)
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