import discord , os , asyncio
from discord.ext import commands
from settings import botToken , botVer

intents = discord.Intents(messages = True, guilds = True)
intents.guild_messages = True
intents.members = True
intents.message_content = True
intents.voice_states = True
intents.emojis_and_stickers = True
all_intents = intents.all()
all_intents= True

client = commands.Bot(command_prefix='!', intents = intents)

@client.event
async def on_ready():
    print(f'logged in as: {client.user.name}')
    await client.change_presence(status=discord.Status.idle, activity = discord.Streaming(name=f"Version {botVer} | !help", url="https://www.twitch.tv/discord"))


async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")

async def Login():
    async with client:
        await load_extensions()
        await client.start(botToken)

asyncio.run(Login())
