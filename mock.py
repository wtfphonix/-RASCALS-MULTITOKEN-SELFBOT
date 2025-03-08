# token in line 24 only
# kof kof kof
# kof kof kof
# kof kof kof
# kof kof kof
# kof kof kof
# kof kof kof
# kof kof kof
# kof kof kof
# kof kof kof
# kof kof kof

import discord
from discord.ext import commands, tasks
import asyncio
import random
from itertools import cycle
import aiohttp
from colorama import Fore, Style, init

intents = discord.Intents.default()
intents.messages = True

token = ''

bot = commands.Bot(command_prefix="x", self_bot=True, intents=intents, bot=False)

print("kofkofkofkofkofkofkofkofkofkofkofkofkofkofkofkofkofkofkofkofkofkofkofkofkof")

@bot.event
async def on_ready():
    print(f"false god @{bot.user}")

react_active = False
active_spammers = {}
tokens = []
selfreact_active = False
ar_active = False

@bot.command()
async def ar(ctx, user: discord.User, *, message: str):
    global ar_active
    ar_active = True
    def check(msg):
        return msg.author == user and ar_active

    while ar_active:
        msg = await bot.wait_for("message", check=check)
        await msg.reply(message)
    await ctx.message.delete()

@bot.command()
async def are(ctx):
    global ar_active
    ar_active = False
    print(f"Stopped auto-reply")
    await ctx.message.delete()

@bot.command()
async def sr(ctx, user: discord.User, emoji: str):
    global react_active
    react_active = True
    def check(message):
        return message.author == user and react_active
    
    async for message in ctx.channel.history(limit=1):
        if message.author == user:
            await message.add_reaction(emoji)
    await ctx.message.delete()
    while react_active:
        message = await bot.wait_for("message", check=check)
        await message.add_reaction(emoji)

@bot.command()
async def sre(ctx, user: discord.User):
    global react_active
    react_active = False
    print(f"Stopped reacting to messages by {user}")
    await ctx.message.delete()

