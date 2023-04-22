import sys
sys.path.append('D:/Users/Murph Strange/Jupyter Notebook/')
import menus
import random
import types

class Character:
    def __init__(self, name):
        self.name = name
        self.strength = 16
        self.intellect = 16
        self.resilience = 16
        
        #ability to run away (TODO: implement Escape action?)
        self.agility = 16

        self.max_hp = 16
        self.hp = self.max_hp
        self.max_mp = 16
        self.mp = self.max_mp

        self.attack_power = 0
        self.defense_power = 0

        self.equipment = {
            "weapon": False,
            "armor": False,
            "shield": False
        }
        self.status = []
        self.inventory = {}
        self.spellbook = {}

    def alive(self):
        if "deceased" not in self.status:
            return True

        else:
            print("%s is a corpse.\n" % self.name)
            return False

    def health(self, change = 0):
        self.hp += change
        if change == 0:
            return self.hp

        elif self.alive() and (change < 0):
            print("%s takes %d damage.\n" % (self.name, abs(change)))
            if self.hp < 1:
                self.hp = 0
                print("%s has died.\n" % self.name)
                self.status = ["deceased"]

            return True

        elif self.alive() and (change > 0):
            print("%s restores %d hp.\n" % (self.name, change))
            if self.hp > self.max_hp:
                self.hp = self.max_hp
                print("%s's health is fully restored!\n" % self.name)

            return True

        else:
            return False

    def magic(self, change = 0):
        if change == 0:
            return self.mp

        elif self.alive() and (change < 0):
            if abs(change) > self.mp:
                print("%s doesn't have enough magic!\n" % self.name)
                return False

            else:
                self.mp += change
                print("%s expends %d magic.\n" % (self.name, abs(change)))
                if self.mp < 1:
                    self.mp = 0
                    print("%s has depleted their magic.\n" % self.name)

                return True

        elif self.alive() and (change > 0):
            self.mp += change
            print("%s restores %d  mp.\n" % (self.name, change))
            if self.mp > self.max_mp:
                self.mp = self.max_mp
                print("%s's magic has been fully restored!\n" % self.name)

            return True

        else:
            return False

    def drink(self, item):
        if item in self.inventory.keys():
            return self.inventory[item].drink(self)

        else:
            print("%s can't drink a %s.\n" % (self.name, item))
            return False

    def equip(self, item):
        if item in self.inventory.keys():
            return self.inventory[item].equip(self)

        else:
            print("%s can't equip a %s.\n" % (self.name, item))
            return False

    def attack(self, target):
        if self.equipment["weapon"]:
            return self.equipment["weapon"].attack(self, target)

        else:
            print("%s is unarmed.\n" % self.name)
            return False

    def defend(self):
        return self.defense_power

    def cast(self, spell, target):
        if spell in self.spellbook.keys():
            print("%s casts %s.\n" % (self.name, spell))
            return self.spellbook[spell].cast(target, self)

        else:
            print("%s can't cast %s.\n" % (self.name, spell))
            return False

    def speak(self, target):
        #Options to converse, trade, engage in combat
        pass

class NPCharacter(Character):
    def __init__(self, name):
        super().__init__(name)
        pass

    def health(self, change = 0):
        res = super().health(change)
        if self.alive() and self.hp < int(self.max_hp/3):
            self.drink("red potion")

        return res

    def magic(self, change = 0):
        res = super().magic(change)
        if self.alive() and self.mp < int(self.max_mp/3):
            self.drink("blue potion")

        return res

    def speak(self, target):
        #Options to converse, trade, or engage in combat
        #overwrite this method with the dialog menus of
        #your choice, using menus and types.MethodType()
        print("%s says" % self.name)
        dialog = menus.Menu('"Continue?"', ['y', 'n'])
        res = dialog.display_prompt()
        return res

class PlayerCharacter(Character):
    def __init__(self, name):
        super().__init__(name)

        self.gold = 100
        self.level = 1
        self.xp = 0
        self.quest_flags = {}

    def speak(self, target):
        if self.alive() and target.alive():
            if type(target) == PlayerCharacter:
                #player character options (trade? duel? invite to party?)
                pass

            elif type(target) == NPCharacter:
                #invoke npc's menus for dialog,
                #changes depending on what the 
                #npc is (foe, merchant, quest giver) 
                return target.speak(self)

            else:
                print("%s can't speak to that.\n" % self.name)
                return False

        else:
            print("%s can't speak to %s.\n" % (self.name, target.name))
            return False

