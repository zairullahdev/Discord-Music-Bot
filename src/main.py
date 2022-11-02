import discord , os , asyncio
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.all()


client = commands.Bot(command_prefix=os.environ['PREFIX'], intents = intents, status=discord.Status.idle, activity=discord.Streaming(name=f"Version {os.environ['BOTVER']} | {os.environ['PREFIX']}help", url="https://www.twitch.tv/discord")

@client.event
async def on_ready():
    print(f'logged in as: {client.user.name}')



async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")

async def Login():
    async with client:
        await load_extensions()
        await client.start(botToken)

asyncio.run(Login())
