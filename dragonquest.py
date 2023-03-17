import random

class Character:
    def __init__(self, name):
        self.name = name
        self.strength = 16
        self.intellect = 16
        self.resilience = 16
        
        #ability to run away (TODO: implement Escape action?)
        #self.agility = 16

        self.max_hp = 16
        self.hp = self.max_hp
        self.max_mp = 16
        self.mp = self.max_mp
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

    def cast(self, spell, target):
        if spell in self.spellbook.keys():
            print("%s casts %s.\n" % (self.name, spell))
            return self.spellbook[spell].cast(target, self)

        else:
            print("%s can't cast %s.\n" % (self.name, spell))
            return False

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

class PlayerCharacter(Character):
    def __init__(self, name):
        super().__init__(name)

        self.gold = 100
        self.level = 1
        self.xp = 0
        self.quest_flags = {}
        
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
    "Bamboo Pole": 2,
    "Club": 4,
    "Copper Sword": 10,
    "Hand Axe": 15,
    "Broad Sword": 20,
    "Flame Sword": 28,
    "Erdrick's Sword": 40
}

armor = {
    "Clothes": 2,
    "Leather Armor": 4,
    "Chain Mail": 12,
    "Half Plate": 16,
    "Full Plate": 24,
    "Magic Armor": 24,
    "Erdrick's Armor": 28
}

shields = {
    "Leather Shield": 4,
    "Iron Shield": 10,
    "Silver Shield": 24
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

if __name__ == "__main__":
    pass