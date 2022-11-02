import discord
import typing
import wavelink

from discord.ext import commands

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.embed_color = discord.Color.from_rgb(128, 67, 255)

    async def create_nodes(self):
        await self.bot.wait_until_ready()
        await wavelink.NodePool.create_node(bot=self.bot, host="kyuk.my.id", port="2333", password="www.kyuk.my.id", region="asia")

    async def user_connectivity(self,ctx: commands.Context):
        if not getattr(ctx.author.voice, 'channel', None):
            await ctx.send(embed=discord.Embed(description=f'Try after joining a `voice channel`', color=discord.Color.from_rgb(128, 67, 255)))        
            return False
        else:   
            return True
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Music Cog is now ready!")

    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        print(f"Node <{node.identifier}> is now Ready!")

    @commands.command(name="join", aliases=["connect", "summon"])
    async def join_command(self, ctx: commands.Context, channel: typing.Optional[discord.VoiceChannel]):
        if channel is None:
            channel = ctx.author.voice.channel
        
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)

        if player is not None:
            if player.is_connected():
                return await ctx.send("bot is already connected to a voice channel")
        
        await channel.connect(cls=wavelink.Player)
        mbed=discord.Embed(title=f"Connected to {channel.name}{channel}", color=discord.Color.from_rgb(255, 255, 255))
        await ctx.send(embed=mbed)

    @commands.command(name='disconnect', aliases=['dc', 'leave'], help='Keluar dari voice')
    async def disconnect_command(self,ctx: commands.Context):
        if await self.user_connectivity(ctx) == False:
            return
        else:
            vc : wavelink.Player = ctx.voice_client
            try:
                await vc.disconnect()
                await ctx.send(embed=discord.Embed(description='**BYE!** Have a great time!', color=discord.Color.from_rgb(255, 255, 255)))
            except Exception:
                await ctx.send(embed=discord.Embed(description='Failed to destroy!', color=discord.Color.from_rgb(255, 255, 255)))

    @commands.command(name='play', aliases=['p'], help='Memutar lagu yang di berikan')
    async def play_command(self,ctx: commands.Context, *, search: wavelink.YouTubeTrack):
        if not getattr(ctx.author.voice, 'channel', None):
            return await ctx.send(embed=discord.Embed(description=f'Coba lagi setelah join kedalam voice', color=discord.Color.from_rgb(128, 67, 255)))  
        elif not ctx.voice_client:
            vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        else:
            vc: wavelink.Player = ctx.voice_client
        if not vc.is_playing() and vc.queue.is_empty(): 
         await vc.play(search)
         playString = discord.Embed(description=f'**Search found**\n\n`{search.title}`', color=discord.Color.from_rgb(128, 67, 255))
         await ctx.send(embed=playString)
        else:
         await vc.queue.put_wait(search)
         await ctx.send("Added: ", search)

    @commands.command(name='skip', help="Skip Lagu")
    async def skip(self, ctx):
       if not getattr(ctx.author.voice, 'channel', None):
            return await ctx.send(embed=discord.Embed(description=f'Coba lagi setelah join kedalam voice', color=discord.Color.from_rgb(128, 67, 255)))  
       elif not ctx.voice_client:
            return await ctx.send("Bot is not connected")
       else:
            vc: wavelink.Player = ctx.voice_client
       if not vc.is_playing():
        return await ctx.send("Nothing Played")
       await ctx.send("Skipped: ", vc.track.title)
       await vc.stop()


      
    

async def setup(bot):
    await bot.loop.create_task(self.create_nodes())
    await bot.add_cog(Music(bot))
