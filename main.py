import discord
import time
import random
import os
import json
import websockets
import io
import threading
from datetime import datetime
from gcfill import GCFill
running_processes = {}
from discord.client import aiohttp
import asyncio
import subprocess
import requests
from discord.ext import commands

token = "" 

alw_handler = None
# Load jokes from a file
def load_jokes():
    with open("jokes.txt", "r") as file:
        return [line.strip() for line in file.readlines()]

# Discord bot setup
intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.guilds = True
intents.dm_messages = True
intents.guild_messages = True

prefix = ","

# Define a function to get the current prefix
def get_prefix(bot, message):
    return prefix

# Set up the bot
intents = discord.Intents.default()
bot = commands.Bot(command_prefix=get_prefix, self_bot=True, intents=intents)
# Command to change the prefix
@bot.command()
async def p(ctx, new_prefix):
    global prefix
    if new_prefix.lower() == "none":
        prefix = ""  # Set prefix to nothing
        await ctx.send("Prefix removed. Commands can now be used without a prefix.")
    else:
        prefix = new_prefix
        await ctx.send(f"Prefix changed to: {new_prefix}")

 
             
            

@bot.command()
async def menu(ctx):
    # Delete the command invocation message
    await ctx.message.delete()

    # Send the initial welcome messages
    msg1 = await ctx.send("```css\n        [招呼 x 屠杀]\n```")
    msg2 = await ctx.send("```css\n          WELCOME, \n       RASCALS  SELFBOT.\n   SAY ENTER TO PROCEED.\n```")
    msg3 = await ctx.send("```css\n      [RASCALS  X SELFBOT]\n```")

    # Function to check if the message is from the correct user and channel
    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    # Wait for the user to type "enter"
    try:
        while True:
            response = await bot.wait_for("message", check=check, timeout=30)
            await response.delete()  # Auto-delete the response

            if response.content.lower() == "enter":
                await msg2.edit(content="```css\n        RASCALS X SELFBOT CLIENTS\n[1] Beef\n[2] Utility\n[3] Troll\n```")
                break  # Exit to the main screen
            else:
                await msg2.edit(content=msg2.content + "\n    Please say enter.")  # Invalid input response

        # Main screen loop
        while True:
            try:
                response = await bot.wait_for("message", check=check, timeout=30)
                await response.delete()  # Auto-delete the response

                if response.content == '1':
                    # Beef screen
                    await msg2.edit(content="```css\n      [RASCALS X SELFBOT]\n[1] Auto Responder\n[2] Auto Pressure\n[3] Groupchat Commands\n```")
                    await handle_beef_screen(ctx, msg2)

                elif response.content == '2':
                    # Utility screen
                    await msg2.edit(content="```css\n      [UTILITY]\n[1] Anti Snake\n[2] Logger\n[3] React\n[4] Streaming\n[5] Status\n[6] Guild\n[7] VC Commands\n```")
                    await handle_utility_screen(ctx, msg2)

                elif response.content == '3':
                    # Troll screen
                    await msg2.edit(content="```css\n      [TROLL]\n[1] Kiss <user>\nkisses user\n[2] Phc <user> <message>\nfake ph comment\n[3] Tweet <name> <message>\nfake tweet\n```")
                    await handle_troll_screen(ctx, msg2)

                elif response.content.lower() == "end":
                    await msg1.delete()
                    await msg2.delete()
                    await msg3.delete()
                    return  # Exit the command
                else:
                    await msg2.edit(content=msg2.content + "\n    Please say 1, 2, or 3.")  # Invalid input

            except asyncio.TimeoutError:
                await ctx.send("You took too long to respond!").delete(delay=1)

    except asyncio.TimeoutError:
        await ctx.send("You took too long to respond!").delete(delay=1)

async def handle_beef_screen(ctx, msg2):
    while True:
        response = await bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=30)
        await response.delete()  # Auto-delete the response

        if response.content == '1':
            await msg2.edit(content="```css\n      Auto Responder\n[1] ar <userid> <position>\nreplies to user with that token\n[2] are <position>\nends reply to user with that token\n[3] am <position> <mode>\nchanges mode for that token\n[4] ara <userid>\nstarts replies with all tokens\n[5] arae\nends replies with all tokens\n[6] ama <mode>\nchanges mode for all tokens\n```")  # Auto Responder screen
        elif response.content == '2':
            await msg2.edit(content="```css\n      Auto Pressure\n[1] ap <channelid> <position>\nstarts ap with that token\n[2] ape <position>\nends ap with that token\n[3] apm <position> <mode>\nchanges mode with that token\n[4] apd <position> <delay>\nchanges delay with that token\n[5] app <position> <userid>\nstarts pinging userid with that token\![6] apa <channelid>\nstarts ap with all tokens\n[7] apae\nends ap with all tokens\n[8] apda <delay>\nchanges delay with all tokens\n[9] apma <mode>\nchanges mode for all tokens\n[10] appa <userid>\npings user with all tokens\n[11] m <channelid> <position>\nfake manual with that token\n[12] me <position>\nends fake manual with that token\n[13] mm <position> <mode>\nchanges mode with that token\n[14] mp <position> <userid>\npings user with that token\n[15] ma <channelid>\nstarts manual with all tokens\n[16] mae\nends manual with all tokens\n[17] mma <mode>\nchanges mode for all tokens\n[18] mpa <userid>\npings user with all tokens\n[19] kill <user> <channelid>\nstarts pinging user with tokens\n[20] kille\nends kill command\n```")  # Auto Pressure screen
        elif response.content == '3':
            await msg2.edit(content="```css\n      Groupchat Commands\n[1] gct <channelid> <position> <name>\nchanges name with that token\n[2] gcte <position>\nends name change with that token\n[3] gcta <channelid> <name>\nstarts name change with all tokens\n[4] gctae\nends name change with all tokens\n```")  # Groupchat Commands screen
        elif response.content.lower() == "back":
            await msg2.edit(content="```css\n        RASCALSCLIENTS\n[1] Beef\n[2] Utility\n[3] Troll\n```")  # Return to main menu
            break  # Exit the Beef screen loop
        elif response.content.lower() == "end":
            await ctx.send("Ending the menu...").delete(delay=1)  # Optional end message
            return  # Exit the command
        else:
            await msg2.edit(content=msg2.content + "\n    Please say 1, 2, or 3.")  # Invalid input

async def handle_utility_screen(ctx, msg2):
    while True:
        response = await bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=30)
        await response.delete()  # Auto-delete the response

        if response.content == '1':
            await msg2.edit(content="```css\n      Anti Snake\n[1] alw <on/off>\nturns on/off anti last word\n[2] agct <on/off>\nturns on/off anti gc trap\n[3] gcf\ninitiates gc fill listener\n[4] gcfe\nends gc fill listener\n[5] wl <userid>\nwhitelists user for alw\n[6] gcwl <userid>\nwhitelists user for agct\n[7] uid <userid>\nadds user to gcfill.txt\n[8] gcfill\nadds users to gc from gcfill.txt\n[9] afk <user>\nstarts anti afk check for user\n[10] afke <user>\nends anti afk check for user\n```")  # Anti Snake screen
        elif response.content == '2':
            await msg2.edit(content="```css\n      Logger\n[1] log <on/off>\nstarts/endslogging\n[2] clearlog\nclears logs\n[3] displaylog\nshows all logs\n[4] display <number>\nshows specific log\n[5] purge <number>\ndeletes number of messages\n[6] av <user>\nreturns users avatar\n[7] tc\nchecks valid tokens\n[8] ul\nsends username list\n[9] p <new prefix>\nchanges prefix ```")  # Logger screen
        elif response.content == '3':
            await msg2.edit(content="```css\n      React\n[1] react <userid> <position> <emoji>\n[2] reactend <position>\n[3] re\n[4] ree\n```")  # React screen
        elif response.content == '4':
            await msg2.edit(content="```css\n      Streaming\n[1] ss <statuses>\nsets stream status list to rotate\n[2] ssr\nstarts rotation\n[3] ssd <delay>\nchanges delay\n[4] ssre\nends rotating\n[5] rss <statuses>\nstarts rotation for all tokens\n[6] rsse\nends rotation for all tokens\n[7] rssd <delay>\nchanges delay for all tokens\n```")  # Streaming screen
        elif response.content == '5':
            await msg2.edit(content="```css\n      Status\n[1] s <statuses>\nsets statuses to rotate\n[2] sr\nstarts rotating statuses\n[3] sd <delay>\nchanges delay to rotate\n[4] sre\nends status rotation\n```")  # Status screen
        elif response.content == '6':
            await msg2.edit(content="```css\n      Guild\n[1] rg\nstarts guild rotate\n[2] rgd <delay>\nchanges guild rotate delay\n[3] rge\nends guild rotate\n```")  # Guild screen
        elif response.content == '7':
            await msg2.edit(content="```css\nVC Commands\n[1] vc <channelid>\nstarts vc connection,has to be invoked in dms to call a dm or gc and invoked in server for a server vc\n[2] vce\nends vc connection```")  # VC Commands screen
        elif response.content.lower() == "back":
            await msg2.edit(content="```css\n        RASCALSCLIENTS\n[1] Beef\n[2] Utility\n[3] Troll\n```")  # Return to main menu
            break  # Exit the Utility screen loop
        elif response.content.lower() == "end":
            await ctx.send("Ending the menu...").delete(delay=1)  # Optional end message
            return  # Exit the command
        else:
            await msg2.edit(content=msg2.content + "\n    Please say 1, 2, or 3.")  # Invalid input

async def handle_troll_screen(ctx, msg2):
    while True:
        response = await bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=30)
        await response.delete()  # Auto-delete the response

        if response.content == '1':
            await msg2.edit(content="```css\n      Kiss\n[1] kiss <user>\n```")  # Kiss command
        elif response.content == '2':
            await msg2.edit(content="```css\n      Fake PHC\n[1] phc <user> <message>\n```")  # PHC command
        elif response.content == '3':
            await msg2.edit(content="```css\n      Fake Tweet\n[1] tweet <name> <message>\n```")  # Tweet command
        elif response.content.lower() == "back":
            await msg2.edit(content="```css\n        RASCALSCLIENTS\n[1] Beef\n[2] Utility\n[3] Troll\n```")  # Return to main menu
            break  # Exit the Troll screen loop
        elif response.content.lower() == "end":
            await ctx.send("Ending the menu...").delete(delay=1)  # Optional end message
            return  # Exit the command
        else:
            await msg2.edit(content=msg2.content + "\n    Please say 1, 2, or 3.")  # Invalid input

 
        




send_messages = {}
current_modes = {}  # Store current modes for each token
message_count = {}  # Count of messages sent per token
jokes1 = []  # Load jokes from mjokes.txt
image_links = {}  # Dictionary to store image links for each token
user_react_dict = {}  # Dictionary to store user IDs to ping for each token

