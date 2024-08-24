import random
import time
import threading

from gear import Weapon, Armor
from enemy import Enemy


class Player:

    def __init__(self):
        self.current_health = 250
        self.max_health = 250
        self.armor = 0
        self.attack = 0
        self.attack_speed = 1
        self.luck = 0
        self.enchants = {}
        self.completed_combats = 0
        self.chest_pity = 0
        self.opened_chests = 0

        self.regen_amount = 5
        self.regen_interval = 2        
        self.burn_power = 1
        self.burn_interval = 2
        self.poison_power = 1
        self.poison_interval = 1
        self.frost_power = 1

        self.hp_bar = None
        self.hp_text = None
        self.regenerating = False
        self.dead = False

        self.weapon = None
        self.helmet = None
        self.chestpiece = None
        self.pants = None
        self.boots = None
        self.gloves = None
        self.trinket = None

        self.high_score = 0
        self.window_reference = None


    def take_damage(self, amount, hp_bar, hp_text, combat_screen):
        # assign hp_bar and text to keep threading happy
        self.hp_bar = hp_bar
        self.hp_text = hp_text

        # mitigate damage taken through armor
        mitigated_damage = round(amount / (1 + (self.armor/75)))
        
        if self.current_health - mitigated_damage < 1:
            self.die(combat_screen)
            return
        self.current_health -= mitigated_damage
        if combat_screen.active:
            combat_screen.handle_combat_text("enemy_damage", mitigated_damage)
        if self.check_children():
            self.hp_bar.set(self.current_health / self.max_health)
            self.hp_text.configure(text=f"{self.current_health} / {self.max_health}")
        #print(f"Took {mitigated_damage} damage!")
        if self.regenerating == False:
            self.open_regen_thread()
        return mitigated_damage
    
    def open_regen_thread(self):
        self.regen_thread = threading.Thread(name='regen', target=self.regen_HP)
        self.regen_thread.start()

    def die(self, combat_screen):
        self.dead = True
        combat_screen.draw_death_screen()
        combat_screen.destroy()
        print("You died!")


    def regen_HP(self):

        while (self.current_health < self.max_health) and self.dead == False:
            #print(self.check_children())
            self.regenerating = True
            new_hp = (self.current_health + self.regen_amount)
            if new_hp > self.max_health:
                self.current_health = self.max_health
            else:
                self.current_health = new_hp
            if self.check_children():
                self.hp_bar.set(self.current_health / self.max_health)
                self.hp_text.configure(text=f"{self.current_health} / {self.max_health}")
            else:
                break
            #print(f"Restored {self.regen_amount} HP, bringing your total HP to {self.current_health}")
            time.sleep(self.regen_interval)
        self.regenerating = False

    def check_children(self):

        for child in self.window_reference.children:
            if 'combat_screen' in child:
                return True
            else:
                return False

            



    def generate_loot(self, forced=""):
        a_or_w = random.randrange(1, 4)
        if a_or_w == 1 or forced == "weapon":
            # weapon - name, damage=1, speed=1, enchants={}, rarity="Common"
            # possible_weapons list (found in select_base_weapon method) is a list of tuples formatted (name, base damage, base speed)

            base_weapon = self.select_base_weapon()

            base_name = base_weapon[0]
            base_damage = base_weapon[1]
            base_speed = base_weapon[2]



            rarity = random.randrange(1,11)

            if rarity < 4:
                # common
                #print(f"Rolled a rarity of: {rarity}!")
                wep = self.modify_base_stats(base_name, base_damage, base_speed, "Common")
                #print(f"Generated a {wep.name} with {wep.damage} damage, {round(wep.speed, 2)}s attack delay, and {len(wep.enchants)} enchantments, of {wep.rarity} rarity")
                return wep
            elif rarity <= 6:
                # rare
                #print(f"Rolled a rarity of: {rarity}!")
                wep = self.modify_base_stats(base_name, base_damage, base_speed, "Rare")
                #print(f"Generated a {wep.name} with {wep.damage} damage, {round(wep.speed, 2)}s attack delay, and {len(wep.enchants)} enchantments, of {wep.rarity} rarity")
                return wep
            elif rarity <= 9:
                # epic
                #print(f"Rolled a rarity of: {rarity}!")
                wep = self.modify_base_stats(base_name, base_damage, base_speed, "Epic")
                #print(f"Generated a {wep.name} with {wep.damage} damage, {round(wep.speed, 2)}s attack delay, and {len(wep.enchants)} enchantments, of {wep.rarity} rarity")
                return wep
            elif rarity == 10:
                # legendary
                #print(f"Rolled a rarity of: {rarity}!")
                wep = self.modify_base_stats(base_name, base_damage, base_speed, "Legendary")
                #print(f"Generated a {wep.name} with {wep.damage} damage, {round(wep.speed, 2)}s attack delay, and {len(wep.enchants)} enchantments, of {wep.rarity} rarity")
                return wep

        elif a_or_w >1 or forced =="armor":
            # armor - name, defense, HP, luck, dodge
            which_piece = random.randrange(1, 7)

            match which_piece:

                case 1:
                    base_armor = self.select_base_helm()
                    slot = 'helm'
                case 2:
                    base_armor = self.select_base_chestpiece()
                    slot = 'chest'
                case 3:
                    base_armor = self.select_base_legs()
                    slot = 'legs'
                case 4:
                    base_armor = self.select_base_gloves()
                    slot = 'gloves'
                case 5:
                    base_armor = self.select_base_boots()
                    slot = 'boots'
                case 6:
                    base_armor = self.select_base_trinket()
                    slot = 'trinket'
                
                case _:
                    print(f"Generated a base_armor roll outside the scope that should be possible.  Rolled: {which_piece}")

            base_armor_name = base_armor[0]
            base_armor_value = base_armor[1]
            base_armor_hp = base_armor[2]
            base_armor_regen = base_armor[3]

            rarity = random.randrange(1,11)

            if rarity < 4:
                armor = self.modify_base_armor_stats(base_armor_name, base_armor_value, base_armor_hp, base_armor_regen, slot, "Common")
                return armor
            elif rarity <= 6:
                armor = self.modify_base_armor_stats(base_armor_name, base_armor_value, base_armor_hp, base_armor_regen, slot, "Rare")
                return armor
            elif rarity <= 9:
                armor = self.modify_base_armor_stats(base_armor_name, base_armor_value, base_armor_hp, base_armor_regen, slot, "Epic")
                return armor
            elif rarity == 10:
                armor = self.modify_base_armor_stats(base_armor_name, base_armor_value, base_armor_hp, base_armor_regen, slot, "Legendary")
                return armor
            
    def string_color_picker(self, rarity):

        if rarity == "Common":
            return "#ADADAD"
        elif rarity == "Rare":
            return "#62B0FC"
        elif rarity == "Epic":
            return "#C462FC"
        elif rarity == "Legendary":
            return "#FCC462"

    def select_base_weapon(self):

        possible_weapons = [('Dagger', 6, 0.25),
                            ('Sword', 16, 1),
                            ('Bow', 10, 0.75),
                            ('Staff', 30, 1.75),
                            ('Whip', 14, 0.75),
                            ('Scimitar', 20, 0.8),
                            ('Wand', 26, 1),
                            ('Maul', 60, 3),
                            ('Hammer', 24, 1.2),
                            ('Throwing Knife', 15, 0.6),
                            ('Crossbow', 30, 1.25),
                            ('Scythe', 40, 2),
                            ('Bell', 8, 0.3),
                            ('Claws', 12, 0.55),
                            ('Longsword', 25, 1.25),
                            ('Ritual Book', 45, 2),
                            ('Longbow', 40, 1.8),
                            ('Musket', 70, 4)]
        
        return possible_weapons[random.randrange(len(possible_weapons))]
    
    def select_base_helm(self):

        possible_helms = [('Full Helm', 8, 17, 3),     #Name, Armor, HP, HP regen
                            ('Medium Helm', 5, 20, 5),
                            ('Cap', 2, 20, 10),
                            ('Cowl', 3, 17, 10),
                            ('Greathelm', 15, 15, 5),
                            ('Faceguard', 10, 15, 5),
                            ('Wizard Hat', 2, 10, 15),
                            ('Mask', 1, 20, 10),
                            ('Halo', 4, 15, 10),
                            ('Robinhood Hat', 3, 10, 10),
                            ('Chainhood', 7, 15, 8)]
        
        return possible_helms[random.randrange(len(possible_helms))]
    
    def select_base_chestpiece(self):

        possible_chests = [('Platebody', 8, 17, 3),     #Armor, HP, HP regen
                            ('Chainbody', 5, 20, 5),
                            ('Cloth Shirt', 2, 20, 10),
                            ('Vest', 3, 17, 10),
                            ('Breastplate', 15, 15, 5),
                            ('Gambeson', 10, 15, 5),
                            ('Robe', 2, 10, 15),
                            ('Gown', 1, 20, 10),
                            ('Garb', 4, 15, 10),
                            ('Tunic', 7, 15, 8)]
        
        return possible_chests[random.randrange(len(possible_chests))]
    
    def select_base_legs(self):

        possible_legs = [('Platelegs', 8, 17, 3),     #Armor, HP, HP regen
                            ('Plateskirt', 5, 20, 5),
                            ('Trousers', 2, 20, 10),
                            ('Pants', 3, 17, 10),
                            ('Greathelm', 15, 15, 5),
                            ('Chausses', 10, 15, 5),
                            ('Robe Bottoms', 2, 10, 15),
                            ('Greaves', 10, 15, 2)]
    
        return possible_legs[random.randrange(len(possible_legs))]
    
    def select_base_gloves(self):

        possible_gloves = [('Plated Gloves', 8, 17, 3),     #Armor, HP, HP regen
                            ('Vambraces', 5, 20, 5),
                            ('Gloves', 2, 20, 10),
                            ('Mitts', 3, 17, 10),
                            ('Gauntlets', 15, 15, 5),
                            ('Grasps', 10, 15, 5),
                            ('Fingerless Gloves', 2, 10, 15),
                            ('Wristwraps', 1, 20, 10),
                            ('Knuckles', 4, 15, 10)]
        
        return possible_gloves[random.randrange(len(possible_gloves))]

    def select_base_boots(self):

        possible_boots = [('Plate Boots', 8, 17, 3),     #Armor, HP, HP regen
                            ('Leather Boots', 5, 20, 5),
                            ('Cloth Boots', 2, 20, 10),
                            ('Shoes', 3, 17, 10),
                            ('Greatboots', 15, 15, 5),
                            ('Dragonhide Boots', 10, 15, 5),
                            ('Sandals', 2, 10, 15),
                            ('Socks', 1, 20, 10)]
        
        return possible_boots[random.randrange(len(possible_boots))]
    
    def select_base_trinket(self):

        possible_trinkets = [('Ring', 8, 17, 3),     #Armor, HP, HP regen
                            ('Prayer Scroll', 5, 20, 5),
                            ('Amulet', 2, 20, 10),
                            ('Beads', 3, 17, 10),
                            ('Talisman', 15, 15, 5),
                            ('Bracelet', 10, 15, 5),
                            ('Soapstone Idol', 2, 10, 15),
                            ('Fingerbone', 1, 20, 10),
                            ('Fossilized Tooth', 1, 30, 5),
                            ('Bone Flute', 8, 5, 20),
                            ('Beating Heart', 1, 30, 1)]
        
        return possible_trinkets[random.randrange(len(possible_trinkets))]
    
        
        
    def modify_base_armor_stats(self, name, armor_value, armor_hp, hp_regen, slot, rarity):

        modded_armor_name = self.add_name_prefix(rarity) + name

        modded_armor = self.modify_damage_value(armor_value, rarity)

        modded_hp = self.modify_damage_value(armor_hp, rarity)

        modded_regen = self.modify_damage_value(hp_regen, rarity)

        armor_enchant_tuple = self.add_armor_enchants(rarity)
        enchants = {}

        string_color = self.string_color_picker(rarity)
        
        luck = 0

        regen_speed = 1

        burn_strength = 1

        burn_speed = 1

        poison_strength = 1

        poison_speed = 1

        frost_power = 1

        if armor_enchant_tuple is not None:
                modded_armor_name += f" {armor_enchant_tuple[0]}"
                enchants = armor_enchant_tuple[1]       

        if 'Armor' in enchants:
            armor_modifier = (1 + enchants['Armor'] * 0.1)
            modded_armor = round(armor_modifier * modded_armor)

        if 'Health' in enchants:
            hp_modifier = (1 + enchants['Health'] * 0.1)
            modded_hp = round(hp_modifier * modded_hp)

        if 'Regen' in enchants:
            regen_modifier = (1 + enchants['Regen'] * 0.1)
            modded_regen = round(regen_modifier * modded_regen)

        if 'Regen Speed' in enchants:
            regen_speed_modifier = (1 - enchants['Regen Speed'] * 0.05)
            if regen_speed_modifier < 0.75: regen_speed_modifier = 0.75
            regen_speed = round(regen_speed * regen_speed_modifier, 2)

        if 'Burn Strength' in enchants:
            burn_modifier = (enchants['Burn Strength'] * 0.5)
            burn_strength = burn_modifier * burn_strength

        if 'Poison Strength' in enchants:
            poison_modifier = (enchants['Poison Strength'] * 0.5)
            poison_strength = poison_modifier * poison_strength

        if 'Frost Power' in enchants:
            frost_modifier = (enchants['Frost Power'] * 0.3)
            frost_power = frost_modifier * frost_power

        if 'Burn Speed' in enchants:
            burn_speed_modifier = (1 - (enchants['Burn Speed'] * 0.1))
            if burn_speed_modifier < 0.5: burn_speed_modifier = 0.5
            burn_speed = burn_speed_modifier * burn_speed

        if 'Poison Speed' in enchants:
            poison_speed_modifier = (1 - (enchants['Poison Speed'] * 0.1))
            if poison_speed_modifier < 0.5: poison_speed_modifier = 0.5
            poison_speed = poison_speed_modifier * poison_speed

        if 'Luck Up' in enchants:
                luck = (enchants['Luck Up'])

        return Armor(modded_armor_name, modded_armor, modded_hp, modded_regen, regen_speed, luck, slot, rarity, enchants, burn_strength, burn_speed, poison_strength, poison_speed, frost_power, string_color)

    def modify_base_stats(self, name, damage, speed, rarity):
        
        # add name prefix, based on rarity
            modded_name = self.add_name_prefix(rarity) + name

        # modify base damage to produce final damage, based on rarity
            modded_damage = self.modify_damage_value(damage, rarity)

        # modify base speed value to produce final seped, based on rarity
            modded_speed = self.modify_attack_speed(speed, rarity)

        # add enchantments based on rarity
            enchant_tuple = self.add_enchants(rarity)
            enchants = {}

        # initialize luck to avoid errors
            luck = 0

        # determine a rarity-based string_color for use in tooltips
            string_color = self.string_color_picker(rarity)

        # modify base stats based on enchantments 
            if enchant_tuple is not None:
                modded_name += f" {enchant_tuple[0]}"
                enchants = enchant_tuple[1]       
            if 'Damage Up' in enchants:
                damage_modifier = (1 + enchants['Damage Up'] * 0.1)
                modded_damage = round(damage_modifier * modded_damage)
            if 'Speed Up' in enchants:
                speed_modifier = (1 - enchants['Speed Up'] * 0.05)
                modded_speed *= speed_modifier
            if 'Luck Up' in enchants:
                luck = (enchants['Luck Up'])       
            
            return Weapon(modded_name, modded_damage, modded_speed, enchants, luck, rarity, string_color)
        

    def add_name_prefix(self, rarity):
        common_names = ["Rusted", "Chipped", "Tarnished", "Dusty", "Weathered", "Worn", "Crusty", "Poor", "Weak", "Ragged", "Dull", "Unremarkable",
                        "Unexciting", "Lame", "Bland"]
        rare_names = ["Shiny", "Sturdy", "Stout", "Reliable", "Polished", "Appealing", "Useful", "Proven", "Handy", "Nice", "Worthy", "Decent", "Good"]
        epic_names = ["Great", "Gleaming", "Powerful", "Arcane", "Battle-worn", "Bloodsoaked", "Excellent", "Hero's", "Devious", "Stunning", "Wicked", "Cruel",
                      "Wizard's", "Elven", "Dragonslayer's", "Ancient"]
        legendary_names = ["Radiant", "Conqueror's", "Exceptional", "Legendary", "Masterwork", "God-given", "Headhunter's", "Soultaker's", "Reaper's",
                           "Assassin's", "Bounty Hunter's", "Masterpiece", "Exquisite", "Divine", "Angelic", "Diabolical", "Mythic", "Frostwoven", "Infernal",
                           "Archmage's", "Imperial"]
        
        if rarity == "Common":
            return f"{common_names[random.randrange(len(common_names))]} "
        if rarity == "Rare":
            return f"{rare_names[random.randrange(len(rare_names))]} "
        if rarity == "Epic":
            return f"{epic_names[random.randrange(len(epic_names))]} "
        if rarity == "Legendary":
            return f"{legendary_names[random.randrange(len(legendary_names))]} "
        
    def modify_damage_value(self, damage, rarity):
        if rarity == "Common":
            return int(damage * random.uniform(1, 1.3))
        if rarity == "Rare":
            return int(damage * random.uniform(1.2, 1.6))
        if rarity == "Epic":
            return int(damage * random.uniform(1.4, 1.9))
        if rarity == "Legendary":
            return int(damage * random.uniform(1.6, 2.5))
        
    def modify_attack_speed(self, speed, rarity):
        if rarity == "Common":
            return (speed * random.uniform(0.8, 1))
        if rarity == "Rare":
            return (speed * random.uniform(0.7, 1))
        if rarity == "Epic":
            return (speed * random.uniform(0.6, 1))
        if rarity == "Legendary":
            return (speed * random.uniform(0.5, 1))
        
    def add_enchants(self, rarity):
        # Later, when I use a list to roll for enchants, I can just search this dict for the enchant to get the appropriate suffix
        suffix_enchants = {'Vampirism': 'of the Vampire', 'Burning': 'of the Inferno', 'Frost': 'of Ice', 'Speed Up': 'of the Winds', 'Luck Up': 'of the Thief',
                           'Damage Up': 'of Brutality', 'Poison': 'of the Fang', 'Blindness': 'of the Eye'}
        
        enchants_list = ['Vampirism', 'Burning', 'Frost', 'Speed Up', 'Luck Up', 'Damage Up', 'Poison', 'Blindness']

        output_enchants = {}

        if rarity == "Common":
            return None
        
        if rarity == "Rare":
            return None
        
        if rarity == "Epic":
            no_of_enchants = random.randrange(1, 3)
            suffix = None
            for i in range(no_of_enchants):
                random_enchant = enchants_list[random.randrange(0, len(enchants_list))]
                if suffix is None:
                    suffix = suffix_enchants[random_enchant]
                output_enchants[random_enchant] = random.randrange(1, 6)

        if rarity == "Legendary":
            no_of_enchants = random.randrange(2, 4)
            suffix = None
            for i in range(no_of_enchants):
                random_enchant = enchants_list[random.randrange(0, len(enchants_list))]
                if suffix is None:
                    suffix = suffix_enchants[random_enchant]
                output_enchants[random_enchant] = random.randrange(3, 6)
        
        return (suffix, output_enchants)
    
    def add_armor_enchants(self, rarity):

        suffix_enchants = {'Burn Strength': 'of the Pyromancer', 'Burn Speed': 'of Encroaching Flames', 'Health': 'of the Brawny', 'Armor': 'of the Juggernaut', 
                           'Regen': 'of the Medic', 'Regen Speed': 'of the Hearty', 'Poison Strength': 'of Venom', 'Poison Speed': 'of the Assassin', 'Frost Power': 'of Rime'}
        
        enchants_list = ['Burn Strength', 'Burn Speed', 'Health', 'Armor', 'Regen', 'Regen Speed', 'Poison Strength', 'Poison Speed', 'Frost Power']

        output_enchants = {}

        if rarity == "Common":
            return None
        
        if rarity == "Rare":
            return None
        
        if rarity == "Epic":
            no_of_enchants = random.randrange(1, 3)
            suffix = None
            for i in range(no_of_enchants):
                random_enchant = enchants_list[random.randrange(0, len(enchants_list))]
                if suffix is None:
                    suffix = suffix_enchants[random_enchant]
                output_enchants[random_enchant] = random.randrange(1, 6)

        if rarity == "Legendary":
            no_of_enchants = random.randrange(2, 4)
            suffix = None
            for i in range(no_of_enchants):
                random_enchant = enchants_list[random.randrange(0, len(enchants_list))]
                if suffix is None:
                    suffix = suffix_enchants[random_enchant]
                output_enchants[random_enchant] = random.randrange(3, 6)
        
        return (suffix, output_enchants)

    def generate_enemy(self):
        
        base_enemy = self.roll_enemy()
        enemy_name = base_enemy[0]
        enemy_attack = (base_enemy[1]) * (1 + (self.completed_combats * 0.15))
        enemy_speed = base_enemy[2]
        enemy_health = base_enemy[3] * (1 + (self.completed_combats * 0.05))
        enemy_img = self.select_enemy_img(enemy_name)

        return Enemy(enemy_name, enemy_attack, enemy_speed, enemy_health, enemy_img, player=self)

    def roll_enemy(self):

        possible_enemies = [('Crawling Hand', 3, 0.5, 100),
                            ('Bear', 7, 1, 200),
                            ('Cave Slime', 4, 0.75, 150),
                            ('Crab', 5, 1, 250),
                            ('Black Dragon', 20, 3, 300),
                            ('Blue Dragon', 15, 3, 250),
                            ('Red Dragon', 10, 2, 200),
                            ('Green Dragon', 10, 3, 150),
                            ('Bear Patriarch', 15, 2, 250),
                            ('Undead Bear', 15, 2, 250),
                            ('Necromancer', 25, 5, 200),
                            ('Giant Spider', 8, 1, 150),
                            ('Giant Rat', 5, 0.75, 125),
                            ('Ancient Skeleton', 8, 0.8, 200),
                            ('Goblin', 6, 0.75, 150),
                            ('Lizard', 4, 0.35, 125),
                            ('Skeleton', 5, 1, 200),
                            ('Hellhound', 8, 1, 250),
                            ('Wizard', 15, 4, 175),
                            ('Zombie', 8, 1.25, 200),
                            ('Wyvern', 20, 3.5, 300)]
                           
        return possible_enemies[random.randrange(len(possible_enemies))]
    
    def select_enemy_img(self, enemy_name):

        img_options = []
        dimensions = (0,0)

        match enemy_name:
            case "Crawling Hand":
                img_options = ['./images/enemies/Crawling_Hand.png',
                               './images/enemies/Crawling_Hand_2.png',
                               './images/enemies/Crawling_Hand_3.png',
                               './images/enemies/Crawling_Hand_4.png']
                dimensions = (350,300)
                
            case "Bear":
                img_options = ['./images/enemies/Bear.png',
                               './images/enemies/Bear_2.png',
                               './images/enemies/Bear_3.png']
                dimensions = (350,300)

            case "Cave Slime":
                img_options = ['./images/enemies/Cave_Slime.png']
                dimensions = (350,300)

            case "Crab":
                img_options = ['./images/enemies/Crab.png',
                               './images/enemies/Crab_2.png',
                               './images/enemies/Crab_3.png']
                dimensions = (350,300)

            case "Black Dragon":
                img_options = ['./images/enemies/Black_Dragon.png']
                dimensions = (350,300)

            case "Blue Dragon":
                img_options = ['./images/enemies/Blue_Dragon.png',
                               './images/enemies/Blue_Dragon_2.png']
                dimensions = (350,300)

            case "Red Dragon":
                img_options = ['./images/enemies/Red_Dragon.png']
                dimensions = (350,300)

            case "Green Dragon":
                img_options = ['./images/enemies/Green_Dragon.png']
                dimensions = (350,300)

            case "Bear Patriarch":
                img_options = ['./images/enemies/Elite_Bear.png']
                dimensions = (350,300)

            case "Undead Bear":
                img_options = ['./images/enemies/Elite_Bear_2.png']
                dimensions = (350,300)

            case "Necromancer":
                img_options = ['./images/enemies/Elite_Wizard.png']
                dimensions = (250,400)

            case "Giant Spider":
                img_options = ['./images/enemies/Fever_Spider.png']
                dimensions = (350,275)

            case "Giant Rat":
                img_options = ['./images/enemies/Giant_Rat.png']
                dimensions = (350,350)

            case "Ancient Skeleton":
                img_options = ['./images/enemies/Giant_Skeleton.png',
                               './images/enemies/Giant_Skeleton_2.png']
                dimensions = (250,400)

            case "Goblin":
                img_options = ['./images/enemies/Goblin.png',
                               './images/enemies/Goblin_2.png',
                               './images/enemies/Goblin_3.png',
                               './images/enemies/Goblin_4.png']
                dimensions = (250,400)

            case "Lizard":
                img_options = ['./images/enemies/Lizard.png',
                               './images/enemies/Lizard_2.png']
                dimensions = (350,250)

            case "Skeleton":
                img_options = ['./images/enemies/Skeleton.png',
                               './images/enemies/Skeleton_2.png',
                               './images/enemies/Skeleton_3.png']
                dimensions = (200,400)

            case "Hellhound":
                img_options = ['./images/enemies/Terror_Dog.png']
                dimensions = (350,300)

            case "Wizard":
                img_options = ['./images/enemies/Wizard.png']
                dimensions = (150,400)

            case "Wyvern":
                img_options = ['./images/enemies/Elite_Dragon.png']
                dimensions = (300,400)

            case "Zombie":
                img_options = ['./images/enemies/Zombie.png',
                               './images/enemies/Zombie_2.png',
                               './images/enemies/Zombie_3.png']
                dimensions = (200,400)
            
            case _:
                print(f"Something broke, likely a typo with {enemy_name}")
                
        img_path = img_options[random.randrange(len(img_options))]
        return (img_path, dimensions)