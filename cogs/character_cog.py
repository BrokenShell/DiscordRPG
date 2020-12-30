from discord.ext import commands
from RPG.character import Character


class CharacterCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def make_character(self, ctx, *, name: str = ''):
        if name:
            print(f'[•] Making {name}')
            character = Character(name)
            await ctx.send(character)


def setup(bot):
    bot.add_cog(CharacterCog(bot))
    print('[•] Character Loaded')
