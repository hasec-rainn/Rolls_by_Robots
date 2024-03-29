import actions as act
import modifiable_objs as mo
import ai_constants as aic
import random as rand
import math as mth
import numpy as np

class Character:

    def __init__(self, name, max_hp, ac, speed, prof_bonus,
                 dmg_mods : dict[mo.DmgMod], attributes : dict, actions: dict[act.Action], 
                 bonus_actions : dict[act.Action], reactions : dict[act.Action], leg_actions : dict[act.Action]):
        """
        Creates a new character object with a specified name, maximum hp, ac,
        and proficiency bonus.    

        * `dmg_mods` should be a dict of mo.DmgMod objects, where the key = damage type
        * `attributes` should be a dict of mo.Attribute objects, where key = attribute type
        * `actions` should be a dict containing two arrays keyed as `pos` and `neg`. These arrays contain actions that benefit and harm targets, respectively.
        * 'bonus_actions', `reactions`, `leg_actions` should have the same structure as `actions`
        """
        self.name = name
        self.health = mo.Health(max_hp) 
        self.ac = mo.ModObj(ac)  #assume armor is static: system cannot represent taking cover
        self.prof_bonus = prof_bonus
        self.speed = mo.ModObj(speed)   #speed boosts & reductions are representable
        self.effects = mo.Effects()

        self.dmg_mods = {}
        for type in range(0,aic.NDMGTYPE):
            self.dmg_mods[type] = dmg_mods[type]

        self.attributes = {}
        for att in range(0,aic.NATT):
            self.attributes[att] = attributes[att]

        self.used_reaction = False
        self.all_actions = {"actions": {"pos": [], "neg": []},
                      "bonus_actions": {"pos": [], "neg": []},
                      "reactions": {"pos": [], "neg": []},
                      "leg_actions": {"pos": [], "neg": []}
                      }
        self.all_actions["actions"]["pos"] = actions["pos"]
        self.all_actions["bonus_actions"]["pos"] = bonus_actions["pos"]
        self.all_actions["reactions"]["pos"] = reactions["pos"]
        self.all_actions["leg_actions"]["pos"] = leg_actions["pos"]

        self.all_actions["actions"]["neg"] = actions["neg"]
        self.all_actions["bonus_actions"]["neg"] = bonus_actions["neg"]
        self.all_actions["reactions"]["neg"] = reactions["neg"]
        self.all_actions["leg_actions"]["neg"] = leg_actions["neg"]

    def __str__(self) -> str:
        return ("Character '" + str(self.name) + "' Overview:"
        + "\nHealth" + str(self.health)
        + "\nAC: " + str(self.ac)
        + "\nProf Bonus: \n\t" + str(self.prof_bonus)
        + "\nSpeed: " + str(self.speed)
        + "\nEffects: " + str(self.effects) 
        )

    def ReturnCopy(self):
        """
        Returns a deep copy* of the `character` object.
        Used when creating a duplicate of a character so it can be modified in a
        new state
        * Note that all_actions is not a deep copy, as it should never
        be changed
        """

        dmg_mods = {}
        for type in range(0,aic.NDMGTYPE):
            dmg_mods[type] = -1

        attributes = {}
        for att in range(0,aic.NATT):
            attributes[att] = -1

        copy = Character(None,-1,-1,-1,-1,dmg_mods,attributes,
                         {"pos":[],"neg":[]}, {"pos":[],"neg":[]},
                         {"pos":[],"neg":[]}, {"pos":[],"neg":[]}
                         )
        copy.name = self.name
        copy.health = self.health.ReturnCopy()
        copy.ac = self.ac.ReturnCopy()
        copy.prof_bonus = self.prof_bonus
        copy.speed = self.speed.ReturnCopy()
        copy.effects = self.effects.ReturnCopy()
        
        for type in range(0,aic.NDMGTYPE):
            copy.dmg_mods[type] = self.dmg_mods[type].ReturnCopy()

        for att in range(0,aic.NATT):
            copy.attributes[att] = self.attributes[att].ReturnCopy()
        copy.used_reaction = self.used_reaction

        #we don't need to deep copy this
        copy.all_actions = self.all_actions
        
        return copy    

    def RecieveAction(self, sender : "Character", action : act.Action, real : bool):
        if action.id == aic.MELEEATK and not real:
            ResolveMeleeAtk(self, sender, action, real)
        if action.id == aic.RANGEDATK and not real:
            ResolveRangedAtk(self, sender, action, real)


