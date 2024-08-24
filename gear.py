class Weapon:

    def __init__(self, name, damage=1, speed=1, enchants={}, luck=0, rarity="Common", string_color='#ADADAD'):
        self.name = name
        self.damage = damage
        self.speed = speed
        self.enchants = enchants
        self.luck = luck
        self.rarity = rarity
        self.slot = 'weapon'
        self.color = string_color

    def __str__(self):
        return self.name


class Armor:

    def  __init__(self, name, defense, HP, hp_regen, regen_speed, luck, slot, rarity, enchants, burn_strength, burn_speed, poison_power, poison_speed, frost_power, string_color):
        self.name = name
        self.defense = defense
        self.hp = HP
        self.luck = luck
        self.enchants = enchants
        self.regen_amount = hp_regen
        self.regen_interval = regen_speed       
        self.burn_power = burn_strength
        self.burn_interval = burn_speed
        self.poison_power = poison_power
        self.poison_interval = poison_speed
        self.frost_power = frost_power
        self.rarity = rarity
        self.color = string_color
        self.slot = slot # helm, chest, legs, gloves, boots, trinket

    def __str__(self):
        return self.name