import ai_constants as aic

# Contains all the actions that a character might perform
# this includes attack actions, buff actions, healing actions, etc

class Action:
    """Class to define different types of Actions. """

    def __init__(self, name, att, range, aoe=None):
        self.name = name
        self.att = att
        #what is the maximum distance a target can be to receive this action?
        self.range = range
        #how much of an AOE (if any) does this action have?
        self.aoe = aoe

    def __str__(self):
        return (
        "\nName: " + str(self.name)
        + "\nAttribute: " + str(self.att)
        + "\nRange: " + str(self.range)
        + "\nAOE: " + str(self.aoe)
        )
        #print(*(f"{x}: {y}" for x, y in vars(self).items()), sep="\n")



class MeleeAtk(Action):
    id = aic.MELEEATK

    def __init__(self, name, att, range, damage, dmg_type, use_prof, aoe=None):
        self.name = name
        self.att = att
        self.range = range
        self.aoe = aoe
        self.damage = damage
        self.dmg_type = dmg_type
        self.use_prof = use_prof

    def __str__(self):
        return (
        "\nID: " + aic.action_dict[self.id]
        + Action.__str__(self)
        + "\nDamage: " + str(self.damage)
        + "\nDamage Type: " + str(self.dmg_type)
        + "\nUses Proficiency? " + str(self.use_prof)
        )



class RangedAtk(Action):
    id = aic.RANGEDATK

    def __init__(self, name, att, range, damage, dmg_type, use_prof, aoe=None):
        self.name = name
        self.att = att
        self.range = range
        self.aoe = aoe
        self.damage = damage
        self.dmg_type = dmg_type
        self.use_prof = use_prof

    def __str__(self):
        return (
        "\nID: " + aic.action_dict[self.id]
        + Action.__str__(self)
        + "\nDamage: " + str(self.damage)
        + "\nDamage Type: " + str(self.dmg_type)
        + "\nUses Proficiency? " + str(self.use_prof)
        )



# Action that requires someone to make a saving throw. 
# If they fail, they take damage.
class DamageSave(Action):
    
    id = aic.DAMAGESAVE
    
    def __init__(self, name, att, range, damage, dmg_type, save_type, take_half, aoe=None):
        self.name = name
        self.att = att
        self.range = range
        self.aoe = aoe
        self.damage = damage
        self.dmg_type = dmg_type
        #what type of save (STR,DEX,etc) will recipient make?
        self.save_type = save_type
        #even if someone succeeds, do they still take half dmg?
        self.take_half = take_half

    def __str__(self):
        return (
            "\nID: " + aic.action_dict[self.id]
            + Action.__str__(self)
            + "\nDamage: " + str(self.damage)
            + "\nDamage Type: " + str(self.dmg_type)
            + "\nSave Type: " + str(self.save_type)
            + "\nHalf on Success? " + str(self.take_half)
        )

    def CalcDC(self,proficiency,att_mods):
        """Calculates the DC for this save, since DC is always 
        8+proficiency+attribute modifier.
        """
        return 8 + proficiency + att_mods[self.att]




# Action that requires someone to make a saving throw. 
# If they fail, they are afflicted with a condition for a duration.
class ConditionSave(Action):
    id = aic.CONDITIONSAVE
    
    def __init__(self, name, att, range, condition, duration, save_type, aoe=None):
        self.name = name
        self.att = att
        self.range = range
        self.aoe = aoe
        self.condition = condition # what condition are they afflicted with?
        self.duration = duration #how long will this condition last?
        #what type of save (STR,DEX,etc) will recipient make?
        self.save_type = save_type

    def __str__(self):
        return (
            "\nID: " + aic.action_dict[self.id]
            + Action.__str__(self)
            + "\nCondition: " + str(self.condition)
            + "\nDuration: " + str(self.duration)
            + "\nSave Type: " + str(self.save_type)
        )

    def CalcDC(self, proficiency, att_mods):
        """Calculates the DC for this save, since DC is always 
        8+proficiency+attribute modifier.
        """
        return 8 + proficiency + att_mods[self.att]



class ConditionBuff(Action):
    id = aic.CONDITIONBUFF

    def __init__(self, name, att, range, condition, duration, aoe=None):
        self.name = name
        self.att = att
        self.range = range
        self.aoe = aoe
        self.condition = condition # what condition are they afflicted with?
        self.duration = duration #how long will this condition last?

    def __str__(self):
        return (
            "\nID: " + aic.action_dict[self.id]
            + Action.__str__(self)
            + "\nCondition: " + str(self.condition)
            + "\nDuration: " + str(self.duration)
        )
    
class Heal(Action):
    id = aic.HEAL

    def __init__(self, name, att, range, health, aoe=None):
        self.name = name
        self.att = att
        self.range = range
        self.aoe = aoe
        self.health = health # what condition are they afflicted with?

    def __str__(self):
        return (
            "\nID: " + aic.action_dict[self.id]
            + Action.__str__(self)
            + "\nHealing Power: " + str(self.health)
        )


default_action = Action("default","dex",10)
melee = MeleeAtk("sword","str",5,25,"slash",True)
ranged = RangedAtk("bow","dex",300,10,"pierce",True)
earth_shatter = DamageSave("Earth Shatter", "str",30,50,"bludgeon","dex",True)
color_spray = ConditionSave("color spray","int",30,"blind",10,"wis",25)
rage = ConditionBuff("Rage",aic.STR,aic.SELF,"Enraged",100,True)
lay_on_hands = Heal("Lay On Hands", aic.CHA, aic.TOUCH, 20)

a_list = [default_action,melee,ranged,earth_shatter,color_spray,rage, lay_on_hands]

for action in a_list:
    print(action)
    print("\n")