import discord , os , asyncio
from discord.ext import commands
from dotenv import load_dotenv
import wavelink


load_dotenv()

intents = discord.Intents.all()

class OurBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def setup_hook(self):
     await load_extensions()

client = OurBot(command_prefix=os.environ['BOTPREFIX'], intents = intents, status=discord.Status.idle, activity=discord.Streaming(name=f"Version {os.environ['BOTVER']} | {os.environ['BOTPREFIX']}help", url="https://www.twitch.tv/discord"))


@client.listen()
async def on_wavelink_node_ready(node: wavelink.Node):
        print(f"Node <{node.identifier}> is now Ready!")


@client.event
async def on_ready():
    print(f'logged in as: {client.user.name}')

async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")

client.run(os.environ['TOKEN'])
