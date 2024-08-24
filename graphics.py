import customtkinter as ctk
import pickle
from PIL import Image, ImageTk
import threading
import time
import random
import pywinstyles

from gear import Weapon
from player import Player
from enemy import Enemy


class Window(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.geometry("900x1200")
        self.title("Loot Roller")
        self.iconbitmap('./images/chest.ico')
        self.resizable(False, False)   # width, height
        self.name = "Root Window"

    def readjust(self):
        self.geometry("900x1200")

        

class Lobby(ctk.CTkFrame):

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        player = Player()
        player.window_reference = self.master
        self.name = "Lobby"
        self.active = True
        try:
            with open('high_score.dat', 'rb') as file:
                player.high_score = pickle.load(file)
        except:
            player.high_score = 0
        self.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor="center")
        #self.pack()

        def play_button():
            chest_screen = Chest_Screen(master = self.master, player=player)
            self.active = False
            self.destroy()


        scorevar = ctk.StringVar()
        scorevar.set(f"High Score: {player.high_score}")

        # play button
        button = ctk.CTkButton(master=self,
                               text="Play Game",
                               corner_radius=5,
                               command=play_button,
                               fg_color='#E6D97B',
                               hover_color='#D4C875',
                               text_color='#303030',
                               height=350,
                               width=500,
                               font=("Roboto", 76))
        button.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        # title
        title = ctk.CTkLabel(master=self,
                             text="LOOT ROLLER",
                             font=("Roboto", 112))
        title.place(relx=0.5, rely=0.2, anchor=ctk.CENTER)

        # high score block
        high_score = ctk.CTkLabel(master=self,
                                  textvariable=scorevar,
                                  font=("Roboto", 52))
        high_score.place(relx=0.5, rely=0.8, anchor=ctk.CENTER)

                


class Chest_Screen(ctk.CTkFrame):

    def __init__(self, player, master, **kwargs):
        super().__init__(master, **kwargs)
        self.name = "Chest Screen"
        self.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor="center")
        self.active = True


        # Various widget functions 
        def open_chest():
            generated_items = []
            # Regular chest
            if player.opened_chests > 0:
                for i in range(5 + player.luck):
                    generated_item = player.generate_loot()
                    if generated_item not in generated_items:
                        window = Loot_Window(master=self, item=generated_item, player=player)
                        window.title(f"You found: {window.item.name}")
                        generated_items.append(generated_item)
            # First chest     
            else:
                for i in range(5 + player.luck):
                    generated_item = player.generate_loot("weapon")
                    if generated_item not in generated_items:
                        window = Loot_Window(master=self, item=generated_item, player=player)
                        window.title(f"You found: {window.item.name}")
                        generated_items.append(generated_item)
                #cheat_sword = Weapon('Godsword', 150, 0.5, {'Vampirism': 5, 'Blindness': 5}, 5, 'Legendary', string_color='#ff866e')
                #cheaterwindow = Loot_Window(master=self, item=cheat_sword, player=player)
                #cheaterwindow.title(f"Dev item!  Avert your eyes!")

            player.opened_chests += 1
            open_button.destroy()
            help_button.place(relx=0.1, rely=0.933, anchor=ctk.CENTER)
            if player.opened_chests > 1:
                skip_loot_button.place(relx=0.5, rely=0.7, anchor=ctk.CENTER)

        def skip_loot():
            self.active = False
            iterable_dict = dict(self.master.children)
            for child in iterable_dict:
                self.master.children[child].destroy()
            combat_screen = Combat_Screen(master=self.master.master, player=player)

        def open_help():
            help_window = ctk.CTkToplevel()
            help_window.geometry("600x1000")
            help_window.title("Help!")
            help_window.resizable(False, False)
            help_image = ctk.CTkImage(light_image = Image.open('./images/help_screen.png'),
                                   dark_image = Image.open('./images/help_screen.png'),
                                   size = (600,1000))
            help = ctk.CTkLabel(master=help_window,
                                text="",
                                image=help_image)
            help.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
                
                
        # title
        title = ctk.CTkLabel(master=self,
                             text="You've found\na loot chest!\nClick it to open!",
                             font=("Roboto", 88))
        title.place(relx=0.5, rely=0.2, anchor=ctk.CENTER)

        # chest opening button

        chest_image = ctk.CTkImage(light_image = Image.open('./images/lootchest2.png'),
                                   dark_image = Image.open('./images/lootchest2.png'),
                                   size = (600,600))


        open_button = ctk.CTkButton(master=self,
                               text='', 
                               image=chest_image,
                               corner_radius=0,
                               command=open_chest,
                               border_width=0,
                               border_spacing=0,
                               fg_color='#2B2B2B',
                               hover_color='#2B2B2B',
                               text_color='#303030',
                               height=10,
                               width=10,
                               font=("Roboto", 60))
        open_button.place(relx=0.5, rely=0.6, anchor=ctk.CENTER)

        skip_loot_button = ctk.CTkButton(master=self,
                               text="Skip Loot",
                               corner_radius=5,
                               command=skip_loot,
                               fg_color='#E6D97B',
                               hover_color='#D4C875',
                               text_color='#303030',
                               height=100,
                               width=400,
                               font=("Roboto", 60))

        help_button = ctk.CTkButton(master=self,
                               text="?",
                               corner_radius=5,
                               command=open_help,
                               fg_color='#E6D97B',
                               hover_color='#D4C875',
                               text_color='#303030',
                               height=75,
                               width=75,
                               font=("Roboto", 60))




        

