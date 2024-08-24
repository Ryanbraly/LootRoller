import threading
import time
import random

class Enemy():

    def __init__(self, name, attack, speed, health, image, player):
        self.name = name
        self.attack = attack
        self.attack_speed = speed
        self.current_health = health
        self.max_health = health
        self.associated_player = player
        self.miss_chance = 0
        self.poison_stacks = 0
        self.poisoned = False
        self.burning = False
        self.frozen = False
        self.blind = False
        self.dead = False
        self.img_path = image[0]
        self.img_dims = image[1]

        self.hp_bar = None

    def enemy_take_damage(self, amount, hp_bar, player, combat_screen):
        self.hp_bar = hp_bar
        self.combat_screen = combat_screen
        if (self.current_health - amount) < 1:
            self.enemy_die()
            return
        else:
            self.current_health -= amount
        if combat_screen.active:    
            hp_bar.set(self.current_health / self.max_health)
            if 'Burning' in player.enchants and player.enchants['Burning'] > 0:
                self.handle_burning(player)
            if 'Poison' in player.enchants and player.enchants['Poison'] > 0:
                self.handle_poison(player)
            if 'Blindness' in player.enchants and player.enchants['Blindness'] > 0:
                self.handle_blindness(player)
            if 'Frost' in player.enchants and player.enchants['Frost'] > 0:
                self.handle_frost(player)
            if 'Vampirism' in player.enchants and player.enchants['Vampirism'] > 0:
                self.handle_lifesteal(player)
            #print(f"{self.name} took {amount} damage!")


    def enemy_die(self):

        self.dead = True
        self.associated_player.completed_combats += 1
        self.associated_player.chest_pity += 1
        self.combat_screen.reset_enemy()
        #print(f"{self.name} has died.")

    def handle_burning(self, player):
        if self.burning == False:
            # defines a bottom bound for the range (maximum chance is 50%, or range(50, 100))
            threshold = (0.1 * player.enchants['Burning']) * 100

            # rolls a random int between 0 and 100 (randrange is not inclusive of the top bound)
            success_roll = random.randrange(0, 101)

            # now that we have a success roll, we can check if it's lower than the bottom bound, which means we can basically use bottom bound
            # as a threshold for successful rolls.  As the bound goes up with enchant levels, your chance of success increases.

            if success_roll > threshold:
                return
            else:
                if self.combat_screen.active:
                    print(f"{self.name} is burning!")
                    self.combat_screen.handle_combat_text("burning")
                    self.burning = True
                    burning_thread = threading.Thread(name='burning', target=self.burn, args=(player,))
                    burning_thread.start()
        else:
            return
        
    def burn(self, player):

        while (self.dead == False):
            burn_damage = int((self.max_health/10) * player.burn_power)
            new_hp = (self.current_health - burn_damage)
            if new_hp < 1:
                self.dead = True
                self.enemy_die()
            else:
                if self.dead == False:
                    self.current_health = new_hp
                    self.combat_screen.handle_damage_popups(burn_damage, '#ff8936')
                    self.hp_bar.set(self.current_health / self.max_health)
                    #self.hp_text.configure(text=f"{self.current_health} / {self.max_health}")
                    time.sleep(player.burn_interval)

    def handle_poison(self, player):
        
            # defines a bottom bound for the range (maximum chance is 50%, or range(50, 100))
            threshold = (0.1 * player.enchants['Poison']) * 100

            # rolls a random int between 0 and 100 (randrange is not inclusive of the top bound)
            success_roll = random.randrange(0, 101)

            # now that we have a success roll, we can check if it's lower than the bottom bound, which means we can basically use bottom bound
            # as a threshold for successful rolls.  As the bound goes up with enchant levels, your chance of success increases.

            if success_roll > threshold:
                return
            else:
                if self.poisoned == False and self.combat_screen.active:
                    print(f"{self.name} is poisoned!")
                    self.combat_screen.handle_combat_text("poisoned")
                    self.poisoned = True
                    self.poison_stacks += 1
                    poison_thread = threading.Thread(name='poison', target=self.poison, args=(player,))
                    poison_thread.start()
                elif self.poisoned == True and self.poison_stacks < 21:
                    self.poison_stacks += 1

    def poison(self, player):

        while (self.dead == False):
            poison_damage = int(((player.attack / 3) * player.poison_power) * self.poison_stacks)
            new_hp = (self.current_health - poison_damage)
            if new_hp < 1:
                self.dead = True
                self.enemy_die()
            else:
                if self.dead == False:
                    self.current_health = new_hp
                    self.combat_screen.handle_damage_popups(poison_damage, '#c1ff63')
                    self.hp_bar.set(self.current_health / self.max_health)
                    #self.hp_text.configure(text=f"{self.current_health} / {self.max_health}")
                    time.sleep(player.poison_interval)

    def handle_frost(self, player):
        
        if self.frozen == False and self.combat_screen.active:
            #print(f"Enemy attack speed started at: {self.attack_speed}")
            self.attack_speed = ((1 + (player.enchants['Frost'] / 10)) * self.attack_speed * (player.frost_power))
            self.frozen = True
            self.combat_screen.handle_combat_text("freeze")
            self.combat_screen.handle_damage_popups("Frozen!", '#63c6ff')
            #print(f"Enemy attack speed is now: {self.attack_speed}")

    def handle_blindness(self, player):
        
        if self.blind == False and self.combat_screen.active:
            self.miss_chance = (player.enchants['Blindness'] * 5)
            self.blind = True
            self.combat_screen.handle_combat_text("blind")
            self.combat_screen.handle_damage_popups("Blinded!", '#c170ff')
            #print("Enemy blinded!")
            #print(f"Enemy miss chance is now: {self.miss_chance}")

    def handle_lifesteal(self, player):
            new_health = int(player.current_health + (player.attack * (player.enchants['Vampirism'] * 0.1)))
            if new_health > player.max_health:
                player.current_health = player.max_health
            else:
                player.current_health = new_health