class MonsterCharacter(NPCharacter):
    def __init__(self, name, health, magic, attack_power, defense_power, agility, xp, gold, spell_list = []):
        super().__init__(name)
        
        self.max_hp = health
        self.hp = self.max_hp
        self.max_mp = magic
        self.mp = self.max_mp

        self.attack_power = attack_power
        self.defense_power = defense_power
        self.agility = agility

        self.xp = xp
        self.gold = gold
        
        for item in spell_list:
            self.spellbook[item] = Spell(item, spells[item][0], spells[item][1], spells[item][2])
            
    def attack(self, target):
        if self.equipment["weapon"]:
            return self.equipment["weapon"].attack(self, target)
            
        else:
            if self.alive() and target.alive():
                damage = random.randint(int((self.strength + self.attack_power)/3), self.strength + self.attack_power)
                print("%s attacks %s!\n" % (self.name, target.name))
                if random.randint(0, 7) in [3, 5]:
                    print("%s misses!\n" % self.name)
                    damage = 0

                else:
                    print("%s deals %d damage.\n" % (self.name, damage))
                    target_defense = target.defend()
                    if target.equipment["shield"]:
                        target_defense += target.equipment["shield"].defend()

                    if target.equipment["armor"]:
                        target_defense += target.equipment["armor"].defend()

                    resist = random.randint(int((target.resilience + target_defense)/3), target.resilience + target_defense)
                    print("%s has a defense rating of %d.\n" % (target.name, target_defense))
                    print("%s resists %d damage.\n" % (target.name, resist))
                    damage -= resist
                    if damage <= 0:
                        damage = 0
                        print("%s blocks the attack!\n" % target.name)

                target.health(-damage)
                return True

            else:
                return False
                                
class Effect():
    def __init__(self, name, power):
        self.name = name
        self.power = power
        
class Potion(Effect):
    def __init__(self, name, attribute, power, quantity = 0):
        super().__init__(name, power)
        self.attribute = attribute
        self.quantity = quantity

    def pay(self, caster):
        if caster.inventory[self.name].quantity > 0:
            caster.inventory[self.name].quantity -= 1
            return True

        else:
            print("%s has no %s left.\n" % (caster.name, self.name))
            return False

    def drink(self, caster):
        if caster.alive() and self.pay(caster):
            print("%s drinks a %s.\n" % (caster.name, self.name))
            if self.attribute == 'hp':
                caster.health(self.power)

            elif self.attribute == 'mp':
                caster.magic(self.power)

            return True

        else:
            return False

class Spell(Effect):
    def __init__(self, name, cost, power, status = 'none'):
        super().__init__(name, power)
        self.cost = cost
        self.status = status

    def pay(self, caster):
        if caster.magic() > self.cost:
            caster.magic(-self.cost)
            return True

        else:
            return False

    def cast(self, target, caster):
        if caster.alive() and target.alive() and self.pay(caster):
            damage = random.randint(int((caster.intellect + self.power)/2), caster.intellect + self.power)
            print("%s deals %d damage.\n" % (self.name.capitalize(), damage))
            if self.status in target.status:
                resist = random.randint(int((target.intellect + target.resilience)/2), target.intellect + target.resilience)

            else:
                resist = random.randint(0, int((target.intellect + target.resilience)/2))
                if target.alive() and ((damage - resist) > 0) and not self.status == 'none' and self.status not in target.status:
                    target.status.append(self.status)
                    
            print("%s resists %d damage.\n" % (target.name, resist))
            damage -= resist
            if damage <= 0:
                damage = 0
                print("%s is ineffective!\n" % self.name.capitalize())

            target.health(-damage)
            return True

        else:
            return False

class Equipment(Effect):
    def __init__(self, name, power, slot):
        super().__init__(name, power)
        self.slot = slot

    def equip(self, caster):
        if caster.alive() and self.name in caster.inventory.keys():
            if caster.equipment[self.slot]:
                caster.inventory.append(caster.equipment[self.slot])

            caster.equipment[self.slot] = self
            caster.inventory.pop(self.name)
            print("%s equips the %s.\n" % (caster.name, self.name))
            return True

        else:
            return False

    def defend(self):
        return self.power

class Weapon(Equipment):
    def __init__(self, name, power):
        super().__init__(name, power, "weapon")

    def attack(self, caster, target):
        if caster.alive() and target.alive():
            damage = random.randint(int((caster.strength + self.power)/3), caster.strength + self.power)
            print("%s attacks %s with %s.\n" % (caster.name, target.name, self.name))
            if random.randint(0, 7) == 3:
                print("%s misses!\n" % caster.name)
                damage = 0

            else:
                print("%s deals %d damage.\n" % (self.name, damage))
                target_defense = 0
                if target.equipment["shield"]:
                    target_defense += target.equipment["shield"].defend()

                if target.equipment["armor"]:
                    target_defense += target.equipment["armor"].defend()

                resist = random.randint(int((target.resilience + target_defense)/3), target.resilience + target_defense)
                print("%s has a defense rating of %d.\n" % (target.name, target_defense))
                print("%s resists %d damage.\n" % (target.name, resist))
                damage -= resist
                if damage <= 0:
                    damage = 0
                    print("%s blocks the attack!\n" % target.name)

            target.health(-damage)
            return True

        else:
            return False