class Loot_Window(ctk.CTkToplevel):
    def __init__(self, item, player, *args, **kwargs,):
        super().__init__()
        self.item = item
        self.geometry("450x600 + 4500 + 4500")
        self.title("Loot Roller")
        self.after(250, lambda: self.iconbitmap(self.determine_icon(item)))
        self.resizable(False, False)   # width, height
        self.name = "Loot Window"
        self.focus()
        player.chest_pity = 0

        # Set useful variables for display
        text_color = self.item.color
        enchant_string = self.generate_enchant_string(self.item)
        attack_image = ctk.CTkImage(light_image = Image.open('./images/damage_icon.png'),
                                   dark_image = Image.open('./images/damage_icon.png'),
                                   size = (50,50))
        speed_image = ctk.CTkImage(light_image = Image.open('./images/speed_icon.png'),
                                   dark_image = Image.open('./images/speed_icon.png'),
                                   size = (50,50))
        enchant_image = ctk.CTkImage(light_image = Image.open('./images/enchant_icon.png'),
                                   dark_image = Image.open('./images/enchant_icon.png'),
                                   size = (50,50))
        armor_image = ctk.CTkImage(light_image = Image.open('./images/shield.png'),
                                   dark_image = Image.open('./images/shield.png'),
                                   size = (50,50))
        hp_image = ctk.CTkImage(light_image = Image.open('./images/heart.png'),
                                   dark_image = Image.open('./images/heart.png'),
                                   size = (50,50))
        regen_image = ctk.CTkImage(light_image = Image.open('./images/regen.png'),
                                   dark_image = Image.open('./images/regen.png'),
                                   size = (50,50))


        # Equip item button function
        def equip_item():
            
            if item.slot == 'weapon':
                    equip_weapon()
            else:
                    equip_armor(item.slot)

            iterable_dict = dict(self.master.children)
            for child in iterable_dict:
                self.master.children[child].destroy()
            combat_screen = Combat_Screen(master=self.master.master, player=player)
            

        def add_enchants(addable_enchants):
            
            for key in addable_enchants:
                player.enchants[key] = addable_enchants[key]


        def remove_enchants(removable_enchants):
            
            for key in removable_enchants:
                equipped_value = player.enchants[key]
                player.enchants[key] = (equipped_value - removable_enchants[key])

        def equip_weapon():

            if player.weapon == None:
                # Logic will be expanded later, but for now all we have are weapons
                player.weapon = item
                player.attack += item.damage
                player.attack_speed = item.speed
                player.luck += item.luck
                # Enchants in particular will need more attention when we evolve beyond just weapons
                add_enchants(item.enchants)
                #print("No weapon currently equipped!")
                #print(f"Player stats are now:\nWielding: {player.weapon.name}\nAttack: {player.attack}\nAttack Interval: {player.attack_speed}\nEnchants: {player.enchants}\nLuck: {player.luck}")
            else:
                player.attack -= player.weapon.damage
                player.luck -= player.weapon.luck
                player.luck += item.luck
                player.attack += item.damage
                player.attack_speed = item.speed
                remove_enchants(player.weapon.enchants)
                add_enchants(item.enchants)
                player.weapon = item
                #print(f"Replacing {player.weapon.name}")
                #print(f"Player stats are now:\nWielding: {player.weapon.name}\nAttack: {player.attack}\nAttack Interval: {player.attack_speed}\nEnchants: {player.enchants}\nLuck: {player.luck}")

        def equip_armor(passed_slot):

            attribute_name = {
                'helm': 'helmet',
                'chest': 'chestpiece',
                'legs': 'pants',
                'boots': 'boots',
                'gloves': 'gloves',
                'trinket': 'trinket'
            }.get(passed_slot)

            if attribute_name is None:
                print("Problem assigning attribute_name in equip_armor()")
                return

            current_item = getattr(player, attribute_name)

            if current_item is None:
                #print(f"Slot {passed_slot} was determined to be empty.")
                setattr(player, attribute_name, item)
                #print(f"Equipped {item} in {passed_slot}")
                player.armor += item.defense
                player.max_health += item.hp
                player.current_health += item.hp
                player.regen_amount += item.regen_amount
                player.regen_interval *= item.regen_interval
                player.luck += item.luck
                player.burn_power *= item.burn_power
                player.burn_interval *= item.burn_interval
                player.poison_power *= item.poison_power
                player.poison_interval *= item.poison_interval
                player.frost_power *= item.frost_power

                add_enchants(item.enchants)
                #print(f"Player stats are now:\nWearing: {item.name}\nArmor: {player.armor}\nHP Bonus: {item.hp}\nHP Regen Bonus: {item.regen_amount}\nEnchants: {item.enchants}\nLuck: {player.luck}")
            else:
                #print(f"Unequipping {current_item.name}")
                
                player.armor -= current_item.defense
                player.max_health -= current_item.hp
                player.current_health -= current_item.hp
                player.regen_amount -= current_item.regen_amount
                player.regen_interval /= current_item.regen_interval
                player.luck -= current_item.luck
                if current_item.burn_power > 0:
                    player.burn_power /= current_item.burn_power
                if current_item.burn_interval > 0:
                    player.burn_interval /= current_item.burn_interval
                if current_item.poison_power > 0:
                    player.poison_power /= current_item.poison_power
                if current_item.poison_interval > 0:
                    player.poison_interval /= current_item.poison_interval
                if current_item.frost_power > 0:
                    player.frost_power /= current_item.frost_power
                remove_enchants(current_item.enchants)
                setattr(player, attribute_name, None)
                equip_armor(item.slot)
                #print(f"Player stats are now:\nWielding: {player.weapon.name}\nAttack: {player.attack}\nAttack Interval: {player.attack_speed}\nEnchants: {player.enchants}\nLuck: {player.luck}")            


        if item.slot == 'weapon':
            # Display item name
            item_name_display = ctk.CTkLabel(master=self,
                                text=f"{item.name}",
                                wraplength=450,
                                text_color=text_color,
                                font=("Roboto", 58))
            item_name_display.place(relx=0.5, rely=0.2, anchor=ctk.CENTER)

            # Display item damage
            item_damage_display = ctk.CTkLabel(master=self,
                                text=f"  Damage: {item.damage}",
                                image=attack_image,
                                compound='left',
                                text_color=text_color,
                                wraplength=450,
                                font=("Roboto", 28))
            item_damage_display.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

            # Display attack interval
            item_speed_display = ctk.CTkLabel(master=self,
                                text=f"  Attack Interval: {round(item.speed, 2)} seconds",
                                image=speed_image,
                                compound='left',
                                text_color=text_color,
                                wraplength=450,
                                font=("Roboto", 28))
            item_speed_display.place(relx=0.5, rely=0.6, anchor=ctk.CENTER)

            # Display enchantmnets
            enchants_display = ctk.CTkLabel(master=self,
                                text=f"  Enchantments: {enchant_string}",
                                image=enchant_image,
                                compound='left',
                                text_color=text_color,
                                wraplength=400,
                                font=("Roboto", 28))
            enchants_display.place(relx=0.5, rely=0.7, anchor=ctk.CENTER)

            # Equip Item button
            equip_item_button = ctk.CTkButton(master=self,
                                text="Equip Item",
                                corner_radius=5,
                                command=equip_item,
                                fg_color='#E6D97B',
                                hover_color='#D4C875',
                                text_color='#303030',
                                height=75,
                                width=250,
                                font=("Roboto", 48))
            equip_item_button.place(relx=0.5, rely=0.9, anchor=ctk.CENTER)


        if item.slot != 'weapon':

            # Display item name
            item_name_display = ctk.CTkLabel(master=self,
                                text=f"{item.name}",
                                wraplength=450,
                                text_color=text_color,
                                font=("Roboto", 48))
            item_name_display.place(relx=0.5, rely=0.15, anchor=ctk.CENTER)

            # Display item armor
            item_armor_display = ctk.CTkLabel(master=self,
                                text=f"  Armor: {item.defense}",
                                image=armor_image,
                                compound='left',
                                text_color=text_color,
                                wraplength=450,
                                font=("Roboto", 28))
            item_armor_display.place(relx=0.5, rely=0.4, anchor=ctk.CENTER)

            # Display HP bonus
            item_hp_display = ctk.CTkLabel(master=self,
                                text=f"  HP: {item.hp}",
                                image=hp_image,
                                compound='left',
                                text_color=text_color,
                                wraplength=450,
                                font=("Roboto", 28))
            item_hp_display.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

            # Display HP regen bonus
            item_regen_display = ctk.CTkLabel(master=self,
                                text=f"  HP Regen: +{item.regen_amount}",
                                image=regen_image,
                                compound='left',
                                text_color=text_color,
                                wraplength=450,
                                font=("Roboto", 28))
            item_regen_display.place(relx=0.5, rely=0.6, anchor=ctk.CENTER)

            # Display enchantments
            enchants_display = ctk.CTkLabel(master=self,
                                text=f"  Enchantments: {enchant_string}",
                                image=enchant_image,
                                compound='left',
                                text_color=text_color,
                                wraplength=400,
                                font=("Roboto", 28))
            enchants_display.place(relx=0.5, rely=0.7, anchor=ctk.CENTER)

            # Equip Item button
            equip_item_button = ctk.CTkButton(master=self,
                                text="Equip Item",
                                corner_radius=5,
                                command=equip_item,
                                fg_color='#E6D97B',
                                hover_color='#D4C875',
                                text_color='#303030',
                                height=75,
                                width=250,
                                font=("Roboto", 48))
            equip_item_button.place(relx=0.5, rely=0.9, anchor=ctk.CENTER)

    def determine_icon(self, item):
        if item.rarity == "Common":
            return "./images/common.ico"
        elif item.rarity == "Rare":
            return "./images/rare.ico"
        elif item.rarity == "Epic":
            return "./images/epic.ico"
        elif item.rarity == "Legendary":
            return "./images/legendary.ico"

        
    def generate_enchant_string(self, item):
        enchant_string = ""
        if len(item.enchants) > 0:
            for enchant in item.enchants:
                enchant_string += f"{enchant} {item.enchants[enchant]}, "
            enchant_string = enchant_string[:-2]
            return enchant_string
        else:
            return "None"
        