"""
there are two types of function modes: expected and real

'expected' handles an action according to averages and expected outcomes:
there is no random number generation (ie, dice rolling).
Expected is used by the AI to "look ahead" and predict the results of an
action before actually procedding to do said action.

'real' handles an action as it would occur in real life: by generating a
random number to represent dice rolls.
Real is used by the AI to actually take an action after having decided it
was the best action to take.
"""

# arrays containing resolve functions. Can be indexed by using aic constants
# (eg, resolve_expected[aic.MELEEATK] or resolve_real[aic.CONDITIONSAVE])
resolve_expected = {}
resolve_real = {}


def __to_hit_mod__(sender : Character, receiver : Character):
    """
    Checks if the Character `sender` has advantage, disadvantage, or
    a normal chance to hit `receiver` with a melee attack. Returns negative
    on disadvantage, 0 on normal, and positive on advantage.
    """

    #tally up the total number of things giving the attacker (sender) adv
    adv_total = sum(sender.effects.GetEffects() * aic.ATTACKER_ADV_MELEE_MASK) \
    + sum(receiver.effects.GetEffects() * aic.RECEIVER_ADV_MELEE_MASK) 

    #tally up the total number of things giving the attacker (sender) disadv
    disadv_total = sum(sender.effects.GetEffects() * aic.ATTACKER_DISADV_MELEE_MASK) \
    + sum(receiver.effects.GetEffects() * aic.RECEIVER_DISADV_MELEE_MASK)

    return (adv_total - disadv_total)


    

#should only by called by other Resolve_ functions
def __ResolveRealDamage__(self : Character, a : act.Action, dmg_modifier : int):
    """
    Calculates the ammount of damage the character `self` should take, based
    off the rolled damage of the action `a` sent by `sender`. 
    `hit_chance` is not present; if this function is called, the attack 
    has already hit. 
    """
    #do damage rolls
    damage = 0
    for d in range(0,a.dice[aic.DICEQTY]):
        damage += rand.randint(1,a.dice[aic.DICETYPE])

    #change the damage to reflect the receiver's resistance
    damage = mth.floor(damage * aic.dmgmod_dict[dmg_modifier])

    #have the receiver take the damage
    self.health.SubHP(damage)

#should only be called by other resolve functions
def __ResolveExpectedDamage__(self : Character, sender: Character, a : act.Action,
                              dmg_modifier : int, hit_mod : int):
    """
    Calculates the ammount of damage the character `self` should take, based
    off the weighted damage of the action `a` sent by `sender`. 
    The damage is weighted by its likelyhood to hit: `hit_chance`.
    `hit_chance`, in turn, is partly affected by the parameter `hit_mod`. 
    """
    hit_chance = -1
    if hit_mod == 0: #looking at a normal chance to hit
            hit_chance = (21 + (sender.prof_bonus*a.use_prof) - self.ac.GetValue()) / 20
    elif hit_mod < 0: #looking at disadvantage to hit
        hit_chance = (21 + (sender.prof_bonus*a.use_prof) - self.ac.GetValue())**2 / 400
    else: # looking at advantage to hit
        hit_chance = 1 - (self.ac.GetValue() - (sender.prof_bonus*a.use_prof) - 1)**2 / 400

    #calc expected damage based off dmg modifier and hit chance
    damage = a.damage * hit_chance
    damage = mth.floor(damage * aic.dmgmod_dict[dmg_modifier])

    #have the receiver take the damage
    self.health.SubHP(damage)


def FlightCheck(self : Character, sender : Character):
    """
    Checks to make sure that `sender` can affect `self` with an action,
    based off the assumption that someone who can't fly won't be able
    to reach someone in melee who can fly.
    """
    
    #if sender can affect, result should be >= 0
    #this means that either both can fly, both can't fly, or the sender can fly
    if 0 >= (sender.effects.GetEffects()[aic.FLY] - self.effects.GetEffects()[aic.FLY]):
        return True
    else:
        return False

