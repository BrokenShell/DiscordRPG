from discord.ext import commands
from Fortuna import dice


class DiceCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def roll(self, ctx, *, dice_expression: str = 'd20'):
        """ Evaluates a dice expression like `d6`, `3d6` or `3d6+1`
        Examples:
            /roll       -> rolls one twenty-sided die
            /roll d10   -> rolls one ten-sided die
            /roll 3d6   -> rolls three six-sided dice
            /roll 8d6+3 -> rolls eight six-sided dice, then adds three
            /roll XdY+Z -> rolls a Y-sided dice X times, then adds Z """
        name, _ = str(ctx.author).split("#")
        await ctx.send('\t=>\t'.join(parse_dice(dice_expression, name)))


def setup(bot):
    bot.add_cog(DiceCog(bot))
    print('[•] Dice Loaded')


def parse_dice(dice_expression, name):
    if '+' in dice_expression:
        op = '+'
        dice_expression, modifier = dice_expression.split(op)
        modifier = int(modifier)
    elif '-' in dice_expression:
        op = '-'
        dice_expression, modifier = dice_expression.split(op)
        modifier = abs(int(modifier))
    else:
        modifier = ''
        op = ''

    if 'd' in dice_expression:
        rolls, sides = dice_expression.split('d')
        rolls = int(rolls) if rolls else 1
        sides = int(sides) if sides else 20
    else:
        rolls = 1
        sides = int(dice_expression)

    if op == '+':
        output = (
            f'{name} rolls `{rolls if rolls != 1 else ""}d{sides} + {modifier}`',
            f'{dice(rolls, sides) + modifier}',
        )
    elif op == '-':
        output = (
            f'{name} rolls `{rolls if rolls != 1 else ""}d{sides} - {modifier}`',
            f'{dice(rolls, sides) - modifier}',
        )
    else:
        output = (
            f'{name} rolls `{rolls if rolls != 1 else ""}d{sides}`',
            f'{dice(rolls, sides)}',
        )
    return output