weapons = {
    "Bamboo Pole": 2, #10
    "Club": 4, #60
    "Copper Sword": 10, #180
    "Hand Axe": 15, #560
    "Broad Sword": 20, #1500
    "Flame Sword": 28, #9800
    "Erdrick's Sword": 40 #0
}

armor = {
    "Clothes": 2, #50
    "Leather Armor": 4, #40
    "Chain Mail": 12, #300
    "Half Plate": 16, #1000
    "Full Plate": 24, #3000
    "Magic Armor": 24, #7700
    "Erdrick's Armor": 28 #0
}

shields = {
    "Leather Shield": 4, #90
    "Iron Shield": 10, #800
    "Silver Shield": 24 #14800
}

spells = {
    "zap": (1, 2, 'none'),
    "fireball": (2, 4, 'burning'),
    "blizzard": (4, 8, 'freezing'),
    "lightning": (8, 12, 'shocked')
}

potions = {
    "red potion": (8, 'hp'),
    "blue potion": (8, 'mp')
}

monsters = {
    "slime": (3, 0, 5, 3, 2, 1, 2, []),
    "she-slime":(4, 0, 7, 3, 4, 2, 4, []),
    "dracky": (6, 0, 9, 6, 5, 3, 6, []),
    "ghost": (7, 0, 11, 8, 6, 4, 8, []),
    "prestidigitator": (12, 8, 8, 12, 6, 8, 16, ["zap"]),
    "drackolyte": (15, 8, 13, 13, 8, 12, 20, ["zap"]),
    "scorpion": (20, 0, 18, 35, 4, 16, 25, []),
    "skeleton": (30, 0, 28, 22, 17, 25, 42, []),
    "lunatick": (22, 0, 22, 18, 11, 14, 21, []),
    "fightgeist": (23, 10, 18, 20, 14, 15, 19,["fireball"]),
    "drohl drone": (35, 0, 24, 6, 9, 18, 30, []),
    "drackyma":(20, 10, 22, 26, 16, 20, 25, ["fireball"]),
    "legerdeman": (28, 10, 26, 24, 15, 28, 50, ["fireball"]),
    "bewarewolf": (34, 0, 40, 30, 21, 40, 60, []),
    "iron scorpion": (22, 0, 36, 60, 25, 31, 48, []),
    "skeleton scrapper": (36, 0, 44, 34, 23, 42, 62, []),
    "scarewolf": (38, 6, 50, 36, 23, 52, 80, ["zap"]),
    "gold golem": (99, 0, 48, 30, 26, 6, 650, []),
    "chimaera": (42, 0, 56, 48, 31, 64, 150, []),
    "spitegeist": (33, 14, 40, 38, 26, 47, 72, ["fireball"]),
    "raving lunatick": (35, 30, 41, 40, 28, 58, 95, ["blizzard"]),
    "drohl diabolist": (38, 10, 44, 16, 11, 58, 110, ["fireball"]),
    "skeleton soldier": (46, 12, 62, 46, 36, 72, 120, ["fireball"]),
    "death scorpion": (35, 0, 55, 90, 33, 70, 110, []),
    "knight errant": (55, 6, 70, 71, 45, 78, 150, ["zap"]),
    "dark skeleton": (43, 0, 79, 51, 40, 90, 148, []),
    "hocus chimaera": (50, 12, 68, 62, 44, 83, 135, ["fireball"]),
    "metal slime": (4, 6, 18, 255, 153, 775, 6, ["zap"]),
    "tearwolf": (60, 0, 80, 65, 45, 95, 155, []),
    "cosmic chimaera": (73, 15, 82, 65, 52, 105, 169, ["zap", "fireball"]),
    "dragon": (67, 18, 88, 72, 47, 135, 160, ["zap", "fireball"]),
    "green dragon": (166, 65, 88, 72, 47, 950, 250, ["zap", "fireball", "blizzard", "lightning"]),
    "vis mager": (70, 16, 71, 60, 49, 120, 185, ["zap", "fireball"]),
    "golem": (155, 0, 120, 60, 39, 2000, 10, []),
    "knight aberrant": (79, 4, 94, 92, 53, 130, 165, ["zap"]),
    "blue dragon": (98, 75, 98, 80, 52, 180, 150, ["zap", "fireball", "blizzard", "lightning"]),
    "stone golem": (160, 0, 100, 40, 40, 155, 148, []),
    "knight abhorrent": (98, 14, 105, 99, 57, 172, 152, ["zap", "fireball"]),
    "red dragon": (105, 85, 115, 104, 62, 350, 143, ["zap", "fireball", "blizzard", "lightning"]),
    "dragon mage": (240, 95, 107, 110, 55, 480, 500, ["zap", "fireball", "blizzard", "lightning"]),
    "dragon lord": (361, 120, 130, 150, 90, 1000, 2500, ["zap", "fireball", "blizzard", "lightning"])
}

if __name__ == "__main__":
    pass

#TODO: Implement escape action
#Create a vendor from the NPC class that takes gold for weapons and armor