def ResolveMeleeAtk(self : Character, sender : Character, a : act.MeleeAtk, real : bool):
    """
    Function that modifies a character as if they had just been affected
    by the described action.
    * `self` : the character to be affected/changed by the action
    * `sender` : the character sending the action that will affect `self`
    * `a` : the action being sent that will affect the character `self`
    * `real` : boolean value representing if real mode should be used to
    resolve the action. `True` -> real mode, `False` -> expected mode.
    """
    
    #resolve the attack in real/expected mode, given that the receiver is
    #not immune to that damage type
    #otherwise, assume the receiver cannot be harmed and do nothing
    dmg_modifier = self.dmg_mods[a.dmg_type].GetValue() #relevant damage modifier for receiver
    if (dmg_modifier != aic.IMMUNE and FlightCheck(self, sender)):
        
        res = __to_hit_mod__(sender, self)
        #resolve attacks
        if real:
            hit_roll = None
            if res == 0: # looks like the attacker has norm chance to hit
                hit_roll = (a.use_prof*sender.prof_bonus)+rand.randint(1,20)
            elif res < 0: #looks like attacker has disadvantage to hit
                hit_roll_1 = (a.use_prof*sender.prof_bonus)+rand.randint(1,20)
                hit_roll_2 = (a.use_prof*sender.prof_bonus)+rand.randint(1,20)
                hit_roll = min(hit_roll_1, hit_roll_2)
            else: #looks like attacker has advantage to hit
                hit_roll_1 = (a.use_prof*sender.prof_bonus)+rand.randint(1,20)
                hit_roll_2 = (a.use_prof*sender.prof_bonus)+rand.randint(1,20)
                hit_roll = max(hit_roll_1, hit_roll_2)

            if hit_roll >= self.ac.GetValue():
                __ResolveRealDamage__(self, a, dmg_modifier)
        else:
            hit_mod = __to_hit_mod__(sender, self)
            __ResolveExpectedDamage__(self,sender,a,dmg_modifier,hit_mod)

def ResolveRangedAtk(self : Character, sender : Character, a : act.RangedAtk, real : bool):
    """
    Function that modifies a character as if they had just been affected
    by the described action.
    * `self` : the character to be affected/changed by the action
    * `sender` : the character sending the action that will affect `self`
    * `a` : the action being sent that will affect the character `self`
    * `real` : boolean value representing if real mode should be used to
    resolve the action. `True` -> real mode, `False` -> expected mode.
    """
    
    #resolve the attack in real/expected mode, given that the receiver is
    #not immune to that damage type
    #otherwise, assume the receiver cannot be harmed and do nothing
    
    dmg_modifier = self.dmg_mods[a.dmg_type].GetValue() #relevant damage modifier for receiver
    if (dmg_modifier != aic.IMMUNE):
        
        res = __to_hit_mod__(sender, self)
        #resolve attacks
        if real:
            hit_roll = None
            if res == 0: # looks like the attacker has norm chance to hit
                hit_roll = (a.use_prof*sender.prof_bonus)+rand.randint(1,20)
            elif res < 0: #looks like attacker has disadvantage to hit
                hit_roll_1 = (a.use_prof*sender.prof_bonus)+rand.randint(1,20)
                hit_roll_2 = (a.use_prof*sender.prof_bonus)+rand.randint(1,20)
                hit_roll = min(hit_roll_1, hit_roll_2)
            else: #looks like attacker has advantage to hit
                hit_roll_1 = (a.use_prof*sender.prof_bonus)+rand.randint(1,20)
                hit_roll_2 = (a.use_prof*sender.prof_bonus)+rand.randint(1,20)
                hit_roll = max(hit_roll_1, hit_roll_2)

            if hit_roll >= self.ac.GetValue():
                __ResolveRealDamage__(self, a, dmg_modifier)
        else:
            hit_mod = __to_hit_mod__(sender, self)
            __ResolveExpectedDamage__(self,sender,a,dmg_modifier,hit_mod)

def ResolveDamageSave(self : Character, a : act.DamageSave, real : bool):
    """
    Function that modifies a character as if they had just been affected
    by the described action.
    * `self` : the character to be affected/changed by the action
    * `a` : the action that will affect the character
    * `real` : boolean value representing if real mode should be used to
    resolve the action. `True` -> real mode, `False` -> expected mode.
    """
    pass

def ResolveConditionSave(self : Character, a : act.ConditionSave, real : bool):
    """
    Function that modifies a character as if they had just been affected
    by the described action.
    * `self` : the character to be affected/changed by the action
    * `a` : the action that will affect the character
    * `real` : boolean value representing if real mode should be used to
    resolve the action. `True` -> real mode, `False` -> expected mode.
    """
    pass

def ResolveConditionBuff(self : Character, a : act.ConditionBuff, real : bool):
    """
    Function that modifies a character as if they had just been affected
    by the described action.
    * `self` : the character to be affected/changed by the action
    * `a` : the action that will affect the character
    * `real` : boolean value representing if real mode should be used to
    resolve the action. `True` -> real mode, `False` -> expected mode.
    """
    pass

def ResolveHeal(self : Character, a : act.Heal, mode : str, real : bool):
    """
    Function that modifies a character as if they had just been affected
    by the described action.
    * `self` : the character to be affected/changed by the action
    * `a` : the action that will affect the character
    * `real` : boolean value representing if real mode should be used to
    resolve the action. `True` -> real mode, `False` -> expected mode.
    """
    pass
    