@bot.command()
async def stream(ctx, *, name: str):
    global active_clients

    try:
        with open('tokens.txt', 'r') as file:
            tokens = [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        await ctx.send("```No file called tokens.txt found```")
        return

    token_cycle = cycle(tokens)

    async def stream_with_token(token, name):
        user_client = discord.Client(intents=discord.Intents.default())
        
        @user_client.event
        async def on_ready():
            await user_client.change_presence(
                activity=discord.Streaming(name=name, url="https://twitch.tv/kof")
            )
            await user_client.close()

        try:
            await user_client.start(token, bot=False)
        except discord.LoginFailure:
            print(f"Invalid token: {token[-4:]}")
        except Exception as e:
            print(f"Error with token {token[-4:]}: {e}")

    for token in token_cycle:
        await stream_with_token(token, name)
        await asyncio.sleep(1)  

    await ctx.message.delete()
    print(f"Started streaming with multiple tokens: {name}")

@bot.command()
async def gc(ctx, user: discord.User, *, base_name: str = "Test"):
    channel = ctx.channel
    if channel.id in active_spammers:
        await ctx.send("Gc command is running")
        return

    active_spammers[channel.id] = True
    await ctx.message.delete()
    await ctx.send(f"```Started spamming```")

    index = 1
    while active_spammers.get(channel.id):
        new_name = f"{base_name} {index}"
        try:
            await channel.edit(name=new_name)
            print(f"Changed group chat name to: {new_name}")
        except discord.Forbidden:
            print("Forbidden to change group chat name.")
        except discord.HTTPException as e:
            print(f"HTTP Exception: {e}")
            await asyncio.sleep(5)

        joke = random.choice(open('jokes.txt').readlines()).strip()
        try:
            await channel.send(f"{joke} {user.mention}")
            await asyncio.sleep(random.uniform(0.5, 2.5))
        except discord.HTTPException as e:
            print(f"HTTP Exception: {e}")
            await asyncio.sleep(5)

        index += 1
    
menu_access_granted = False

@bot.check
async def global_check(ctx):
    global menu_access_granted

    if ctx.command.name == "menu":
        return True

    if not menu_access_granted:
        await ctx.send("```Access denied. Your a skid loser```")
        return False

    return True

@bot.command()
async def gce(ctx):
    channel = ctx.channel
    if channel.id in active_spammers:
        active_spammers[channel.id] = False
        await ctx.send("```Stopped gc spamming in this channel```")
    else:
        await ctx.send("```No active gc spamming found in this channel```")
    await ctx.message.delete()

def load_tokens():
    global tokens
    try:
        with open("tokens.txt", "r") as file:
            tokens = file.read().splitlines()
    except FileNotFoundError:
        print("```Error: tokens.txt file not found```")
    tokens = [token.strip() for token in tokens if token.strip()]

async def react_with_tokens(message_id, channel_id, emoji):
    """
    React to a specific message with all tokens from tokens.txt.
    """
    url = f"https://discord.com/api/v9/channels/{channel_id}/messages/{message_id}/reactions/{emoji}/@me"
    headers_list = [{"Authorization": token, "Content-Type": "application/json"} for token in tokens]

    async with aiohttp.ClientSession() as session:
        for headers in headers_list:
            try:
                async with session.put(url, headers=headers) as response:
                    pass  
            except Exception:
                pass  

@bot.command()
async def tokreact(ctx, emoji: str):
    global selfreact_active
    selfreact_active = True

    def check(message):
        return message.author == bot.user and selfreact_active

    await ctx.message.delete()
    await ctx.send(f"```Self-reaction mode activated with emoji: {emoji}```", delete_after=5)

    while selfreact_active:
        message = await bot.wait_for("message", check=check)
        bot.loop.create_task(react_with_tokens(message.id, message.channel.id, emoji))

@bot.command()
async def tokreacte(ctx):
    global selfreact_active
    if selfreact_active:
        selfreact_active = False
        await ctx.send("```Self-reaction mode deactivated```", delete_after=5)
    else:
        await ctx.send("```Self-reaction mode is not active```", delete_after=5)

tokens = []  
active_clients = {} 
gc_name_counter = 1  

with open("tokens.txt", "r") as file:
    tokens = [line.strip() for line in file.readlines()]

def load_jokes():
    try:
        with open("jokes.txt", "r") as file:
            return [joke.strip() for joke in file.readlines()]
    except FileNotFoundError:
        return []

class KofMadeThisForRoot(discord.Client):
    def __init__(self, token, channel_id, user_to_ping=None, mode=1, name_base=None, change_name=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.token = token
        self.channel_id = channel_id
        self.running = True
        self.mode = mode
        self.jokes = load_jokes()
        self.user_to_ping = user_to_ping
        self.name_base = name_base
        self.change_name = change_name

    async def on_ready(self):
        print(f"Client with token {self.token[-4:]} is ready")
        await self.start_spamming()

    async def start_spamming(self):
        global gc_name_counter
        channel = self.get_channel(self.channel_id)
        if channel is None:
            print(f"Channel with ID {self.channel_id} not found for token {self.token[-4:]}")
            return

        while self.running:
            joke = random.choice(self.jokes) if self.jokes else "No jokes available"
            try:
                if self.mode == 2:
                    content = f"# {joke} {joke} {joke} {joke} {joke} {joke} {joke} {joke} {joke} {joke} {joke} {joke} {joke} {joke} {joke} {joke} {joke} {joke} {joke} {joke} {joke} {joke} {joke} {joke} {joke} {joke} {joke} {joke} {joke} {joke} {joke} {joke} {joke} {joke} {joke} {joke} {joke} {joke} {joke} {joke} {joke} {joke} {joke} {joke} {joke} {joke} {joke} {joke} {self.user_to_ping.mention if self.user_to_ping else ''}"
                elif self.mode == 3:
                    content = '{} {}'.format('\n'.join(joke.split()), self.user_to_ping.mention if self.user_to_ping else '')
                else:
                    content = f"{joke} {self.user_to_ping.mention if self.user_to_ping else ''}"
                if self.change_name and channel.type == discord.ChannelType.group:
                    new_name = f"{self.name_base} {gc_name_counter}"
                    try:
                        await channel.edit(name=new_name)
                        print(f"Changed group chat name to: {new_name}")
                        gc_name_counter += 1
                    except discord.Forbidden:
                        print(f"Permission denied to change group chat name.")
                    except discord.HTTPException as e:
                        print(f"HTTP exception while changing group chat name: {e}")

                await channel.send(content)
                await asyncio.sleep(random.uniform(0.5, 2))  

            except discord.HTTPException as e:
                print(f"HTTP Exception for token {self.token[-4:]}: {e}")
                await asyncio.sleep(5)

@bot.command()
async def menu(ctx):
    global menu_access_granted

    if menu_access_granted:
        await ctx.send("```You have already been blessed.```")
        return

    red_ini_font = "```ini\n[kof for root]```"
    black_ini_font = "```ini\n     Please enter the password\n```"
    blue_ini_font = "```ini\n [touch of a god] ```"
    
    await ctx.send(red_ini_font)
    await ctx.send(black_ini_font)
    await ctx.send(blue_ini_font)

    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    try:
        response = await bot.wait_for("message", check=check, timeout=30.0)
        if response.content == str(ctx.author.id):
            menu_access_granted = True
            await ctx.send("```ini\n[the gods have blessed you]```")
        else:
            await ctx.send("```ini\nYOU ARE NOT THE OWNER```")
    except asyncio.TimeoutError:
        await ctx.send("```ini\nYou took too long to respond```")

@bot.command()
async def t(ctx, user: discord.User = None):
    global active_clients

    if active_clients:
        await ctx.send("```T command is already running. Stop it first using `te`.```")
        return

    channel_id = ctx.channel.id
    jokes = load_jokes()
    if not jokes:
        await ctx.send("```No jokes found in jokes.txt.```")
        return

    for token in tokens:
        client = KofMadeThisForRoot(token, channel_id, user_to_ping=user)
        active_clients[token] = client
        asyncio.create_task(client.start(token, bot=False))

    await ctx.send("```T command started.```")

@bot.command()
async def te(ctx):
    global active_clients

    if not active_clients:
        await ctx.send("```T command is not running.```")
        return

    for token, client in list(active_clients.items()):
        client.running = False
        await client.close()
        del active_clients[token]

    await ctx.send("```T command stopped.```")

@bot.command()
async def um(ctx, mode: int):
    global active_clients

    if mode not in [1, 2, 3]:
        await ctx.send("```Invalid mode. Choose between 1, 2, or 3.```")
        return

    if not active_clients:
        await ctx.send("```No active spamming sessions to update.```")
        return

    for client in active_clients.values():
        client.mode = mode

    await ctx.send(f"```T command mode updated to {mode}.```")

@bot.command()
async def god(ctx, user: discord.User, *, gc_name: str):
    global active_clients, gc_name_counter
    gc_name_counter = 1

    for client in active_clients.values():
        client.running = False
        await client.close()

    channel_id = ctx.channel.id

    for token in tokens:
        client = KofMadeThisForRoot(
            token, channel_id, user_to_ping=user, name_base=gc_name, change_name=True
        )
        active_clients[token] = client
        asyncio.create_task(client.start(token, bot=False))

    await ctx.send("```Started `god` command.```")

@bot.command()
async def gode(ctx):
    global active_clients

    for token, client in list(active_clients.items()):
        client.running = False
        await client.close()
        del active_clients[token]

    await ctx.send("```Stopped `god` command.```")

@bot.command()
async def tm(ctx):
    await ctx.send("Mimicking all messages...")

    tokens = load_tokens()

    bots = []

    mimicking = True

    async def mimic_with_token(token, message):
        """Use a token to mimic a message once in all channels and DMs."""
        try:
            new_bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())

            @new_bot.event
            async def on_ready():
                for guild in new_bot.guilds:
                    for channel in guild.text_channels:
                        await channel.send(message.content)  
                try:
                    await new_bot.user.send(message.content)  
                except discord.errors.Forbidden:
                    pass  

                print(f"Bot with token {token} is ready and mimicking messages...")

            await new_bot.start(token, bot=False)
            bots.append(new_bot)  
        except Exception as e:
            print(f"Error with token {token}: {e}")

    @bot.event
    async def on_message(message):
        if message.author == ctx.author:
            if mimicking:
                for token in tokens:
                    await mimic_with_token(token, message)

        await bot.process_commands(message)

    await bot.process_commands(ctx)

    @bot.command()
    async def tme(ctx):
        nonlocal mimicking
        mimicking = False
        for bot_instance in bots:
            await bot_instance.close()
        bots.clear()
        await ctx.send("Mimicking stopped.")

bot.run(token, bot=False)

