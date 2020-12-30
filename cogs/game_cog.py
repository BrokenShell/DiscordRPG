from discord.ext import commands


class GameCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def echo(self, ctx, *, text: str):
        await ctx.send(text)


def setup(bot):
    bot.add_cog(GameCog(bot))
    print('[•] Game Loaded')
