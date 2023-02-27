import random

class Character:
    def __init__(self, name):
        self.name = name
        self.inventory = {}
        self.gold = 100
        
        #physical power
        self.strength = 16
        
        #knowledge of arcane arts
        self.intellect = 16
        
        #ability to run away
        self.agility = 16
        
        #natural damage tolerance
        self.resilience = 16
        
        #maximum health points
        self.max_hp = 16
        self.hp = self.max_hp
        
        #maximum magic points
        self.max_mp = 16
        self.mp = self.max_mp
        
        #attack power = strength+weapon
        #spell power = intellect+spell
        #defense power = (shield+armor)+resilience 
        #protection = intellect+resilience 
        self.equipment = {
        	}
        self.spellbook = {}
        self.status = []
        pass

    def speak(self, target):
        pass

    def equip(self, slot, gear):
        self.equipment[slot] = gear
        pass
            
    pass

class NPCharacter(Character):
    def __init__(self, name):
        super().__init__(name)
        pass
    pass

class PlayerCharacter(Character):
    def __init__(self, name):
        super().__init__(name)
        
        self.level = 1
        self.exp_points = 0
        self.quest_flags = {
        	
        	}
        pass
    pass

class Effect():
    def __init__(self, name, power):
        self.name = name
        self.power = power

    pass

class Spell(Effect):
    def __init__(self, name, cost, power, status='none'):
        super().__init__(name, power)
        self.cost = cost
        self.status = status

    def pay(self, caster):
        if caster.mp > self.cost:
            caster.mp = caster.mp - self.cost
            return True
        else:
            return False

    def cast(self, target, caster):
        if self.pay(caster):
            # calculate damage
            damage = (random.randint(caster.intellect/4, caster.intellect))+(random.randint(self.power/2, self.power))
            print("%s deals %d" % (self.name, damage))
            
            if self.status in target.status:
                resist = (random.randint(target.intellect/2, target.intellect))+(random.randint(target.resilience/2, target.resilience))
                print("%s resists %d damage" % (target.name, resist))
                damage = damage - resist
                if damage < 0:
                    damage = 0
                    print("%s is ineffective" % self.name)
                target.hp = target.hp - damage
                if target.hp < 0:
                    target.hp = 0
                print("%s hp is %d" % (target.name, target.hp))
                if target.hp < 1:
                    print("%s died.\n" % target.name)
            else:
                resist = (random.randint(0, target.intellect/2))+(random.randint(0, target.resilience/2))
                print("%s resists %d damage" % (target.name, resist))
                
                damage = damage - resist
                if damage < 0:
                    damage = 0
                    print("%s is ineffective" % self.name)
                target.hp = target.hp - damage
                if target.hp < 0:
                    target.hp =0
                print("%s hp is %d" % (target.name, target.hp))
                if target.hp < 1:  
                    print("%s died.\n" % target.name)
                    
                if not self.status == 'none' and damage > 0:
                    target.status.append(self.status)
                
            return True
        else:
            return False

class Potion(Effect):
    def __init__(self, name, attribute, power, quantity=0):
        super().__init__(name, power)
        self.attribute = attribute
        self.quantity = quantity

    def pay(self, caster):
        if caster.inventory[self.name].quantity > 0:
            caster.inventory[self.name].quantity = caster.inventory[self.name].quantity - 1
            return True
        else:
            return False

    def drink(self, caster):
        if self.pay(caster):
            if self.attribute == 'hp':
                caster.hp = caster.hp + self.power
                print("%s restores %d hp" % (self.name, self.power))
                if caster.hp > caster.max_hp:
                    caster.hp = caster.max_hp
                print("%s hp is now %d" % (caster.name, caster.hp))
            elif self.attribute == 'mp':
                caster.mp = caster.mp + self.power
                print("%s restores %d mp" % (self.name, self.power))
                if caster.mp > caster.max_mp:
                    caster.mp = caster.max_mp
                print("%s mp is now %d" % (caster.name, caster.mp))


            return True
        else:
            return False

class Equipment(Effect):
    def __init__(self, name, power, slot):
        super().__init__(name, power)
        self.slot = slot

    def pay(self, caster):
        pass
    
    def equip(self, caster):
        #TODO: ensure item is in inventory to equip
        if caster.equipment[self.slot]:
            caster.inventory.append(caster.equipment[self.slot])
        caster.equipment[self.slot] = self.name

class Weapon(Equipment):
    def __init__(self, name, power, slot):
        super().__init__(name, power, slot)
        
    def attack(self, caster, target):
        pass

#Type: (+attack, gold)
weapons = {
   "Bamboo Pole": (2, 10),
   "Club": (4, 60),
   "Copper Sword": (10, 180),
   "Hand Axe": (15, 560),
   "Broad Sword": (20, 1500),
   "Flame Sword": (28, 9800),
   "Erdrick's Sword": (40, 0) 
}


#Type: (+defense, gold)
armor = {
   "Clothes": (2, 50),
   "Leather Armor": (4, 40),
   "Chain Mail": (12, 300),
   "Half Plate": (16, 1000),
   "Full Plate": (24, 3000),
   "Magic Armor": (24, 7700),
   "Erdrick's Armor": (28, 0)
}

#Type: (+defense, gold)
shields = {
   "Leather Shield": (4, 90),
   "Iron Shield": (10, 800),
   "Silver Shield": (24, 14800)
}


char = Character("Ted")
npc = NPCharacter("Bill")
player = PlayerCharacter("Murph")

player.spellbook["zap"] = Spell("zap", 1, 2)
player.spellbook["fireball"] = Spell("fireball", 2, 4, "burning")
player.spellbook["blizzard"] = Spell("blizzard", 4, 8, "freezing")
player.spellbook["lightning"] = Spell("lightning", 8, 12, "shocked")

player.inventory["red potion"] = Potion("red potion", 'hp', 8, 3)
npc.inventory["red potion"] = Potion("red potion", 'hp', 8, 3)
player.inventory["blue potion"] = Potion("blue potion", 'mp', 8, 3)


print(char.name)
print(npc.name)
print(player.name, player.strength, player.equipment)

player.spellbook["zap"].cast(npc, player)
player.spellbook["fireball"].cast(npc, player)
player.spellbook["blizzard"].cast(npc, player)

player.inventory["blue potion"].drink(player)
npc.inventory["red potion"].drink(npc)
player.spellbook["blizzard"].cast(npc, player)
player.spellbook["lightning"].cast(npc, player)

print(npc.name,npc.hp, npc.mp, npc.status, npc.inventory["red potion"].name, npc.inventory["red potion"].quantity)
print(player.name, player.hp, player.mp, player.status, player.inventory["blue potion"].name, player.inventory["blue potion"].quantity)