# Load jokes from mjokes.txt
def load_jokes():
    with open('mjokes.txt', 'r') as file:
        jokes = file.readlines()
    return [joke.strip() for joke in jokes]

jokes1 = load_jokes()

def read_tokens(filename='tokens2.txt'):
    """Read tokens from a file and return them as a list."""
    with open(filename, 'r') as file:
        tokens = file.read().splitlines()
    return tokens

def get_token_by_position(position):
    """Retrieve a token by its position from the tokens list, adjusted for 1-based indexing."""
    tokens = read_tokens()
    # Adjust for 1-based position by subtracting 1 from the input
    if 1 <= position <= len(tokens):
        return tokens[position - 1]
    return None

class MessageBot(discord.Client):
    def __init__(self, token, channel_id, position, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.token = token
        self.channel_id = channel_id
        self.position = position

    async def on_ready(self):
        print(f'Logged in as {self.user} using token {self.token[-4:]}.')
        await self.send_messages()

    async def send_messages(self):
        global message_count
        channel = self.get_channel(self.channel_id) or await self.fetch_channel(self.channel_id)

        while send_messages.get(self.position, False):
            message_count[self.position] = message_count.get(self.position, 0) + 1

            # Check if message count exceeds 7
            if message_count[self.position] > 7:
                current_modes[self.position] = 2  # Switch to mode 2 for 10 seconds
                await asyncio.sleep(10)  # Wait for 10 seconds
                current_modes[self.position] = 7  # Revert back to mode 7
                message_count[self.position] = 0  # Reset message count

            # Select a random joke
            joke = random.choice(jokes1)
            words = joke.split()
            ping_user = user_react_dict.get(self.position, None)  # Get the user ID to ping

            await self.simulate_typing(channel)

            mode = current_modes.get(self.position, 1)  # Default to mode 1 if not set

            if mode == 1:  # Mode 1: Randomly sends 1 or 2 words at a time
                i = 0
                while i < len(words):
                    if i < len(words) - 1 and random.random() < 0.5:
                        # Send two words
                        msg = words[i] + " " + words[i + 1]
                        i += 2
                    else:
                        # Send one word
                        msg = words[i]
                        i += 1

                    await channel.send(msg)
                    await self.maybe_ping_user(channel, ping_user)
                    await asyncio.sleep(random.uniform(0.9, 1.4))  # Adjusted delay

            elif mode == 2:  # Mode 2: Sends the whole joke as a sentence
                await channel.send(joke)
                await self.maybe_ping_user(channel, ping_user)
                await asyncio.sleep(random.uniform(2.5, 3.5))

            elif mode == 3:  # Mode 3: Sends each word on a new line
                new_line_msg = '\n'.join(words)
                await channel.send(new_line_msg)
                await self.maybe_ping_user(channel, ping_user)
                await asyncio.sleep(random.uniform(2.5, 3.5) + 0.1)

            elif mode == 4:  # Mode 4: Header format
                header_msg = f"# {joke}"
                await channel.send(header_msg)
                await self.maybe_ping_user(channel, ping_user)
                await asyncio.sleep(random.uniform(2.5, 3.5) + 0.5)

            elif mode == 5:  # Mode 5: > # format
                header_msg = f"> # {joke}"
                await channel.send(header_msg)
                await self.maybe_ping_user(channel, ping_user)
                await asyncio.sleep(random.uniform(2.5, 3.5) + 0.5)

            elif mode == 6:  # Mode 6: More configurations as needed
                await channel.send(joke)
                await self.maybe_ping_user(channel, ping_user)
                await asyncio.sleep(random.uniform(2.5, 3.5))

            elif mode == 7:  # Mode 7: Combination of modes 1, 2, and 3
                format_choice = random.randint(1, 3)
                if format_choice == 1:  # Mode 1
                    i = 0
                    while i < len(words):
                        if i < len(words) - 1 and random.random() < 0.5:
                            msg = words[i] + " " + words[i + 1]
                            i += 2
                        else:
                            msg = words[i]
                            i += 1

                        await channel.send(msg)

                elif format_choice == 2:  # Mode 2
                    await channel.send(joke)

                elif format_choice == 3:  # Mode 3
                    new_line_msg = '\n'.join(words)
                    await channel.send(new_line_msg)

    async def maybe_ping_user(self, channel, user_id):
        """Ping the user with 100% chance."""
        if user_id:
            await channel.send(f"<@{user_id}>")

    async def simulate_typing(self, channel):
        """Simulate typing before sending a message."""
        async with channel.typing():
            await asyncio.sleep(random.uniform(1, 3))  # Simulate typing for a random time




@bot.command()
async def ma(ctx, channel_id: int):
    """Start sending messages using all tokens in the specified channel simultaneously."""
    global send_messages
    tokens = read_tokens()
    tasks = []

    for position, token in enumerate(tokens):
        send_messages[position] = True  # Ensure message sending is allowed for the specified token
        message_count[position] = 0  # Reset message count for this token
        current_modes[position] = 1  # Default to mode 1 for this token

        client = MessageBot(token, channel_id, position)
        tasks.append(client.start(token, bot=False))  # Create a task for each token

    await asyncio.gather(*tasks)  # Start all tasks simultaneously

@bot.command()
async def mae(ctx):
    """Stop sending messages for all tokens."""
    global send_messages
    for position in send_messages.keys():
        send_messages[position] = False  # Disable sending messages for each token
    await ctx.send("Stopped all tokens from sending messages.")
@bot.command()
async def mp(ctx, position: int, user_id: int):
    """Set the user ID to ping at the end of the messages for the specified token."""
    token = get_token_by_position(position - 1)  # Adjusted for 1-based index, as you requested
    if token:
        user_react_dict[position - 1] = user_id  # Set user ID to ping for the specified token
        await ctx.send(f"Will ping user <@{user_id}> at the end of messages sent by token at position {position}.")
    else:
        await ctx.send("Invalid position! Please provide a position between 1 and the number of tokens.")
@bot.command()
async def mpa(ctx, user_id: int):
    """Set all tokens to ping the specified user ID."""
    for position in range(len(send_messages)):
        token = get_token_by_position(position)  # Adjusted for 1-based index
        if token:
            user_react_dict[position] = user_id  # Set user ID to ping for all tokens
    await ctx.send(f"All tokens will now ping user <@{user_id}> at the end of messages.")

@bot.command()
async def mma(ctx, mode: int):
    """Change the mode for all tokens."""
    global current_modes
    if mode in range(1, 8):  # Ensure the mode is between 1 and 7
        for position in range(len(current_modes)):  # Iterate through all tokens
            current_modes[position] = mode  # Set the mode for each token
        await ctx.send(f"All tokens have been set to mode {mode}.")
    else:
        await ctx.send("Invalid mode! Please enter a mode between 1 and 7.")  
@bot.command()
async def mm(ctx, position: int, mode: int):
    """Change the mode of the token at the specified position."""
    token = get_token_by_position(position - 1)  # Adjusted for 1-based index, as you requested
    if token:
        if 1 <= mode <= 7:  # Ensure the mode is between 1 and 7
            current_modes[position - 1] = mode  # Adjust for 1-based index
            await ctx.send(f"Mode for token at position {position} changed to {mode}.")
        else:
            await ctx.send("Invalid mode! Please enter a mode between 1 and 7.")
    else:
        await ctx.send("Invalid position! Please provide a position between 1 and the number of tokens.")        
@bot.command()
async def m(ctx, channel_id: int, position: int):
    """Start sending messages using the token at the specified position in the given channel."""
    token = get_token_by_position(position - 1)  # Adjusted for 1-based index, as you requested
    if token:
        channel = await bot.fetch_channel(channel_id)  # Fetch the channel by ID
        send_messages[position - 1] = True  # Enable message sending for the specified token
        message_count[position - 1] = 0  # Reset message count for this token
        current_modes[position - 1] = 1  # Default to mode 1 for this token

        client = MessageBot(token, channel_id, position - 1)
        await client.start(token, bot=False)
    else:
        await ctx.send(f"No token found at position {position}.")      
@bot.command()
async def me(ctx, position: int):
    """Stop sending messages using the token at the specified position."""
    token = get_token_by_position(position - 1)  # Adjusted for 1-based index, as you requested
    if token:
        send_messages[position - 1] = False  # Stop message sending for the specified token
        await ctx.send(f"Stopped sending messages for token at position {position}.")
    else:
        await ctx.send("Invalid position! Please provide a position between 1 and the number of tokens.")        
        


# Global variables
current_modes_200 = {}
message_count_200 = {}
jokes_200 = []  # Load jokes from jokes.txt
image_links_200 = {}  # Image links for each token
user_react_dict_200 = {}  # User IDs to ping for each token
delays_200 = {}  # Delay per token
send_messages_200 = {}  # To keep track of sending state

# Load jokes from jokes.txt
def load_jokes():
    with open('jokes.txt', 'r') as file:
        jokes = file.readlines()
    return [joke.strip() for joke in jokes]

jokes_200 = load_jokes()

def read_tokens(filename='tokens2.txt'):
    """Read tokens from a file and return them as a list."""
    with open(filename, 'r') as file:
        tokens = file.read().splitlines()
    return tokens

def get_token_by_position(position):
    """Retrieve a token by its position (1-based index)."""
    tokens = read_tokens()
    if 1 <= position <= len(tokens):
        return tokens[position - 1]
    return None


            
class MessageBot200(discord.Client):
    def __init__(self, token, channel_id, position, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.token = token
        self.channel_id = channel_id
        self.position = position

    async def on_ready(self):
        print(f'Logged in as {self.user} using token {self.token[-4:]}.')
        await self.send_messages()

    async def send_messages(self):
        global message_count_200
        channel = self.get_channel(self.channel_id) or await self.fetch_channel(self.channel_id)

        while send_messages_200.get(self.position, False):  # Check if the token is allowed to send messages
            message_count_200[self.position] = message_count_200.get(self.position, 0) + 1

            # Check if message count exceeds 7
            if message_count_200[self.position] > 7:
                message_count_200[self.position] = 0  # Reset message count

            # Select a random joke
            joke = random.choice(jokes_200)
            words = joke.split()
            ping_user = user_react_dict_200.get(self.position, None)
            image_link = image_links_200.get(self.position, None)

            await self.simulate_typing(channel)

            mode = current_modes_200.get(self.position, 1)  # Default to mode 1 if not set
            delay = delays_200.get(self.position, 0.2)  # Default delay is 0.2 if not set

            # Debugging log to show the message being sent
            print(f"Sending message with token {self.position + 1}: {joke}")

            if mode == 1:  # Normal mode: Just sends joke (with ping/image if applicable)
                msg = joke
                if ping_user:
                    msg += f" <@{ping_user}>"
                if image_link:
                    msg += f" {image_link}"
                await channel.send(msg)
                await asyncio.sleep(delay)

            elif mode == 2:  # Header mode: Adds # before the joke
                msg = f"# {joke}"
                if ping_user:
                    msg += f" <@{ping_user}>"
                if image_link:
                    msg += f" {image_link}"
                await channel.send(msg)
                await asyncio.sleep(delay)

            elif mode == 3:  # > # mode: Adds > # before the joke
                msg = f"> # {joke}"
                if ping_user:
                    msg += f" <@{ping_user}>"
                if image_link:
                    msg += f" {image_link}"
                await channel.send(msg)
                await asyncio.sleep(delay)

    async def simulate_typing(self, channel):
        """Simulate typing before sending a message."""
        async with channel.typing():
            await asyncio.sleep(random.uniform(1, 3))  # Simulate typing for a random time

@bot.command()
async def asma(ctx, mode: int):
    """Set the mode for all tokens."""
    if mode in [1, 2, 3]:
        for position in range(len(read_tokens())):
            current_modes_200[position] = mode
        await ctx.send(f"All tokens have been set to mode {mode}.")
    else:
        await ctx.send("Invalid mode. Please choose 1, 2, or 3.")
# Changes in the als command
@bot.command()
async def als(ctx, channel_id: int):
    """Start sending messages using the tokens in the specified channel."""
    global send_messages_200
    send_messages_200.clear()  # Clear previous session data
    
    tokens = read_tokens()  # Read tokens from tokens2.txt
    tasks = []  # A list to hold all tasks

    for position, token in enumerate(tokens):
        send_messages_200[position] = True  # Enable message sending for this token
        message_count_200[position] = 0  # Reset message count
        current_modes_200[position] = 1  # Default to mode 1 for each token
        delays_200[position] = 0.2  # Default delay for each token

        # Create a new MessageBot200 instance for each token and start it
        client = MessageBot200(token, channel_id, position)
        tasks.append(client.start(token, bot=False))  # Start the bot for this token

    # Wait for all tokens to start sending messages
    await asyncio.gather(*tasks)  
    await ctx.send(f"Started sending messages in channel {channel_id} with {len(tokens)} tokens.")
@bot.command()
async def asp(ctx, position: int, user_id: int):
    """Set ping for the specified token."""
    if 1 <= position <= len(read_tokens()):
        user_react_dict_200[position - 1] = user_id
        await ctx.send(f"Token at position {position} will now ping user <@{user_id}> at the end of messages.")
    else:
        await ctx.send(f"Invalid position. Please provide a position between 1 and {len(read_tokens())}.")

@bot.command()
async def aspa(ctx, user_id: int):
    """Set ping for all tokens."""
    for position in range(len(read_tokens())):
        user_react_dict_200[position] = user_id
    await ctx.send(f"All tokens will now ping user <@{user_id}> at the end of messages.")

@bot.command()
async def asi(ctx, position: int, image_url: str):
    """Set the image link for the specified token."""
    if 1 <= position <= len(read_tokens()):
        image_links_200[position - 1] = image_url
        await ctx.send(f"Image link set for token at position {position}.")
    else:
        await ctx.send(f"Invalid position. Please provide a position between 1 and {len(read_tokens())}.")

@bot.command()
async def asia(ctx, image_url: str):
    """Set the image link for all tokens."""
    for position in range(len(read_tokens())):
        image_links_200[position] = image_url
    await ctx.send("Image link set for all tokens.")

@bot.command()
async def asm(ctx, position: int, mode: int):
    """Set the mode for the specified token."""
    if 1 <= position <= len(read_tokens()):
        if mode in [1, 2, 3]:
            current_modes_200[position - 1] = mode
            await ctx.send(f"Mode for token at position {position} changed to {mode}.")
        else:
            await ctx.send("Invalid mode. Please choose 1, 2, or 3.")
    else:
        await ctx.send(f"Invalid position. Please provide a position between 1 and {len(read_tokens())}.")
# Commands for changing delay
@bot.command()
async def asd(ctx, position: int, delay: float):
    """Set the delay for a specific token."""
    if 1 <= position <= len(read_tokens()):
        delays_200[position - 1] = delay  # Set the delay for the specified token
        await ctx.send(f"Delay for token at position {position} set to {delay} seconds.")
    else:
        await ctx.send(f"Invalid position. Please provide a position between 1 and {len(read_tokens())}.")

@bot.command()
async def asda(ctx, delay: float):
    """Set the delay for all tokens."""
    for position in range(len(read_tokens())):
        delays_200[position] = delay  # Set the delay for all tokens
    await ctx.send(f"Delay for all tokens set to {delay} seconds.")
@bot.command()
async def ase(ctx):
    """Stop the sending of messages."""
    global send_messages_200
    send_messages_200.clear()  # Stop all tokens from sending messages
    await ctx.send("Message sending process has been stopped.")
    
    
killloop = asyncio.Event()

REQUEST_DELAY = 0.2
MAX_REQUESTS_BEFORE_SWITCH = 7

def load_file(file_path):
    """Helper function to load a file into a list."""
    with open(file_path, "r") as file:
        return [line.strip() for line in file if line.strip()]

def load_tokens():
    return load_file("tokens2.txt")  # Load tokens from tokens2.txt

def load_packs():
    return load_file("jokes.txt")

def log_action(message, channel=None):
    """Log formatted message to the console with timestamp and location type."""
    timestamp = datetime.now().strftime('%H:%M:%S')
    location = "Start"
    if channel:
        if isinstance(channel, discord.DMChannel):
            location = "DM"
        elif isinstance(channel, discord.TextChannel):
            location = "CH"
        elif isinstance(channel, discord.GroupChannel):
            location = "GC"
    
    print(f"{timestamp} - in {location}: {message}")

async def manage_outlaster(channel_id, user_id, name=None):  # Add name parameter
    """Main function for sending messages using tokens and handling rate limits."""
    tokens = load_tokens()
    messages = load_packs()
    if not tokens or not messages:
        log_action("Missing tokens or message packs.", client.get_channel(channel_id))
        return

    log_action("Starting outlaster message sending...", bot.get_channel(channel_id))
    current_value = message_count = token_index = 0
    while not killloop.is_set() and tokens:
        if token_index >= len(tokens):
            token_index = 0

        token = tokens[token_index]
        headers = {"Authorization": f"{token}"}
        joke = random.choice(messages)  # Select a random joke
        # Append name to the joke if provided
        if name:
            joke += f" {name}"

        json_data = {"content": f"{joke} <@{user_id}> \n ```{current_value}```"}
        url = f"https://discord.com/api/v9/channels/{channel_id}/messages"

        response = requests.post(url, headers=headers, json=json_data)
        if response.status_code == 200:  # Message sent successfully
            log_action(f"Message sent with token {token_index + 1}", bot.get_channel(channel_id))
            message_count += 1
            current_value += 1
            await asyncio.sleep(REQUEST_DELAY)

            if message_count >= MAX_REQUESTS_BEFORE_SWITCH:  # Check if we need to switch tokens
                message_count = 0
                token_index += 1
        elif response.status_code == 429:  # Rate limited
            log_action("Rate limited; retrying...", bot.get_channel(channel_id))
            await asyncio.sleep(20)
        elif response.status_code == 403:  # Invalid token
            log_action(f"Invalid token {token_index + 1}; removing from list.", bot.get_channel(channel_id))
            tokens.pop(token_index)
        else:  # Other errors
            log_action(f"Error: HTTP {response.status_code}; retrying with next token.", bot.get_channel(channel_id))
            token_index += 1

    log_action("Outlaster message sending stopped.", bot.get_channel(channel_id))

def start_outlaster_thread(channel_id, user_id, name=None):  # Add name parameter
    threading.Thread(target=asyncio.run, args=(manage_outlaster(channel_id, user_id, name),)).start()

@bot.command()
async def kill(ctx, user: discord.User, channel_id: int, *, name: str = None):  # name is now optional
    await ctx.message.delete()  # Delete the command message
    killloop.clear()  # Clear any existing kill loops
    start_outlaster_thread(channel_id, user.id, name)  # Start the outlaster thread with the name

    # Send a confirmation message
    if name:
        await ctx.send(f"Outlaster started for {user.mention} with name '{name}'.", delete_after=5)
    else:
        await ctx.send(f"Outlaster started for {user.mention}.", delete_after=5)
@bot.command()
async def kille(ctx):
    await ctx.message.delete()
    killloop.set()
    await ctx.send("Outlaster stopped.", delete_after=5)


# Global variables
reply_mode = 1
tracked_user_id = None
replying = False
jokes = load_jokes()
logging_enabled = False
log_file = "logs.txt"
message_log = []
last_message_time = {}  # Store the last message time for each tracked user
mode_6_active = False  # Track if mode 6 is active
last_mode_6_response_time = {}  
gcfill_cog = GCFill(bot)
bot.add_cog(gcfill_cog)



# Constants and initializations
DISCORD_API_URL_SINGLE = "https://discord.com/api/v9/users/@me/settings"
status_delay900 = {}  # Delay per token position
active_clients900 = {}  # Active clients per token position
status_lists900 = {}  # Status lists per token position

class MultiStatusClient900(discord.Client):
    def __init__(self, token, position, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.token900 = token
        self.position900 = position
        self.running900 = True  # Control loop for rotation

    async def update_status900(self, status_text):
        """Update the custom status."""
        change_single_custom_status(self.token900, status_text)

    async def rotate_statuses900(self):
        """Rotate through the statuses for this token indefinitely."""
        global status_delay900, status_lists900
        while self.running900:
            statuses = status_lists900.get(self.position900, [])
            delay = status_delay900.get(self.position900, 4)  # Default delay is 4 seconds
            for status in statuses:
                if not self.running900:
                    break
                await self.update_status900(status)
                await asyncio.sleep(delay)

    async def on_ready(self):
        print(f'Logged in as {self.user} with token ending in {self.token900[-4:]}')
        asyncio.create_task(self.rotate_statuses900())

    async def stop_rotation(self):
        """Stop the status rotation loop."""
        self.running900 = False
        await self.close()

def change_single_custom_status(token, status_text):
    """Send a request to Discord to update the custom status for the token."""
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    payload = {
        "custom_status": {
            "text": status_text
        }
    }
    try:
        response = requests.patch(DISCORD_API_URL_SINGLE, headers=headers, json=payload)
        if response.status_code == 200:
            print(f"Successfully changed status to '{status_text}' for token ending in {token[-4:]}")
        else:
            print(f"Failed to change status. Status Code: {response.status_code}, Response: {response.text}")
    except requests.RequestException as e:
        print(f"Error while changing status for token ending in {token[-4:]}: {e}")

async def start_client_with_rotation900(token, position, statuses):
    """Log in the specified token and start rotating statuses for it."""
    global status_lists900, active_clients900
    status_lists900[position] = statuses  # Set status list for this token

    client = MultiStatusClient900(token, position, intents=discord.Intents.default())
    active_clients900[position] = client
    await client.start(token, bot=False)  # Start client
    
@bot.command()
async def s(ctx, position: int, *, statuses: str):
    """Set and start rotating the status for a specific token."""
    global active_clients900, status_lists900

    # Load tokens from a file
    tokens = read_tokens('tokens2.txt')

    # Check if position is valid (1-based index)
    if position < 1 or position > len(tokens):
        await ctx.send("Invalid position. Please provide a valid token position.")
        return

    # Parse and set the statuses
    statuses_list = [status.strip() for status in statuses.split(',')]
    token = tokens[position - 1]  # Adjust for 1-based index

    # Stop any existing client for this token if already running
    if position in active_clients900:
        await active_clients900[position].stop_rotation()
        del active_clients900[position]

    # Start new client with the specified statuses
    await start_client_with_rotation900(token, position, statuses_list)
    await ctx.send(f"Started rotating statuses for token {position}.")

@bot.command()
async def se(ctx, position: int):
    """Stop rotating statuses for a specific token."""
    global active_clients900

    # Check if client for this token position is active (1-based index)
    if position in active_clients900:
        await active_clients900[position].stop_rotation()
        del active_clients900[position]
        await ctx.send(f"Stopped rotating statuses for token {position}.")
    else:
        await ctx.send(f"No active status rotation found for token {position}.")

@bot.command()
async def sd(ctx, position: int, delay: int):
    """Change the delay between status updates for a specific token."""
    global status_delay900

    if delay > 0:
        status_delay900[position] = delay  # Set delay for this token (1-based index)
        await ctx.send(f"Status delay for token {position} changed to {delay} seconds.")
    else:
        await ctx.send("Delay must be a positive integer.")

def read_tokens(filename='tokens2.txt'):
    """Read tokens from a file."""
    with open(filename, 'r') as file:
        tokens = file.read().splitlines()
    return tokens


# Global variables with '300' added
streaming_status_delay300 = {}  # Delay per token position
active_clients300 = {}  # Active clients per token position
streaming_status_lists300 = {}  # Status lists per token position

class MultiStreamClient300(discord.Client):
    def __init__(self, token, position, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.token300 = token
        self.position300 = position
        self.running = True  # Control loop for rotation

    async def update_presence300(self, details):
        """Update the custom streaming presence."""
        activity = discord.Streaming(
            name=details,
            url='https://www.twitch.tv/yourchannel'  # Replace with your channel URL
        )
        await self.change_presence(activity=activity)

    async def rotate_statuses300(self):
        """Rotate through the streaming statuses for this token indefinitely."""
        global streaming_status_delay300, streaming_status_lists300
        while self.running:
            statuses = streaming_status_lists300.get(self.position300, [])
            delay = streaming_status_delay300.get(self.position300, 3)
            for status in statuses:
                if not self.running:
                    break
                await self.update_presence300(status)
                await asyncio.sleep(delay)

    async def on_ready(self):
        print(f'Logged in as {self.user} with token {self.token300[-4:]}')
        asyncio.create_task(self.rotate_statuses300())

    async def stop_rotation(self):
        """Stop the status rotation loop."""
        self.running = False
        await self.close()

async def start_client_with_rotation300(token, position, statuses):
    """Log in the specified token and start rotating statuses for it."""
    global streaming_status_lists300, active_clients300
    streaming_status_lists300[position] = statuses  # Set status list for this token

    client = MultiStreamClient300(token, position, intents=intents)
    active_clients300[position] = client
    await client.start(token, bot=False)  # Start client

@bot.command()
async def ss(ctx, position: int, *, statuses: str):
    """Set and start rotating the stream status for a specific token."""
    global active_clients300, streaming_status_lists300

    # Load tokens from a file
    tokens = read_tokens('tokens2.txt')

    # Check if position is valid (1-based index)
    if position < 1 or position > len(tokens):
        await ctx.send("Invalid position. Please provide a valid token position.")
        return

    # Parse and set the statuses
    statuses_list = [status.strip() for status in statuses.split(',')]
    token = tokens[position - 1]  # Adjust for 1-based index

    # Stop any existing client for this token if already running
    if position in active_clients300:
        await active_clients300[position].stop_rotation()
        del active_clients300[position]

    # Start new client with the specified statuses
    await start_client_with_rotation300(token, position, statuses_list)
    await ctx.send(f"Started rotating streaming statuses for token {position}.")

@bot.command()
async def sse(ctx, position: int):
    """Stop rotating streaming statuses for a specific token."""
    global active_clients300

    # Check if client for this token position is active (1-based index)
    if position in active_clients300:
        await active_clients300[position].stop_rotation()
        del active_clients300[position]
        await ctx.send(f"Stopped rotating streaming statuses for token {position}.")
    else:
        await ctx.send(f"No active status rotation found for token {position}.")

@bot.command()
async def ssd(ctx, position: int, delay: int):
    """Change the delay between streaming status updates for a specific token."""
    global streaming_status_delay300

    if delay > 0:
        streaming_status_delay300[position] = delay  # Set delay for this token (1-based index)
        await ctx.send(f"Streaming status delay for token {position} changed to {delay} seconds.")
    else:
        await ctx.send("Delay must be a positive integer.")

@bot.command()
async def ssa(ctx, *, statuses: str):
    """Start rotating streaming statuses for all tokens."""
    global active_clients300

    # Load tokens from a file
    tokens = read_tokens('tokens2.txt')
    statuses_list = [status.strip() for status in statuses.split(',')]

    # Stop any existing clients
    for position, client in active_clients300.items():
        await client.stop_rotation()
    active_clients300.clear()

    # Start new clients with specified statuses
    for i, token in enumerate(tokens, start=1):  # 1-based index
        await start_client_with_rotation300(token, i, statuses_list)

    await ctx.send("Started rotating streaming statuses for all tokens.")

@bot.command()
async def ssae(ctx):
    """Stop rotating streaming statuses for all tokens."""
    global active_clients300

    # Stop all active clients
    for client in active_clients300.values():
        await client.stop_rotation()
    active_clients300.clear()

    await ctx.send("Stopped rotating streaming statuses for all tokens.")

@bot.command()
async def ssda(ctx, delay: int):
    """Change the delay between streaming status updates for all tokens."""
    global streaming_status_delay300

    if delay > 0:
        # Set delay for all token positions
        for position in active_clients300.keys():
            streaming_status_delay300[position] = delay
        await ctx.send(f"Streaming status delay for all tokens changed to {delay} seconds.")
    else:
        await ctx.send("Delay must be a positive integer.")

def read_tokens(filename='tokens2.txt'):
    """Read tokens from a file."""
    with open(filename, 'r') as file:
        tokens = file.read().splitlines()
    return tokens
@bot.command(name='gcf')
async def gcf(ctx):
    """Enable the GC fill listener."""
    gcfill_cog.enabled = True
    gcfill_cog.start_auto_adder()
    await ctx.send("GC fill listener enabled.")

@bot.command(name='gcfe')
async def gcfe(ctx):
    """Disable the GC fill listener."""
    gcfill_cog.enabled = False
    gcfill_cog.stop_auto_adder()
    await ctx.send("GC fill listener disabled.")

@bot.command(name='uid')
async def add_uid(ctx, user_id: str):
    """Add a user ID to gcfill.txt."""
    try:
        with open('gcfill.txt', 'a') as file:
            file.write(f"\n{user_id}\n")
        await ctx.send(f"User ID {user_id} added to gcfill.txt.")
    except Exception as e:
        await ctx.send(f"An error occurred while adding the user ID: {e}")

# Message Logger
@bot.command()
async def log(ctx, option):
    global logging_enabled
    if option == "on":
        logging_enabled = True
        await ctx.send("Logging for DMs and GCs has been turned ON.")
    elif option == "off":
        logging_enabled = False
        await ctx.send("Logging for DMs and GCs has been turned OFF.")
    else:
        await ctx.send("Invalid option! Use `log on` or `log off`.")

# Log deleted messages
@bot.event
async def on_message_delete(message):
    global logging_enabled

    # Log only in DMs and GCs
    if logging_enabled and (isinstance(message.channel, discord.DMChannel) or isinstance(message.channel, discord.GroupChannel)):
        log_entry = f"Message {len(message_log) + 1}: A message was deleted by {message.author} in {message.channel.name if message.guild else 'DM/GC'}\n"

        if message.content:
            log_entry += f"Content: {message.content}\n"

        if message.attachments:
            for attachment in message.attachments:
                log_entry += f"Attachment: {attachment.url}\n"

        message_log.append(log_entry)

        with open(log_file, "a") as f:
            f.write(log_entry)

        print(f"Logged: {log_entry.strip()}")

# Display the deleted message
@bot.command()
async def display(ctx, number: int):
    if 0 < number <= len(message_log):
        await ctx.send(message_log[number - 1])
    else:
        await ctx.send(f"No log found for number {number}. Check the range.")

# display the entire log file
@bot.command()
async def displaylog(ctx):
    if os.path.exists(log_file):
        with open(log_file, "r") as f:
            log_content = f.read()
        if log_content:
            await ctx.send(f"```{log_content}```")
        else:
            await ctx.send("The log is empty.")
    else:
        await ctx.send("Log file does not exist.")

# clear the log file
@bot.command()
async def clearlog(ctx):
    if os.path.exists(log_file):
        os.remove(log_file)
        message_log.clear()
        await ctx.send("Logs have been cleared.")
    else:
        await ctx.send("Log file does not exist.")

# Purge In Dms Or Group Chat
@bot.command()
async def purge(ctx, num: int = None):
    """Purges a specified number of messages, including old ones, in DMs and Group Chats."""

    # Check if the command is used in DMs or a Group Chat
    if isinstance(ctx.channel, discord.DMChannel) or isinstance(ctx.channel, discord.GroupChannel):

        if num is not None and num < 1:
            await ctx.send("Please specify a number greater than 0.")
            return

        deleted_count = 0  # Track how many messages have been deleted

        # If num is None, delete as many messages as possible with a 0.5-second delay
        if num is None:
            # Fetch all messages in the channel (limit to 1000 to avoid overload)
            async for message in ctx.channel.history(limit=1000):
                try:
                    # Check if the message is sent by the user (bot/self-bot), skip if not
                    if message.author == bot.user or message.author == ctx.author:
                        await message.delete()
                        deleted_count += 1
                        await asyncio.sleep(0.01)  # 0.5 seconds delay between each delete
                except discord.Forbidden:
                    await ctx.send("I don't have permission to delete messages here.")
                    return
                except discord.HTTPException:
                    # Stop if we hit rate limits or any other errors
                    await ctx.send(f"Stopped after deleting {deleted_count} messages due to an error.")
                    return

        else:
            # Fetch the specified number of messages
            async for message in ctx.channel.history(limit=num):
                try:
                    # Only delete messages from the bot/user, skip others
                    if message.author == bot.user or message.author == ctx.author:
                        await message.delete()
                        deleted_count += 1
                        await asyncio.sleep(0.05)  # 0.5 seconds delay between each delete
                except discord.Forbidden:
                    await ctx.send("I don't have permission to delete messages here.")
                    return
                except discord.HTTPException:
                    # Stop if we hit rate limits or any other errors
                    await ctx.send(f"Stopped after deleting {deleted_count} messages due to an error.")
                    return

        # Inform the user about the successful deletion
        await ctx.send(f"Successfully deleted {deleted_count} message(s).")

    else:
        await ctx.send("This command can only be used in DMs or Group Chats.")



@bot.event
async def on_ready():
    global alw_handler
    print(f"Logged in as {bot.user}")
    alw_handler = ALWHandler(bot)  # Initialize the ALWHandler
    print("ALWHandler initialized.")


# Hardcoded emojis
emojis = [ '\<a:WF:1280996198890864680>', '\<a:zwhiteverified:1261879185371172886>', '\<a:0blackxwhiteflash:1293641546503163905>', '\<a:black_lightning:1281422609443192883>', '\<a:BCross:1281816486633144351>', '\<a:Crown_Black:1270933813018497064>', '\<a:black_cross:1214004562537488454>', '\<a:nux_cross1:1258357351535083581>', '\<:whitevampirefangs:1304085056880382072>', '\<a:whitegrown_DIOR:1151090822113148971>', '\<a:1whitecustomgif:1277651799100096595>', '\<a:1104884088843817104:1300009218212102145>'      ]
current_index = 0
reacting = False

@bot.command()
async def re(ctx):
    global reacting, current_index
    reacting = True
    current_index = 0
    await ctx.send(f"Started reacting with emojis: {', '.join(emojis)}")

@bot.command()
async def ree(ctx):
    global reacting
    reacting = False
    await ctx.send("Stopped reacting to messages.")

import re
afk_responded = set()  # Track users who have received a response to prevent further responses
afk_watchers = {}
last_messages = {}  # Initialize the last_messages dictionary
waiting_for_response = {}
def calculate_delay(response: str, wpm: int = 120) -> float:
    word_count = len(response.split())
    delay_per_word = 60 / wpm
    total_delay = word_count * delay_per_word
    return total_delay

@bot.command()
async def afk(ctx, user: discord.User):
    if user.id not in afk_watchers:
        afk_watchers[user.id] = True
        await ctx.message.delete()
        await ctx.send(f"Started monitoring {user.mention} for AFK checks.", delete_after=5)
    else:
        await ctx.send(f"{user.mention} is already being monitored.", delete_after=5)

@bot.command()
async def afke(ctx, user: discord.User):
    if user.id in afk_watchers:
        del afk_watchers[user.id]
        await ctx.message.delete()
        await ctx.send(f"Stopped monitoring {user.mention} for AFK checks.", delete_after=2)
    else:
        await ctx.send(f"{user.mention} is not being monitored.", delete_after=5)

        
        
        
        
@bot.event
async def on_message(message):
    global reacting, current_index, waiting_for_response, afk_responded

    if message.author.id in afk_watchers:
        # Check for 'check' at the end of the message
        if message.content.lower().endswith("check"):
            delay = calculate_delay("here")
            await asyncio.sleep(delay)
            async with message.channel.typing():
                await asyncio.sleep(random.uniform(0.9, 1.5))
                await message.channel.send("here")
            return

        # If the message ends with 'say', listen for the next message
        if message.content.lower().endswith("say"):
            waiting_for_response[message.author.id] = True
            return  # Wait for a second message

        # Handle first message if it starts with "say"
        if message.content.lower().startswith("say "):
            match = re.search(r'\bsay\s+(.+)', message.content.lower())
            if match:
                response = match.group(1).strip()
                response = re.sub(r'<@!?[0-9]+>', '', response).strip()  # Remove user mentions

                # Replace standalone 'I' followed by 'M' (both standalone) with 'ur'
                response = re.sub(r'\bi\b\s+m\b', 'ur', response, flags=re.IGNORECASE)

                # Replace standalone 'M' with 'r'
                response = re.sub(r'\b(m)\b', 'r', response, flags=re.IGNORECASE)

                # Replace "I am a" with "ur a"
                response = re.sub(r'\b(i am a)\s*(.+)', r'ur a \2', response, flags=re.IGNORECASE)

                # Replace standalone 'I' followed by apostrophe with 'ur'
                response = re.sub(r'\bi\'m\b', 'ur', response, flags=re.IGNORECASE)

                # Replace other variations with "ur"
                response = re.sub(r'\b(im|my|i\'m|i m|im a|i\'m a|I am a)\s*(.+)', r"ur \2", response, flags=re.IGNORECASE)
                response = re.sub(r'\b(im|my|i\'m|i m)\s*(.+)', r"ur \2", response, flags=re.IGNORECASE)

                # Replace standalone 'I' with 'u'
                response = re.sub(r'\bi\b', 'u', response, flags=re.IGNORECASE)

                # Special cases with variations
                if any(phrase in response.lower() for phrase in ["ur my god", "you’re my god", "you are my god", "ur my god", "youre my god"]):
                    response = "im ur god"
                elif any(phrase in response.lower() for phrase in ["u own me", "you own me"]):
                    response = "i own you"
                elif any(phrase in response.lower() for phrase in ["im ur slut", "ur my slut", "youre my slut", "you are my slut", "u are my slut"]):
                    response = "ur my slut"
                elif any(phrase in response.lower() for phrase in ["im ur bitch", "ur my bitch", "youre my bitch", "you are my bitch", "u are my bitch"]):
                    response = "ur my bitch"

                # Send response
                delay = calculate_delay(response)
                await asyncio.sleep(delay)

                # Simulate typing
                typing_delay = random.uniform(0.9, 1.5)
                async with message.channel.typing():
                    await asyncio.sleep(typing_delay)
                    await message.channel.send(response)
                return  # Prevent further processing

        # Handle cases where the message starts with 'afk', 'bot', or 'client' and includes 'say'
        if (message.content.lower().startswith("afk") or 
            message.content.lower().startswith("bot") or 
            message.content.lower().startswith("client")) and "say" in message.content.lower():
            match = re.search(r'\bsay\s+(.+)', message.content.lower())
            if match:
                response = match.group(1).strip()
                response = re.sub(r'<@!?[0-9]+>', '', response).strip()  # Remove user mentions

                # Replace standalone 'I' followed by 'M' (both standalone) with 'ur'
                response = re.sub(r'\bi\b\s+m\b', 'ur', response, flags=re.IGNORECASE)

                # Replace standalone 'M' with 'r'
                response = re.sub(r'\b(m)\b', 'r', response, flags=re.IGNORECASE)

                # Replace "I am a" with "ur a"
                response = re.sub(r'\b(i am a)\s*(.+)', r'ur a \2', response, flags=re.IGNORECASE)

                # Replace standalone 'I' followed by apostrophe with 'ur'
                response = re.sub(r'\bi\'m\b', 'ur', response, flags=re.IGNORECASE)

                # Replace other variations with "ur"
                response = re.sub(r'\b(im|my|i\'m|i m|im a|my|i\'m a|I am a)\s*(.+)', r"ur \2", response, flags=re.IGNORECASE)
                response = re.sub(r'\b(im|my|i\'m|i m)\s*(.+)', r"ur \2", response, flags=re.IGNORECASE)

                # Replace standalone 'I' with 'u'
                response = re.sub(r'\bi\b', 'u', response, flags=re.IGNORECASE)

                # Special cases with variations
                if any(phrase in response.lower() for phrase in ["ur my god", "you’re my god", "you are my god", "ur my god", "youre my god"]):
                    response = "im ur god"
                elif any(phrase in response.lower() for phrase in ["u own me", "you own me"]):
                    response = "i own you"
                elif any(phrase in response.lower() for phrase in ["im ur slut", "ur my slut", "youre my slut", "you are my slut", "u are my slut"]):
                    response = "ur my slut"
                elif any(phrase in response.lower() for phrase in ["im ur bitch", "ur my bitch", "youre my bitch", "you are my bitch", "u are my bitch"]):
                    response = "ur my bitch"

                # Send response
                delay = calculate_delay(response)
                await asyncio.sleep(delay)

                # Simulate typing
                typing_delay = random.uniform(0.9, 1.5)
                async with message.channel.typing():
                    await asyncio.sleep(typing_delay)
                    await message.channel.send(response)
                return  # Prevent further processing

    # Check for a second message if the user is waiting for a response
    if message.author.id in waiting_for_response and waiting_for_response[message.author.id]:
        response = message.content.strip()
        response = re.sub(r'<@!?[0-9]+>', '', response).strip()  # Remove user mentions

        # Replace standalone 'I' followed by 'M' (both standalone) with 'ur'
        response = re.sub(r'\bi\b\s+m\b', 'ur', response, flags=re.IGNORECASE)

        # Replace standalone 'M' with 'r'
        response = re.sub(r'\b(m)\b', 'r', response, flags=re.IGNORECASE)

        # Replace "I am a" with "ur a"
        response = re.sub(r'\b(i am a)\s*(.+)', r'ur a \2', response, flags=re.IGNORECASE)

        # Replace standalone 'I' followed by apostrophe with 'ur'
        response = re.sub(r'\bi\'m\b', 'ur', response, flags=re.IGNORECASE)

        # Replace other variations with "ur"
        response = re.sub(r'\b(im|my|i\'m|i m|im a|i\'m a|I am a)\s*(.+)', r"ur \2", response, flags=re.IGNORECASE)
        response = re.sub(r'\b(im|my|i\'m|i m)\s*(.+)', r"ur \2", response, flags=re.IGNORECASE)

        # Replace standalone 'I' with 'u'
        response = re.sub(r'\bi\b', 'u', response, flags=re.IGNORECASE)

        # Special cases with variations
        if any(phrase in response.lower() for phrase in ["ur my god", "you’re my god", "you are my god", "ur my god", "youre my god"]):
            response = "im ur god"
        elif any(phrase in response.lower() for phrase in ["u own me", "you own me"]):
            response = "i own you"
        elif any(phrase in response.lower() for phrase in ["im ur slut", "ur my slut", "youre my slut", "you are my slut", "u are my slut"]):
            response = "ur my slut"
        elif any(phrase in response.lower() for phrase in ["im ur bitch", "ur my bitch", "youre my bitch", "you are my bitch", "u are my bitch"]):
            response = "ur my bitch"

        # Send the response for the second message
        delay = calculate_delay(response)
        await asyncio.sleep(delay)

        # Simulate typing
        typing_delay = random.uniform(0.9, 1.5)
        async with message.channel.typing():
            await asyncio.sleep(typing_delay)
            await message.channel.send(response)

        del waiting_for_response[message.author.id]  # Clear the waiting state after responding
        return  # Prevent further processing

    # Reacting functionality
    if reacting and message.author.id == 942244824411689000:  # Check for specific user ID
        try:
            # React with the emoji at the current index
            await message.add_reaction(emojis[current_index])
            # Update index for the next emoji
            current_index = (current_index + 1) % len(emojis)  # Rotate through emojis
        except Exception as e:
            print(f"Error adding reaction: {e}")

    # If alw_handler is defined, call its on_message method
    if alw_handler is not None:
        await alw_handler.on_message(message)

    # Process commands after handling the message
    await bot.process_commands(message)
@bot.command()
async def alw(ctx, option: str):
    global alw_handler
    if alw_handler is None:
        await ctx.send("ALWHandler is not initialized.")
        return

    if option.lower() == "on":
        alw_handler.alw_enabled = True
        alw_handler.uid = str(ctx.author.id)  # Set user ID from context
        await ctx.send("Auto Last Word feature enabled.")
    elif option.lower() == "off":
        alw_handler.alw_enabled = False
        await ctx.send("Auto Last Word feature disabled.")
    else:
        await ctx.send("Invalid option. Use 'on' or 'off'.")   
@bot.command()
async def wl(ctx, user_id: int):
    """Add a user ID to the whitelist."""
    global alw_handler

    if alw_handler is None:
        await ctx.send("ALWHandler is not initialized.")
        return

    # Add user_id to whitelist
    alw_handler.whitelist.add(str(user_id))  # Add to the in-memory set
    alw_handler.save_whitelist()  # Save to file

    await ctx.send(f"User ID {user_id} has been added to the whitelist.")

@bot.command(aliases=["pornhubcomment", 'phc'])
async def phcomment(ctx, user: discord.User = None, *, args=None):
    await ctx.message.delete()
    if user is None or args is None:
        await ctx.send(f'[ERROR]: Invalid input! Command: phcomment <user> <message>')
        return

    avatar_url = user.avatar_url_as(format="png")

    endpoint = f"https://nekobot.xyz/api/imagegen?type=phcomment&text={args}&username={user.name}&image={avatar_url}"
    r = requests.get(endpoint)
    res = r.json()

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(res["message"]) as resp:
                image = await resp.read()
        with io.BytesIO(image) as file:
            await ctx.send(file=discord.File(file, f"{user.name}_pornhub_comment.png"))
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")

@bot.command()
async def tweet(ctx, username: str = None, *, message: str = None):
    await ctx.message.delete()
    if username is None or message is None:
        await ctx.send("missing parameters")
        return
    async with aiohttp.ClientSession() as cs:
        async with cs.get(f"https://nekobot.xyz/api/imagegen?type=tweet&username={username}&text={message}") as r:
            res = await r.json()
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(str(res['message'])) as resp:
                        image = await resp.read()
                with io.BytesIO(image) as file:
                    await ctx.send(file=discord.File(file, f"exeter_tweet.png"))
            except:
                await ctx.send(res['message'])      

# Command to get the avatar of a user
@bot.command()
async def av(ctx, user: discord.User = None):
    try:
        if user is None:  # If no user is provided, get the bot's own avatar
            user = bot.user


        # Check if the user has an avatar
        if user.avatar:
            avatar_url = user.avatar_url
            await ctx.send(f"Avatar URL: {avatar_url}", delete_after=10101010101001010100101111)  # Delete response message after 10101010101001010100101111 seconds
        else:
            await ctx.send(f"{user.name} does not have an avatar.", delete_after=10101010101001010100101111)  # Delete response message after 10101010101001010100101111 seconds


        # Delete the command message itself after 2 seconds
        await asyncio.sleep(2)
        await ctx.message.delete()
    except Exception as e:
        await ctx.send(f"An error occurred: {e}", delete_after=10101010101001010100101111)  # Delete response message after 10101010101001010100101111 seconds







@bot.command()
async def kiss(ctx, user: discord.User):
    await ctx.message.delete()
    r = requests.get("https://nekos.life/api/v2/img/kiss")
    res = r.json()
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(res['url']) as resp:
                image = await resp.read()
        with io.BytesIO(image) as file:
            await ctx.send(user.mention, file=discord.File(file, f"exeter_kiss.gif"))
    except:
        em = discord.Embed(description=user.mention)
        em.set_image(url=res['url'])
        await ctx.send(embed=em)
# Global variables
user_to_ping = {}
current_delay = {}
current_mode = {}
active_clients = {}










def read_tokens(filename='tokens2.txt'):
    """Read tokens from a file."""
    with open(filename, 'r') as file:
        tokens = file.read().splitlines()
    return tokens

running_processes = {}

@bot.command()
async def gct(ctx, channel_id: int, position: int, name: str):
    # Start the gct.py script with the specified position and name
    process = subprocess.Popen(['python', 'gct.py', str(channel_id), str(position), name])

    # Store the process with the position as the key
    running_processes[position] = process

    await ctx.send(f'Started the channel renaming bot in channel ID {channel_id} for token position {position} with name: {name}')

@bot.command()
async def gcte(ctx, position: int):
    # Stop the renaming bot for the specific token at the given position
    if position in running_processes:
        process = running_processes[position]
        process.terminate()  # Terminate the process
        del running_processes[position]  # Remove the process from the dictionary
        await ctx.send(f'Stopped the channel renaming bot for token position {position}.')
    else:
        await ctx.send(f'No renaming bot is running for token position {position}.')

@bot.command()
async def gcta(ctx, channel_id: int, name: str):
    # Start the renaming process for all tokens
    with open("tokens2.txt", "r") as f:
        tokens = f.read().splitlines()

    # Start a process for each token
    for position in range(1, len(tokens) + 1):
        process = subprocess.Popen(['python', 'gct.py', str(channel_id), str(position), name])
        running_processes[position] = process

    await ctx.send(f'Started the channel renaming bot for all tokens in channel ID {channel_id} with name: {name}')

@bot.command()
async def gctae(ctx):
    # Stop all renaming bots for all tokens
    if running_processes:
        for position, process in list(running_processes.items()):
            process.terminate()  # Terminate each process
            del running_processes[position]
        await ctx.send('Stopped all channel renaming bots for all tokens.')
    else:
        await ctx.send('No renaming bots are currently running.')



def load_jokes():
    with open("jokes.txt", "r") as f:
        return f.read().splitlines()

class MultiTokenClient(discord.Client):
    def __init__(self, token, delay, channel_id, user_to_ping=None, mode=1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.token = token
        self.delay = delay
        self.channel_id = channel_id
        self.user_to_ping = user_to_ping
        self.running = True
        self.mode = mode  # Store the mode

    async def on_ready(self):
        print(f'Logged in as {self.user}')
        channel = self.get_channel(self.channel_id)

        while self.running:
            joke = random.choice(load_jokes())  # Load a random joke
            message = self.format_message(joke)
            if message and channel:  # Ensure the channel is valid and message is not None
                try:
                    await channel.send(message)  # Send the joke
                except discord.Forbidden:
                    print(f"Message blocked: {message}")  # Log that the message was blocked
                except Exception as e:
                    print(f"An error occurred: {e}")  # Handle other potential errors
            await asyncio.sleep(self.delay)

def format_message(self, joke):
    # Apply the selected mode to format the joke
    if self.mode == 1:
        # Normal
        return f"{joke} <@{self.user_to_ping}>" if self.user_to_ping else joke
    elif self.mode == 2:
        # 1 new line between words
        formatted_joke = " ".join(joke.split())
        return f"{formatted_joke} <@{self.user_to_ping}>" if self.user_to_ping else '\n'.join(joke.split())
    elif self.mode == 3:
        # Single joke as header multiplied by 20
        repeated_joke = "# " + (joke * 20)
        return f"{repeated_joke} <@{self.user_to_ping}>" if self.user_to_ping else repeated_joke
    elif self.mode == 4:
        # Combine normal, new lines, and header formats
        normal = joke
        new_lines = '\n'.join(joke.split())
        header = f"# {joke} <@{self.user_to_ping}>" if self.user_to_ping else f"# {joke}"
        return f"{normal}\n{new_lines}\n{header}"
    elif self.mode == 5:
        # 100 new lines between words
        formatted_joke = '\n'.join(joke.split())
        if self.user_to_ping:
            return (f"<@{self.user_to_ping}> {formatted_joke}\n") * 100
        else:
            return formatted_joke + ("\n" * 100)
    elif self.mode == 6:
        # Header without multiplying
        header = f"# {joke}"
        return f"{header} <@{self.user_to_ping}>" if self.user_to_ping else header
    elif self.mode == 7:
        # Normal message with random delay
        self.delay = random.uniform(2, 4)  # Random delay between 2 and 4 seconds
        return f"<@{self.user_to_ping}> {joke}" if self.user_to_ping else joke
    elif self.mode == 8:
        # Do not return a message
        return None
    elif self.mode == 9:
        # Appends full invite link
        return f"<@{self.user_to_ping}> {joke}\ndiscord.gg/corpses" if self.user_to_ping else f"{joke}\ndiscord.gg/corpsesodd"
    elif self.mode == 10:
        # Appends just the custom string
        return f"<@{self.user_to_ping}> {joke} /corpses" if self.user_to_ping else f"{joke} /corpses"
    # Fallback to normal
    return joke


@bot.command()
async def ap(ctx, channel_id: int, position: int, delay: float = 4):
    global active_clients

    with open("tokens2.txt", "r") as f:
        tokens = f.read().splitlines()

    if position < 1 or position > len(tokens):
        await ctx.send("Invalid position. Please provide a valid token position.")
        return

    token = tokens[position - 1]  # Adjust for zero-based index

    if token in active_clients:
        active_clients[token].running = False
        await active_clients[token].close()

    client = MultiTokenClient(token, delay, channel_id)
    active_clients[token] = client  # Keep track of the active client
    await client.start(token, bot=False)  # Start the client
    await ctx.send(f'Started sending jokes in <#{channel_id}> every {delay} seconds using token at position {position}.')

@bot.command()
async def ape(ctx, position: int):
    global active_clients

    with open("tokens2.txt", "r") as f:
        tokens = f.read().splitlines()

    if position < 1 or position > len(tokens):
        await ctx.send("Invalid position. Please provide a valid token position.")
        return

    token = tokens[position - 1]  # Adjust for zero-based index

    if token in active_clients:
        active_clients[token].running = False
        await active_clients[token].close()

    await ctx.send(f'Stopped sending jokes for token at position {position}.')

@bot.command()
async def app(ctx, position: int, user_id: int):
    global active_clients

    with open("tokens2.txt", "r") as f:
        tokens = f.read().splitlines()

    if position < 1 or position > len(tokens):
        await ctx.send("Invalid position. Please provide a valid token position.")
        return

    token = tokens[position - 1]  # Adjust for zero-based index

    if token in active_clients:
        active_clients[token].user_to_ping = user_id  # Set the user to ping for this token
        await ctx.send(f'Token at position {position} will now ping <@{user_id}> with each joke.')
    else:
        await ctx.send("Token is not currently active.")

@bot.command()
async def apm(ctx, position: int, mode: int):
    global active_clients

    with open("tokens2.txt", "r") as f:
        tokens = f.read().splitlines()

    if position < 1 or position > len(tokens):
        await ctx.send("Invalid position. Please provide a valid token position.")
        return

    token = tokens[position - 1]  # Adjust for zero-based index

    if token in active_clients:
        active_clients[token].mode = mode  # Update the mode for the active token
        await ctx.send(f'Token at position {position} mode changed to {mode}.')
    else:
        await ctx.send("Token is not currently active.")

@bot.command()
async def apa(ctx, channel_id: int):
    global active_clients

    with open("tokens2.txt", "r") as f:
        tokens = f.read().splitlines()

    async def start_client(token):
        client = MultiTokenClient(token, 4, channel_id)  # Default delay set to 4 seconds
        active_clients[token] = client  # Keep track of the active client
        await client.start(token, bot=False)  # Start the client

    tasks = [start_client(token) for token in tokens]
    await asyncio.gather(*tasks)  # Start all tokens simultaneously

    await ctx.send(f'All tokens are now sending jokes in <#{channel_id}> every 4 seconds.')

@bot.command()
async def apae(ctx):
    global active_clients

    for token, client in active_clients.items():
        client.running = False  # Stop each client
        await client.close()  # Close the client connection

    active_clients.clear()  # Clear the active clients
    await ctx.send('Stopped all active tokens from sending jokes.')

@bot.command()
async def apd(ctx, position: int, delay: float):
    global active_clients

    with open("tokens2.txt", "r") as f:
        tokens = f.read().splitlines()

    if position < 1 or position > len(tokens):
        await ctx.send("Invalid position. Please provide a valid token position.")
        return

    token = tokens[position - 1]  # Adjust for zero-based index

    if token in active_clients:
        active_clients[token].delay = delay  # Update the delay for the active token
        await ctx.send(f'Token at position {position} delay changed to {delay} seconds.')
    else:
        await ctx.send("Token is not currently active.")

@bot.command()
async def apma(ctx, mode: int):
    global active_clients

    for token, client in active_clients.items():
        client.mode = mode  # Update the mode for all active tokens


@bot.command()
async def appa(ctx, user_id: int):
    global active_clients

    for token, client in active_clients.items():
        client.user_to_ping = user_id  # Set the user to ping for all active tokens

@bot.command()
async def apda(ctx, delay: float):
    global active_clients

    for token, client in active_clients.items():
        client.delay = delay  # Update the delay for each active token



@bot.command()
async def tc(ctx):
    valid_tokens = 0
    valid_usernames = set()  # Use a set to avoid duplicates

    # Read tokens from the tokens2.txt file
    with open("tokens2.txt", "r") as f:
        tokens = f.read().splitlines()

    valid_tokens_list = []  # List to keep track of valid tokens

    for token in tokens:
        try:
            # Make a request to get the user info
            headers = {
                "Authorization": token
            }
            response = requests.get("https://discord.com/api/v9/users/@me", headers=headers)

            if response.status_code == 200:  # Valid token
                valid_tokens += 1
                user_info = response.json()
                username = f"{user_info['username']}#{user_info['discriminator']}"
                valid_usernames.add(username)  # Add username to set
                valid_tokens_list.append(token)  # Keep the valid token

            else:  # Invalid token
                # If invalid, do not keep the token
                print(f"Deleting invalid token: {token}")

        except Exception as e:
            print(f"An error occurred: {e}")

    # Write back the valid tokens to the file, removing invalid tokens
    with open("tokens2.txt", "w") as f:
        f.write("\n".join(valid_tokens_list))

    # Construct the result message for valid tokens
    result_message_content = (f"` Valid tokens: {valid_tokens}`\n"
                              f"` Usernames found: {len(valid_usernames)}`")

    # Send the results message
    result_message = await ctx.send(result_message_content)

    # Delete the command message after 0.1 seconds
    await asyncio.sleep(0.1)
    await ctx.message.delete()  # Deletes the command message, not the result message

@bot.command()
async def ul(ctx):
    # Read tokens from tokens2.txt
    with open("tokens2.txt", "r") as f:
        tokens = f.read().splitlines()

    valid_usernames = []

    for token in tokens:
        try:
            # Make a request to get the user info
            headers = {
                "Authorization": token
            }
            response = requests.get("https://discord.com/api/v9/users/@me", headers=headers)

            if response.status_code == 200:  # Valid token
                user_info = response.json()
                username = f"{user_info['username']}#{user_info['discriminator']}"
                valid_usernames.append(username)  # Append username in the order of tokens

        except Exception as e:
            print(f"An error occurred while fetching user info: {e}")

    # Construct the result message in chronological order
    usernames_display = "\n".join(f"{i + 1}. {username}" for i, username in enumerate(valid_usernames)) if valid_usernames else "No valid usernames found."
    result_message_content = (f"`Usernames:\n{usernames_display}`")

    # Send the results message
    await ctx.send(result_message_content)






active_clients_1 = {}
current_mode_1 = {}
user_to_reply = {}
replying = {}
last_message_time = {}
mode_6_active = {}
last_mode_6_response_time = {}

class AutoReplyClient(discord.Client):
    def __init__(self, token, user_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.token = token
        self.user_id = user_id
        self.running = True

    async def on_ready(self):
        print(f'Logged in as {self.user}')

    async def on_message(self, message):
        if message.author.id == self.user_id and not message.author.bot:  # Check if the message is from the user to reply to
            current_time = time.time()
            reply_mode = current_mode_1.get(self.token, 1)  # Default to mode 1 if not set

            # Mode 6 Logic
            if mode_6_active.get(self.token, False):
                # Only respond if 1.5 seconds have passed since the last response to this user
                if message.author.id not in last_mode_6_response_time or (current_time - last_mode_6_response_time[message.author.id] > 1.5):
                    last_mode_6_response_time[message.author.id] = current_time  # Update the last response time
                    await asyncio.sleep(1.5)  # Simulate typing
                    reply_text = random.choice(load_jokes())  # Choose a joke to reply with
                    await message.reply(reply_text)  # Direct reply
                    return  # Exit to prevent processing further messages

            # Update last message time for other modes
            last_message_time[message.id] = current_time

            if reply_mode == 1:
                reply_text = random.choice(load_jokes())  # Normal reply
                await message.reply(reply_text)  # Direct reply
            elif reply_mode == 2:
                joke = random.choice(load_jokes())
                reply_text = "\n" * 100  # 100 empty lines
                reply_text = reply_text.join(joke.split())  # Insert 100 empty lines between words
                await message.reply(reply_text)  # Direct reply
            elif reply_mode == 3:
                reply_text = "\n".join([f"# {word.strip() * 100}" for word in random.choice(load_jokes()).split()])  # Bold reply
                await message.reply(reply_text)  # Direct reply
            elif reply_mode == 4:
                reply_text = random.choice(load_jokes())  # Just send the joke normally
                await asyncio.sleep(1.5)  # Simulate typing
                await message.reply(reply_text)  # Direct reply
            elif reply_mode == 5:
                reply_text = random.choice(load_jokes())  # Send a joke with a ping
                await message.channel.send(f"{reply_text} {message.author.mention}")  # Send with a ping

    def stop_replying(self):
        self.running = False

def load_jokes():
    # Load jokes from jokes.txt
    with open("jokes.txt", "r") as f:
        return f.read().splitlines()  # Return the jokes as a list

@bot.command()
async def ar(ctx, user_id: int, position: int):
    global active_clients_1, current_mode_1, replying

    # Read tokens from tokens2.txt
    with open("tokens2.txt", "r") as f:
        tokens = f.read().splitlines()

    # Check if the position is valid
    if position < 1 or position > len(tokens):
        await ctx.send("Invalid position. Please provide a valid token position.")
        return

    # Get the specified token
    token = tokens[position - 1]  # Adjust for zero-based index

    # Stop any existing client for this token if it's already running
    if token in active_clients_1:
        active_clients_1[token].stop_replying()
        await active_clients_1[token].close()

    # Start the AutoReplyClient for the specified token
    client = AutoReplyClient(token, user_id)
    active_clients_1[token] = client  # Keep track of the active client
    current_mode_1[token] = 1  # Default mode to 1
    user_to_reply[token] = user_id  # Set the user ID to reply to
    replying[token] = True  # Mark as replying
    await client.start(token, bot=False)  # Start the client
    await ctx.send(f'Started auto replying to user <@{user_id}> using token at position {position}.')

@bot.command()
async def are(ctx, position: int):
    global active_clients_1

    # Read tokens from tokens2.txt to maintain the original token order
    with open("tokens2.txt", "r") as f:
        tokens = f.read().splitlines()

    # Check if the position is valid
    if position < 1 or position > len(tokens):
        await ctx.send("Invalid position. Please provide a valid token position.")
        return

    # Get the specified token
    token = tokens[position - 1]  # Get the token at the specified position

    # Stop the active client for the specified token
    if token in active_clients_1:
        active_clients_1[token].stop_replying()
        await active_clients_1[token].close()
        del active_clients_1[token]  # Remove from active clients
        await ctx.send(f'Stopped auto replying for token at position {position}.')
    else:
        await ctx.send("No active client found for this token.")

@bot.command()
async def am(ctx, position: int, mode: int):
    global active_clients_1, current_mode_1

    # Read tokens from tokens2.txt to maintain the original token order
    with open("tokens2.txt", "r") as f:
        tokens = f.read().splitlines()

    # Check if the position is valid
    if position < 1 or position > len(tokens):
        await ctx.send("Invalid position. Please provide a valid token position.")
        return

    # Get the specified token
    token = tokens[position - 1]  # Get the token at the specified position

    # Check if the token is active
    if token in active_clients_1:
        current_mode_1[token] = mode  # Set the new mode for the specified token
        await ctx.send(f'Changed mode for token at position {position} to {mode}.')
    else:
        await ctx.send("No active client found for this token.")


@bot.command()
async def ara(ctx, user_id: int):
    global active_clients_1

    # Read tokens from tokens2.txt
    with open("tokens2.txt", "r") as f:
        tokens = f.read().splitlines()

    # List to hold all the client tasks
    client_tasks = []

    # Log in with every token and start responding to the specified user
    for token in tokens:
        if token not in active_clients_1:  # Check if the client is already running for this token
            client = AutoReplyClient(token, user_id)  # Create a new client instance for auto-replies
            active_clients_1[token] = client  # Keep track of the active client
            client_tasks.append(client.start(token, bot=False))  # Add the start task to the list
        else:
            active_clients_1[token].replying = True  # Ensure it's set to reply

    # Wait for all client tasks to complete
    await asyncio.gather(*client_tasks)

    await ctx.send(f'All tokens are now replying to <@{user_id}>.')
@bot.command()
async def arae(ctx):
    global active_clients_1

    # Stop all active clients
    for token in list(active_clients_1.keys()):
        active_clients_1[token].stop_replying()
        await active_clients_1[token].close()
    active_clients_1.clear()  # Clear the active clients list
    await ctx.send("Stopped auto replying for all tokens.")

@bot.command()
async def ama(ctx, mode: int):
    global active_clients_1

    # Check if the provided mode is valid (you can customize the range based on your modes)
    if mode < 1 or mode > 5:  # Assuming you have 5 modes
        await ctx.send("Invalid mode. Please provide a mode between 1 and 5.")
        return

    # Update the mode for each active client
    for token, client in active_clients_1.items():
        client.reply_mode = mode  # Set the mode for the token's client

    await ctx.send(f'All tokens have been set to mode {mode}.')








user_react_dict = {}
active_clients_x = {}


def read_tokens(filename='tokens2.txt'):
    """Read tokens from a file and return them as a list."""
    with open(filename, 'r') as file:
        tokens = file.read().splitlines()
    return tokens

def get_token_by_position(position):
    """Retrieve a token by its position from the tokens list."""
    tokens = read_tokens()
    if 0 <= position < len(tokens):
        return tokens[position]
    return None

class MultiToken3(discord.Client):
    def __init__(self, token, user_id, emoji, position, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.token = token
        self.user_id = user_id
        self.emoji = emoji
        self.position = position

    async def on_ready(self):
        print(f'Logged in as {self.user} using token {self.token[-4:]}.')

    async def on_message(self, message):
        if message.author.id == self.user_id:
            try:
                await message.add_reaction(self.emoji)
            except discord.Forbidden:
                print(f"Missing permissions to react to messages.")
            except discord.HTTPException as e:
                print(f"Failed to add reaction: {e}")

    async def close(self):
        await super().close()
        active_clients_x.pop(self.position, None)  # Remove client from active_clients_x

@bot.command()
async def react(ctx, user_id: int, position: int, emoji: str):
    """Set up a reaction to a user's messages with the specified token position."""
    token = get_token_by_position(position)
    if token:
        client = MultiToken3(token, user_id, emoji, position)
        await client.start(token, bot=False)
        active_clients_x[position] = client
        user_react_dict[position] = (user_id, emoji)
        await ctx.send(f'Will react to user {user_id}\'s messages with {emoji} using token {position}!')
    else:
        await ctx.send(f"No token found at position {position}.")

@bot.command()
async def reactend(ctx, position: int):
    """Stop reacting to a user's messages for the specified token position."""
    if position in active_clients_x:
        client = active_clients_x[position]
        await client.close()  # This will call the close method in MultiToken3
        await ctx.send(f'Stopped reacting for token at position {position}.')
    else:
        await ctx.send(f'No reaction set for token at position {position}.')



        






RECONNECT_DELAY = 0.1  # Delay before attempting to reconnect
RECONNECT_TIME = 120  # Time after which we will disconnect (2 minutes)



# Dictionary to store token-channel mappings for DMs/GCs and Servers
active_connections = {}  # Stores token-channel mappings and connection states

# WebSocket connection function for DMs and Group DMs
async def connect_to_dm_or_gc(token, channel_id):
    """Connect to a DM or Group DM using websockets."""
    uri = 'wss://gateway.discord.gg/?v=9&encoding=json'
    # Create a unique websocket connection per token
    async with websockets.connect(uri, max_size=None) as VOICE_WEBSOCKET:
        try:
            # Identify payload
            identify_payload = {
                'op': 2,
                'd': {
                    'token': token,
                    'intents': 513,
                    'properties': {
                        '$os': 'linux',
                        '$browser': 'my_library',
                        '$device': 'my_library'
                    }
                }
            }
            await VOICE_WEBSOCKET.send(json.dumps(identify_payload))

            # Voice State payload to join the voice channel
            voice_state_payload = {
                'op': 4,
                'd': {
                    'guild_id': None,  # For DMs and group chats
                    'channel_id': str(channel_id),
                    'self_mute': False,
                    'self_deaf': False,
                    'self_video': False
                }
            }
            await VOICE_WEBSOCKET.send(json.dumps(voice_state_payload))

            print(f"Connected to DM/GC channel {channel_id} with token ending in {token[-4:]}.")
            
            # Store this connection mapping and state
            active_connections[token] = {
                'channel_id': channel_id,
                'VOICE_WEBSOCKET': VOICE_WEBSOCKET
            }

            # Monitor connection and reconnect after disconnect
            await monitor_and_reconnect_dm_or_gc(token)

        except Exception as e:
            print(f"An error occurred while connecting to DM/GC channel {channel_id}: {e}")

async def monitor_and_reconnect_dm_or_gc(token):
    """Monitors the connection for each token and reconnects after disconnect."""
    while True:
        try:
            if token in active_connections:
                VOICE_WEBSOCKET = active_connections[token]['VOICE_WEBSOCKET']
                if VOICE_WEBSOCKET and VOICE_WEBSOCKET.closed:
                    print(f"Token ending in {token[-4:]} disconnected. Reconnecting...")
                    
                    # Get the original channel for reconnection
                    channel_id = active_connections[token]['channel_id']
                    await connect_to_dm_or_gc(token, channel_id)  # Reconnect to the same channel with the same token
                    
            await asyncio.sleep(RECONNECT_TIME)  # Check every 2 minutes

        except Exception as e:
            print(f"Reconnect attempt failed for token ending in {token[-4:]}: {e}")
            await asyncio.sleep(RECONNECT_DELAY)

# Standard connection for Server voice channels
async def connect_to_voice(token, channel_id, guild_id):
    """Connect a bot to a specific server voice channel."""
    intents = discord.Intents.default()
    intents.voice_states = True
    bot_instance = commands.Bot(command_prefix="!", intents=intents)

    @bot_instance.event
    async def on_ready():
        print(f"Logged in as {bot_instance.user} using token ending in {token[-4:]}.")
        guild = bot_instance.get_guild(guild_id)
        if not guild:
            print(f"Guild not found for ID {guild_id}.")
            return
        
        channel = discord.utils.get(guild.voice_channels, id=channel_id)
        if not channel:
            print(f"Voice channel not found for ID {channel_id}.")
            return
        
        try:
            await channel.connect()  # Connect to the voice channel
            print(f"Successfully connected to {channel.name} with token ending in {token[-4:]}.")
            
            # Store this connection mapping
            active_connections[token] = {
                'channel_id': channel_id,
                'guild_id': guild_id
            }

        except Exception as e:
            print(f"Failed to connect with token ending in {token[-4:]}: {e}")

    await bot_instance.start(token, bot=False)  # Start the bot with the token

async def connect_all_tokens_to_voice(channel_id, guild_id):
    """Connect all tokens to a specified voice channel in a server."""
    with open("tokens3.txt", "r") as f:  # Now reads from tokens3.txt
        tokens = f.read().splitlines()
    
    tasks = []
    for token in tokens:
        tasks.append(connect_to_voice(token, channel_id, guild_id))
    
    await asyncio.gather(*tasks)

@bot.command()
async def vc(ctx, position: int, channel_id: int):
    """Command to connect to a specific voice channel at a specified position."""
    guild_id = ctx.guild.id if ctx.guild else None
    with open("tokens3.txt", "r") as f:  # Reads from tokens3.txt
        tokens = f.read().splitlines()
    
    if 1 <= position <= len(tokens):
        token = tokens[position - 1]  # Adjust for 1-based index
        
        if ctx.guild:  # Server VC
            # For server voice channels
            await connect_to_voice(token, channel_id, guild_id)
            await ctx.send(f"Connected token at position {position} to server channel {channel_id}.")
        else:  # For DM or Group DM
            await connect_to_dm_or_gc(token, channel_id)  # DM/GC connection
            await ctx.send(f"Connected token at position {position} to DM/GC channel {channel_id}.")
    else:
        await ctx.send(f"Invalid position: {position}. Position must be between 1 and {len(tokens)}.")

@bot.command()
async def vce(ctx, position: int):
    """Command to connect to the calling voice channel at a specified position."""
    if ctx.author.voice and ctx.author.voice.channel:
        channel_id = ctx.author.voice.channel.id
        await vc(ctx, position, channel_id)
    else:
        await ctx.send("You are not connected to any voice channel.")

@bot.command()
async def vca(ctx, channel_id: int):
    """Command to connect all tokens to a specified voice channel."""
    guild_id = ctx.guild.id
    await connect_all_tokens_to_voice(channel_id, guild_id)
    await ctx.send(f"Connected all tokens to channel {channel_id}.")

# Run the bot


# Run the bot

INTERVAL = 1  # Time between guild identity changes
GUILDS = {

    "rascal": "1034280738129989704",
    "text": "1255456345541443635",
    "star": "1162118669472641024",
    "peep": "1097371199497044034",
    "hesi": "1262925088374915204",
    "kfc": "1213945965686296647"
}
DISCORD_API_URL = "https://discord.com/api/v9/users/@me/clan"
guild_rotation_task = None

def change_identity(guild_name, guild_id):
    headers = {
        "Accept": "*/*",
        "Authorization": token,
        "Content-Type": "application/json"
    }

    payload = {
        "identity_guild_id": guild_id,
        "identity_enabled": True
    }

    try:
        response = requests.put(DISCORD_API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            print(f"Successfully changed to {guild_name}")
        else:
            print(f"Failed to change to {guild_name}. Status Code: {response.status_code}, Response: {response.text}")
    except requests.RequestException as e:
        print(f"Error while changing to {guild_name}: {e}")

async def rotate_guilds():
    while True:
        for guild_name, guild_id in GUILDS.items():
            change_identity(guild_name, guild_id)
            await asyncio.sleep(INTERVAL)

@bot.command()
async def rg(ctx):
    global guild_rotation_task
    if guild_rotation_task is None:
        guild_rotation_task = bot.loop.create_task(rotate_guilds())
        await ctx.send("Guild rotation started!")
    else:
        await ctx.send("Guild rotation is already running.")

@bot.command()
async def rge(ctx):
    global guild_rotation_task
    if guild_rotation_task is not None:
        guild_rotation_task.cancel()
        guild_rotation_task = None
        await ctx.send("Guild rotation stopped!")
    else:
        await ctx.send("Guild rotation is not running.")

@bot.command()
async def rgd(ctx, delay: int):
    """Change the delay for the guild rotation."""
    global INTERVAL
    if delay > 0:
        INTERVAL = delay
        await ctx.send(f"Guild rotation delay changed to {INTERVAL} seconds.")
    else:
        await ctx.send("Delay must be a positive integer.")

@bot.command()
async def us(ctx, *, statuses: str):
    global status_list
    status_list = [status.strip() for status in statuses.split(',')]
    await ctx.send(f"Status list set to: {', '.join(status_list)}")




bot.run(token, bot=False)