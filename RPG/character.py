from Fortuna import smart_clamp, TruffleShuffle, dice
from MonkeyScope import distribution

from RPG.utilities import Bonuses
from cogs.dice_cog import parse_dice


class Archetype:
    bonus_lookup = {
        'Offence': Bonuses(3, 2, 1),
        'Defense': Bonuses(1, 3, 2),
        'Utility': Bonuses(2, 2, 2),
    }

    def __init__(self, name):
        self.name = name
        self.bonuses = self.bonus_lookup[name]


class Bloodline:
    bonus_lookup = {
        'Teraphim': Bonuses(3, 2, 1),
        'Seraphim': Bonuses(1, 3, 2),
        'Nephilim': Bonuses(2, 2, 2),
    }

    def __init__(self, name):
        self.name = name
        self.bonuses = self.bonus_lookup[name]


class ClassType:
    hit_dice_lookup = {
        'Warrior': 12,
        'Priest': 10,
        'Mage': 8,
    }
    damage_dice_lookup = {
        'Warrior': 8,
        'Priest': 10,
        'Mage': 12,
    }

    def __init__(self, name):
        self.name = name
        self.hit_dice = self.hit_dice_lookup[name]
        self.damage_dice = self.damage_dice_lookup[name]


class Character:
    d3 = TruffleShuffle((1, 2, 3))
    random_archetype = TruffleShuffle((
        Archetype('Offence'), Archetype('Defense'), Archetype('Utility')
    ))
    random_bloodline = TruffleShuffle((
        Bloodline('Teraphim'), Bloodline('Seraphim'), Bloodline('Nephilim')
    ))
    random_class = TruffleShuffle((
        ClassType('Warrior'), ClassType('Priest'), ClassType('Mage')
    ))

    def __init__(self, name, class_type=None, level=1):
        self.name = name
        self.class_type = class_type or self.random_class()
        self.level = level
        self.mind = self.d3()
        self.body = self.d3()
        self.soul = self.d3()
        self.archetype = self.random_archetype()
        self.bloodline = self.random_bloodline()
        self.bonuses = self.archetype.bonuses + self.bloodline.bonuses
        self.current_sanity = self.total_sanity
        self.current_health = self.total_health
        self.current_energy = self.total_energy

    @property
    def damage_formula(self):
        return f'{self.level}d{self.class_type.damage_dice}+{self.offense}'

    @property
    def attack_roll_formula(self):
        return f'd20+{self.offense}'

    @property
    def defend_roll_formula(self):
        return f'd20+{self.defense}'

    @property
    def is_dead(self):
        return self.current_health < 1

    @property
    def total_sanity(self):
        return (self.mind + self.level) * self.class_type.hit_dice

    @property
    def total_health(self):
        return (self.body + self.level) * self.class_type.hit_dice

    @property
    def total_energy(self):
        return (self.soul + self.level) * self.class_type.hit_dice

    @property
    def offense(self):
        return max(self.mind, self.body, self.soul) + self.bonuses.offense

    @property
    def defense(self):
        return min(self.mind, self.body, self.soul) + self.bonuses.defense

    @property
    def balance(self):
        return smart_clamp(self.mind, self.body, self.soul) + self.bonuses.balance

    @property
    def sanity(self):
        return f"{self.current_sanity}/{self.total_sanity}"

    @property
    def health(self):
        return f"{self.current_health}/{self.total_health}"

    @property
    def energy(self):
        return f"{self.current_energy}/{self.total_energy}"

    def __str__(self):
        output = (
            f"Character Name: {self.name}",
            f"    Class: {self.class_type.name}",
            f"    Level: {self.level}",
            f"    Archetype: {self.archetype.name}",
            f"    Bloodline: {self.bloodline.name}",
            f"Attributes:",
            f"    Mind: {self.mind}",
            f"    Body: {self.body}",
            f"    Soul: {self.soul}",
            f"Modifiers:",
            f"    Offense: {self.offense}",
            f"    Defense: {self.defense}",
            f"    Utility: {self.balance}",
            f"Resources:",
            f"    Sanity: {self.sanity}",
            f"    Health: {self.health}",
            f"    Energy: {self.energy}",
            f"Formulas:",
            f"    Attack: 1d20+{self.offense}",
            f"    Defend: 1d20+{self.defense}",
            f"    Damage: {self.damage_formula}",
            ""
        )
        return '\n'.join(output)

    def take_damage(self, amount):
        self.current_health = smart_clamp(
            self.current_health - amount, 0, self.total_health)

    def take_heal(self, amount):
        self.current_health = smart_clamp(
            self.current_health + amount, 0, self.total_health)

    def damage(self):
        log, amount = parse_dice(self.damage_formula, self.name)
        # print(log)
        return int(amount)

    def attack(self):
        log, amount = parse_dice(self.attack_roll_formula, self.name)
        # print(log)
        return int(amount)

    def defend(self):
        log, amount = parse_dice(self.defend_roll_formula, self.name)
        # print(log)
        return int(amount)


class CustomCharacter(Character):

    def __init__(self, name, class_type=None, level=1,
                 bloodline=None, archetype=None,
                 mind=None, body=None, soul=None):
        super().__init__(name, class_type, level)
        if bloodline:
            self.bloodline = bloodline
        if archetype:
            self.archetype = archetype
        if mind:
            self.mind = mind
        if body:
            self.body = body
        if soul:
            self.soul = soul
        self.bonuses = self.archetype.bonuses + self.bloodline.bonuses
        self.current_sanity = dice(self.mind + self.level, self.class_type.hit_dice)
        self.current_health = dice(self.body + self.level, self.class_type.hit_dice)
        self.current_energy = dice(self.soul + self.level, self.class_type.hit_dice)


if __name__ == '__main__':
    print()
    c = CustomCharacter(
        name='Ming',
        class_type=ClassType("Mage"),
        level=1,
        bloodline=Bloodline('Teraphim'),
        archetype=Archetype('Offence'),
        mind=3,
        body=2,
        soul=1,
    )
    d = CustomCharacter(
        name='Binwin',
        class_type=ClassType("Warrior"),
        level=1,
        bloodline=Bloodline('Seraphim'),
        archetype=Archetype('Defense'),
        mind=1,
        body=3,
        soul=2,
    )
    print(c)
    print(d)
    distribution(lambda: c.damage() if c.attack() > d.defend() else 0)
    print()
    distribution(lambda: d.damage() if d.attack() > c.defend() else 0)