class Combat_Screen(ctk.CTkFrame):

    def __init__(self, player, master, **kwargs):
        super().__init__(master, **kwargs)
        self.name = "Combat Screen"
        self.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor="center")
        self.current_enemy = player.generate_enemy()
        self.player = player
        self.list_of_lines = []
        self.clicked = False
        self.active = True

        #print(player.enchants)
        
        #print(player.window_reference.children)
        #print(self.player.regenerating)
      

        
        def pick_tooltip_text():

            possible_slots = ['helmet', 'chestpiece', 'pants', 'boots', 'gloves', 'trinket']

            for slot in possible_slots:


                match slot:

                    case 'trinket':
                        comparator = getattr(player, slot)
                        if comparator is None:
                            trinket_name_text.configure(text='No item equipped in this slot!')
                            trinket_stats_text.configure(text='')
                        else:
                            trinket_name_text.configure(text=f'{player.trinket.name}')
                            trinket_name_text.configure(text_color=player.trinket.color)
                            trinket_stats_text.configure(text=f'Armor: {player.trinket.defense}  |  HP: {player.trinket.hp}\nRegen: {player.trinket.regen_amount}')
                            trinket_stats_text.configure(text_color=player.trinket.color)

                    case 'helmet':
                        comparator = getattr(player, slot)
                        if comparator is None:
                            helm_name_text.configure(text='No item equipped in this slot!')
                            helm_stats_text.configure(text='')
                        else:
                            helm_name_text.configure(text=f'{player.helmet.name}')
                            helm_name_text.configure(text_color=player.helmet.color)
                            helm_stats_text.configure(text=f'Armor: {player.helmet.defense}  |  HP: {player.helmet.hp}\nRegen: {player.helmet.regen_amount}')
                            helm_stats_text.configure(text_color=player.helmet.color)

                    case 'chestpiece':
                        comparator = getattr(player, slot)
                        if comparator is None:
                            top_name_text.configure(text='No item equipped in this slot!')
                            top_stats_text.configure(text='')
                        else:
                            top_name_text.configure(text=f'{player.chestpiece.name}')
                            top_name_text.configure(text_color=player.chestpiece.color)
                            top_stats_text.configure(text=f'Armor: {player.chestpiece.defense}  |  HP: {player.chestpiece.hp}\nRegen: {player.chestpiece.regen_amount}')
                            top_stats_text.configure(text_color=player.chestpiece.color)

                    case 'pants':
                        comparator = getattr(player, slot)
                        if comparator is None:
                            legs_name_text.configure(text='No item equipped in this slot!')
                            legs_stats_text.configure(text='')
                        else:
                            legs_name_text.configure(text=f'{player.pants.name}')
                            legs_name_text.configure(text_color=player.pants.color)
                            legs_stats_text.configure(text=f'Armor: {player.pants.defense}  |  HP: {player.pants.hp}\nRegen: {player.pants.regen_amount}')
                            legs_stats_text.configure(text_color=player.pants.color)
                    
                    case 'boots':
                        comparator = getattr(player, slot)
                        if comparator is None:
                            boots_name_text.configure(text='No item equipped in this slot!')
                            boots_stats_text.configure(text='')
                        else:
                            boots_name_text.configure(text=f'{player.boots.name}')
                            boots_name_text.configure(text_color=player.boots.color)
                            boots_stats_text.configure(text=f'Armor: {player.boots.defense}  |  HP: {player.boots.hp}\nRegen: {player.boots.regen_amount}')
                            boots_stats_text.configure(text_color=player.boots.color)

                    case 'gloves':
                        comparator = getattr(player, slot)
                        if comparator is None:
                            gloves_name_text.configure(text='No item equipped in this slot!')
                            gloves_stats_text.configure(text='')
                        else:
                            gloves_name_text.configure(text=f'{player.gloves.name}')
                            gloves_name_text.configure(text_color=player.gloves.color)
                            gloves_stats_text.configure(text=f'Armor: {player.gloves.defense}  |  HP: {player.gloves.hp}\nRegen: {player.gloves.regen_amount}')
                            gloves_stats_text.configure(text_color=player.gloves.color)

        def initiate_combat():
            if self.clicked:
                pass
            else:
                player_attack_thread = threading.Thread(name='player_attack', target=player_attack_loop)
                player_attack_thread.start()
                #player_attack_loop()

                enemy_attack_thread = threading.Thread(name='enemy_attack', target=enemy_attack_loop)
                enemy_attack_thread.start()

                self.clicked = True


        # COMBAT
         
        def player_attack_loop():
            while self.player.dead == False and self.current_enemy is not None: 
                time.sleep(player.attack_speed)         
                if self.current_enemy is not None and self.active:
                    self.handle_damage_popups(self.player.attack, '#DCE4EE')
                    self.current_enemy.enemy_take_damage(player.attack, self.enemy_hpbar, self.player, self)                  
                else:
                    break
                

        def enemy_attack_loop():
            while self.player.dead == False and self.current_enemy is not None:
                time.sleep(self.current_enemy.attack_speed)
                if self.current_enemy and self.current_enemy.dead == False:
                    if random.randrange(1,101) >= self.current_enemy.miss_chance:
                        damage_taken = self.player.take_damage(self.current_enemy.attack, hpbar, HP_bar_text, self)
                        if self.player.dead == False and self.name == "Combat Screen":
                            pass
                        else:
                            break
                    else:
                        if self.active:
                            self.handle_combat_text("enemy_miss", self.player.enchants["Blindness"])
                else:
                    break
        
        # Player HP bar - !ctkprogressbar
        hpbar = ctk.CTkProgressBar(master=self, corner_radius=32, progress_color='#FF3357', fg_color='#303030', width=750, height=75)
        hpbar.set(self.player.current_health /self. player.max_health)
        hpbar.place(relx=0.5, rely=0.49, anchor=ctk.CENTER)

        # Display current / max HP under player HP bar - !ctklabel2
        HP_bar_text = ctk.CTkLabel(master=self,
                             text=f"{self.player.current_health} / {self.player.max_health}",
                             wraplength=750,
                             text_color='#FF3357',
                             font=("Roboto", 32))
        HP_bar_text.place(relx=0.5, rely=0.54, anchor=ctk.CENTER)

        # Combat text frame - !ctkframe
        combat_frame = ctk.CTkFrame(master=self, fg_color='#303030', width = 350, height = 500, border_width = 2, border_color='#ADADAD')
        combat_frame.place(relx=0.75, rely=0.23, anchor=ctk.CENTER)

        # Combat textbox
        self.combat_text = ctk.CTkTextbox(master=self, padx=5, fg_color='#303030', 
                                          width = 345, height = 495, wrap='word', 
                                          corner_radius=0, font=("Roboto", 24),
                                          scrollbar_button_color='#E6D97B', scrollbar_button_hover_color='#D4C875')
        self.combat_text.configure(state='disabled')
        self.combat_text.place(relx=0.75, rely=0.23, anchor=ctk.CENTER)

        

    
        #  Enemy Image - Not listed in self.children, interestingly - I assume because it's a CTk item, but not a widget
        self.enemy_image = ctk.CTkImage(#light_image = Image.open(self.current_enemy.img_path),
                                   dark_image = Image.open(self.current_enemy.img_path),
                                   size = self.current_enemy.img_dims)

        # Enemy Button - !ctkbutton
        self.enemy_button = ctk.CTkButton(master=self,
                               text='', 
                               image=self.enemy_image,
                               corner_radius=0,
                               command=initiate_combat,
                               border_width=0,
                               border_spacing=0,
                               border_color='#2B2B2B',
                               fg_color='#2B2B2B',
                               hover_color='#2B2B2B',
                               text_color='#303030',
                               height=10,
                               width=10,
                               font=("Roboto", 60))
        self.enemy_button.place(relx=0.25, rely=0.24, anchor=ctk.CENTER)


        # Enemy HP bar - !ctkprogressbar2
        self.enemy_hpbar = ctk.CTkProgressBar(master=self, corner_radius=32, progress_color='#FF3357', fg_color='#303030', width=200, height=25)
        self.enemy_hpbar.set(self.current_enemy.current_health / self.current_enemy.max_health)
        self.enemy_hpbar.place(relx=0.25, rely=0.05, anchor=ctk.CENTER)

        # Inventory frame
        self.inventory_frame = ctk.CTkFrame(master=self, fg_color='#303030', width = 875, height = 500, border_width = 2, border_color='#ADADAD')
        self.inventory_frame.place(relx=0.5, rely=0.78, anchor=ctk.CENTER)
        self.inventory_frame.grid_columnconfigure((0, 1), weight=1)

        # Inventory title - 1
        inventory_title = ctk.CTkLabel(master=self.inventory_frame, fg_color='#303030', text="Inventory", font=("Roboto", 50))
        inventory_title.grid(row=0, column=0, padx=20, pady=20, sticky='w')




        # Weapon title - 2
        weapon_title = ctk.CTkLabel(master=self.inventory_frame, fg_color='#303030', text="Weapon:", font=("Roboto", 30))
        weapon_title.grid(row=1, column=0, padx=15, pady=5, sticky='w')

        # Weapon name - 3
        weapon_name_text = ctk.CTkLabel(master=self.inventory_frame, fg_color='#303030', text=f"{player.weapon.name}", text_color=f'{player.weapon.color}', wraplength= 175, font=("Roboto", 20))
        weapon_name_text.grid(row=2, column=0, padx=15, pady=5, sticky='w')

        # Weapon stats - 4
        weapon_stats_text = ctk.CTkLabel(master=self.inventory_frame, fg_color='#303030', text=f"Damage: {player.weapon.damage}  |  Speed: {round(player.weapon.speed, 2)}", 
                                       text_color=f'{player.weapon.color}', font=("Roboto", 16))
        weapon_stats_text.grid(row=3, column=0, padx=15, pady=(5, 20), sticky='w')



        # Trinket title - 5 
        trinket_title = ctk.CTkLabel(master=self.inventory_frame, fg_color='#303030', text="Trinket:", font=("Roboto", 30))
        trinket_title.grid(row=4, column=0, padx=15, pady=5, sticky='w')

        # Trinket name - 6
        trinket_name_text = ctk.CTkLabel(master=self.inventory_frame, fg_color='#303030', text='', text_color='#ADADAD', wraplength=175, font=("Roboto", 20))
        trinket_name_text.grid(row=5, column=0, padx=15, pady=5, sticky='w')

        # Trinket stats - 7
        trinket_stats_text = ctk.CTkLabel(master=self.inventory_frame, fg_color='#303030', text='', 
                                       text_color='#ADADAD', font=("Roboto", 16))
        trinket_stats_text.grid(row=6, column=0, padx=15, pady=(5, 20), sticky='w')



        # Helm title - 8 
        helm_title = ctk.CTkLabel(master=self.inventory_frame, fg_color='#303030', text="Helmet:", font=("Roboto", 30))
        helm_title.grid(row=0, column=1, padx=15, pady=5, sticky='w')

        # Helm name - 9 
        helm_name_text = ctk.CTkLabel(master=self.inventory_frame, fg_color='#303030', text='', text_color='#ADADAD', wraplength=175, font=("Roboto", 20))
        helm_name_text.grid(row=1, column=1, padx=15, pady=5, sticky='w')

        # Helm stats - 10
        helm_stats_text = ctk.CTkLabel(master=self.inventory_frame, fg_color='#303030', text='', 
                                       text_color='#ADADAD', font=("Roboto", 16))
        helm_stats_text.grid(row=2, column=1, padx=15, pady=(5, 20), sticky='w')


        # Top title - 11
        top_title = ctk.CTkLabel(master=self.inventory_frame, fg_color='#303030', text="Top:", font=("Roboto", 30))
        top_title.grid(row=3, column=1, padx=15, pady=5, sticky='w')

        # Top name - 12
        top_name_text = ctk.CTkLabel(master=self.inventory_frame, fg_color='#303030', text='', text_color='#ADADAD', wraplength=175, font=("Roboto", 20))
        top_name_text.grid(row=4, column=1, padx=15, pady=5, sticky='w')

        # Top stats - 13
        top_stats_text = ctk.CTkLabel(master=self.inventory_frame, fg_color='#303030', text='', 
                                       text_color='#ADADAD', font=("Roboto", 16))
        top_stats_text.grid(row=5, column=1, padx=15, pady=(5, 20), sticky='w')



        # Legs title - 14
        legs_title = ctk.CTkLabel(master=self.inventory_frame, fg_color='#303030', text="Legs:", font=("Roboto", 30))
        legs_title.grid(row=0, column=2, padx=15, pady=5, sticky='w')

        # Legs name - 15
        legs_name_text = ctk.CTkLabel(master=self.inventory_frame, fg_color='#303030', text='', text_color='#ADADAD', wraplength=175, font=("Roboto", 20))
        legs_name_text.grid(row=1, column=2, padx=15, pady=5, sticky='w')

        # Legs stats - 16
        legs_stats_text = ctk.CTkLabel(master=self.inventory_frame, fg_color='#303030', text='', 
                                       text_color='#ADADAD', font=("Roboto", 16))
        legs_stats_text.grid(row=2, column=2, padx=15, pady=(5, 20), sticky='w')



        # Gloves title - 17
        gloves_title = ctk.CTkLabel(master=self.inventory_frame, fg_color='#303030', text="Gloves:", font=("Roboto", 30))
        gloves_title.grid(row=3, column=2, padx=15, pady=5, sticky='w')

        # Gloves name - 18
        gloves_name_text = ctk.CTkLabel(master=self.inventory_frame, fg_color='#303030', text='', text_color='#ADADAD', wraplength=175, font=("Roboto", 20))
        gloves_name_text.grid(row=4, column=2, padx=15, pady=5, sticky='w')

        # Gloves stats - 19
        gloves_stats_text = ctk.CTkLabel(master=self.inventory_frame, fg_color='#303030', text='', 
                                       text_color='#ADADAD', font=("Roboto", 16))
        gloves_stats_text.grid(row=5, column=2, padx=15, pady=(5, 20), sticky='w')



        # Boots title - 20
        boots_title = ctk.CTkLabel(master=self.inventory_frame, fg_color='#303030', text="Boots:", font=("Roboto", 30))
        boots_title.grid(row=0, column=3, padx=15, pady=5, sticky='w')

        # Boots name - 21
        boots_name_text = ctk.CTkLabel(master=self.inventory_frame, fg_color='#303030', text='', text_color='#ADADAD', wraplength=175, font=("Roboto", 20))
        boots_name_text.grid(row=1, column=3, padx=15, pady=5, sticky='w')

        # Boots stats - 22
        boots_stats_text = ctk.CTkLabel(master=self.inventory_frame, fg_color='#303030', text='', 
                                       text_color='#ADADAD', font=("Roboto", 16))
        boots_stats_text.grid(row=2, column=3, padx=15, pady=(5, 20), sticky='w')


        # Totals title - 23
        boots_title = ctk.CTkLabel(master=self.inventory_frame, fg_color='#303030', text="Total:", font=("Roboto", 30))
        boots_title.grid(row=3, column=3, padx=15, pady=5)

        # Total armor - 24
        total_armor_text = ctk.CTkLabel(master=self.inventory_frame, fg_color='#303030', text=f'Armor: {self.player.armor}', text_color='#ADADAD', wraplength=175, font=("Roboto", 20))
        total_armor_text.grid(row=4, column=3, padx=15, pady=5,)

        # Total regen - 25
        total_armor_text = ctk.CTkLabel(master=self.inventory_frame, fg_color='#303030', text=f'Regen:\n{self.player.regen_amount} / {self.player.regen_interval} seconds', text_color='#ADADAD', wraplength=200, font=("Roboto", 20))
        total_armor_text.grid(row=5, column=3, padx=15, pady=5)


        # Total score - 26
        total_armor_text = ctk.CTkLabel(master=self.inventory_frame, fg_color='#303030', text=f'Enemies killed:\n{self.player.completed_combats}', text_color='#ADADAD', wraplength=175, font=("Roboto", 20))
        total_armor_text.grid(row=6, column=3, padx=15, pady=5,)


        # Start HP regen on Combat Screen initialize
        

        pick_tooltip_text()
        
        player.hp_bar = hpbar
        player.hp_text = HP_bar_text

        self.player.open_regen_thread()



    def draw_death_screen(self):
        self.active = False
        death_screen = Death_Screen(master=self.master, player=self.player)

    def draw_loot_screen(self):
        self.active = False
        loot_screen = Chest_Screen(master=self.master, player=self.player)
        self.inventory_frame.destroy()
        self.destroy()
    

    # Enemy image button

    def reset_enemy(self):
        self.current_enemy = None
        # check for a chest screen spawn
        if random.randrange(0, 11) < self.player.chest_pity:
            self.draw_loot_screen()
            return
        else:
            ei_trash_collect = self.enemy_image
            del ei_trash_collect
            self.current_enemy = self.player.generate_enemy()
            self.update_enemy_button()
            self.update_enemy_hp_bar()
            self.enemy_button.configure(image=self.enemy_image)

    def update_enemy_button(self):

        self.enemy_image.configure(#light_image = Image.open(self.current_enemy.img_path),
                                dark_image = Image.open(self.current_enemy.img_path),
                                size = self.current_enemy.img_dims)
                                 
                                   
    def update_enemy_hp_bar(self):

        self.enemy_hpbar.set(self.current_enemy.current_health / self.current_enemy.max_health)

    def handle_damage_popups(self, damage, color):
        dmg = damage
        popup = Damage_Popup(master=self, damage=dmg, color=color)

    def handle_combat_text(self, message_type, value=0):

        if self.active:
            match message_type:

                case "burning":
                    self.combat_text.configure(state="normal")
                    self.combat_text.insert("end", f"{self.current_enemy.name} is burning!\n")
                    self.combat_text.configure(state="disabled")

                case "freeze":
                    self.combat_text.configure(state="normal")
                    self.combat_text.insert("end", f"{self.current_enemy.name} is coated in frost!\n")
                    self.combat_text.configure(state="disabled")

                case "blind":
                    self.combat_text.configure(state="normal")
                    self.combat_text.insert("end", f"{self.current_enemy.name} has been blinded!\n")
                    self.combat_text.configure(state="disabled")
                    
                case "poisoned":
                    self.combat_text.configure(state="normal")
                    self.combat_text.insert("end", f"{self.current_enemy.name} is poisoned!\n")
                    self.combat_text.configure(state="disabled")
                    
                case "enemy_damage":
                    self.combat_text.configure(state="normal")
                    self.combat_text.insert("end", f"{self.current_enemy.name} deals {value} damage\n")
                    self.combat_text.configure(state="disabled")
                    self.combat_text.see('end')

                case "enemy_miss":
                    self.combat_text.configure(state="normal")
                    self.combat_text.insert("end", f"{self.current_enemy.name} fails to hit you!\n")
                    self.combat_text.configure(state="disabled")

                case _:
                    print("Attempted to send a combat text window message that shouldn't be possible")
       

    

