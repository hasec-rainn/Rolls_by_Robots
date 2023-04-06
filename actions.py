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
    """
    Creates a new MeleeAtk action. 
    `MeleeAtk` is nearly identical to `RangedAtk`, except that if an action is a `MeleeAtk`,
    it is assumed that it will not hit a character with the `fly` effect unless the user also
    is flying
    * `name`: action's name. Has no impact other than when printing attack.
    * `att`: constant integer from `aic` representing the attribute the attack uses.
    * `range`: range (in feet) of the melee attack.
    * `damage`: damage of the attack. Given attacks in DND rely on dice, it should be the expected/avg damage roll.
    * `dmg_type`: constant integer from `aic` representing the damage type of the attack.
    * `use_prof`: boolean used to determine if `prof_bonus` of a `character` is used for this attack
    * `aoe`: integer representing the area of effect (in feet) of this attack. None if it has no aoe
    """
    id = aic.MELEEATK

    def __init__(self, name:str, att:int, range:int, damage:int, dmg_type:int, use_prof:bool, aoe:int=None):
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
    """
    Creates a new RangedAtk action. 
    `RangedAtk` is nearly identical to `MeleedAtk`, except that if an action is a `RangedAtk`,
    it is always capable of hitting a character with the `fly` effect
    * `name`: action's name. Has no impact other than when printing attack.
    * `att`: constant integer from `aic` representing the attribute the attack uses.
    * `range`: range (in feet) of the melee attack.
    * `damage`: damage of the attack. Given attacks in DND rely on dice, it should be the expected/avg damage roll.
    * `dmg_type`: constant integer from `aic` representing the damage type of the attack.
    * `use_prof`: boolean used to determine if `prof_bonus` of a `character` is used for this attack
    * `aoe`: integer representing the area of effect (in feet) of this attack. None if it has no aoe
    """
    id = aic.RANGEDATK

    def __init__(self, name:str, att:int, range:int, damage:int, dmg_type:int, use_prof:bool, aoe:int=None):
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
    """
    Creates a new DamageSave action.
    DamageSave forces a character to make a saving throw or take damage.
    * `name`: action's name. Has no impact other than when printing attack.
    * `att`: constant integer from `aic` representing the attribute the attack uses.
    * `range`: range (in feet) of the melee attack.
    * `damage`: damage of the attack. Given attacks in DND rely on dice, it should be the expected/avg damage roll.
    * `dmg_type`: constant integer from `aic` representing the damage type of the attack.
    * `save_type`: constant int from `aic` representing the save type (eg, CON, INT, WIS)
    * `take_half`: bool dictating if a creature will still take half damage even if they succeed the save
    * `aoe`: integer representing the area of effect (in feet) of this attack. None if it has no aoe
    """
    id = aic.DAMAGESAVE
    
    def __init__(self, name:str, att:int, range:int, damage:int, 
                 dmg_type:int, save_type:int, take_half:bool, aoe:int=None):
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
    """
    Creates a new ConditionSave action.
    ConditionSave forces a character to make a saving throw or fall under some effect.
    * `name`: action's name. Has no impact other than when printing attack.
    * `att`: constant integer from `aic` representing the attribute the attack uses.
    * `range`: range (in feet) of the melee attack.
    * `condition`: constant int from `aic`. 
    * `dmg_type`: constant int from `aic` representing the damage type of the attack.
    * `save_type`: constant int from `aic` representing the save type (eg, CON, INT, WIS)
    * `take_half`: bool dictating if a creature will still take half damage even if they succeed the save
    * `aoe`: integer representing the area of effect (in feet) of this attack. None if it has no aoe

    Unlike `damage` (number), you can't weight an `effect` (bool) by its success rate. This makes
    determining when to apply effects difficult. In normal circumstances, if a character would fail
    the save on average, then the character will always have the effect applied to them.
    """
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


# default_action = Action("default","dex",10)
# melee = MeleeAtk("sword","str",5,25,"slash",True)
# ranged = RangedAtk("bow","dex",300,10,"pierce",True)
# earth_shatter = DamageSave("Earth Shatter", "str",30,50,"bludgeon","dex",True)
# color_spray = ConditionSave("color spray","int",30,"blind",10,"wis",25)
# rage = ConditionBuff("Rage",aic.STR,aic.SELF,"Enraged",100,True)
# lay_on_hands = Heal("Lay On Hands", aic.CHA, aic.TOUCH, 20)

# a_list = [default_action,melee,ranged,earth_shatter,color_spray,rage, lay_on_hands]

# for action in a_list:
#     print(action)
#     print("\n")