class Death_Screen(ctk.CTkFrame):

    def __init__(self, player, master, **kwargs):
        super().__init__(master, **kwargs)
        self.name = "Oh dear!  You are dead!"
        self.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor="center")
        self.player = player
        self.active = True

        def retry_button():
            lobby = Lobby(master=self.master)
            self.destroy()

        # play button
        try_again_button = ctk.CTkButton(master=self,
                               text="Return to Title",
                               corner_radius=5,
                               command=retry_button,
                               fg_color='#E6D97B',
                               hover_color='#D4C875',
                               text_color='#303030',
                               height=250,
                               width=400,
                               font=("Roboto", 60))
        try_again_button.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        # title
        title = ctk.CTkLabel(master=self,
                             text="YOU DIED",
                             font=("Roboto", 76))
        title.place(relx=0.5, rely=0.2, anchor=ctk.CENTER)

        # high score block
        score_text = ctk.CTkLabel(master=self,
                                  text='',
                                  font=("Roboto", 52))
        score_text.place(relx=0.5, rely=0.8, anchor=ctk.CENTER)

        self.handle_scoring(score_text)

    def handle_scoring(self, score_text):
        prev_high_score = self.player.high_score
        current_high_score = self.player.completed_combats
        if current_high_score > prev_high_score:
            with open('high_score.dat', 'wb') as file:
                pickle.dump(current_high_score, file)
            score_text.configure(text=f'NEW HIGH SCORE!\n{current_high_score}')
        else:
            score_text.configure(text=f'Final Score: {current_high_score}')


class Damage_Popup(ctk.CTkLabel):

    def __init__(self, master, damage, color='#DCE4EE', *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        dmgvar = ctk.StringVar()
        if type(damage) is int:
            dmgvar.set(f"-{damage}")
        else:
            dmgvar.set(damage)

        self.configure(text=dmgvar.get())   
        self.configure(fg_color='#000001') 
        self.configure(text_color=color) 
        self.configure(font=("Roboto", 50)) 

        self.x_var = random.uniform(.15, .35)
        self.y_var = random.uniform(.14, .34)

        self.place(relx=self.x_var, rely=self.y_var, anchor=ctk.CENTER)  
        pywinstyles.set_opacity(self, color="#000001") 
        crunch_thread = threading.Thread(name='damage_popup', target=self.crunch)
        crunch_thread.start()

    def crunch(self):
        time.sleep(0.6)
        self.destroy()
