import actions as act
import modifiable_objs as mo
import ai_constants as aic
import random as rand
import math as mth

class Character:

    def __init__(self, name, max_hp, ac, speed, prof_bonus,
                 dmg_mods : dict[mo.DmgMod], attributes : dict, actions: dict, 
                 bonus_actions : dict, reactions : dict, leg_actions : dict):
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
        for type in range(0,aic.NDMGMOD):
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
        for type in range(0,aic.NDMGMOD):
            self.dmg_mods[type] = -1

        attributes = {}
        for att in range(0,aic.NATT):
            self.attributes[att] = -1

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
        
        for type in range(0,aic.NDMGMOD):
            copy.dmg_mods[type] = self.dmg_mods[type].ReturnCopy()

        for att in range(0,aic.NATT):
            copy.attributes[att] = self.attributes[att]
        copy.used_reaction = self.used_reaction

        #we don't need to deep copy
        copy.all_actions = self.all_actions
        # copy.all_actions["actions"]["pos"] = self.all_actions["actions"]["pos"]
        # copy.all_actions["bonus_actions"]["pos"] = self.all_actions["bonus_actions"]["pos"]
        # copy.all_actions["reactions"]["pos"] = self.all_actions["reactions"]["pos"]
        # copy.all_actions["leg_actions"]["pos"] = self.all_actions["leg_actions"]["pos"]

        # copy.all_actions["actions"]["neg"] = self.all_actions["actions"]["neg"]
        # copy.all_actions["bonus_actions"]["neg"] = self.all_actions["bonus_actions"]["neg"]
        # copy.all_actions["reactions"]["neg"] = self.all_actions["reactions"]["neg"]
        # copy.all_actions["leg_actions"]["neg"] = self.all_actions["leg_actions"]["neg"]
        
        return copy    

    def RecieveAction(self, action : act.Action):
        if action.id == aic.MELEEATK:
            e_MeleeAtk(action)
        elif action.id == aic.RANGEDATK:
            pass
        elif action.id == aic.DAMAGESAVE:
            pass
        elif action.id == aic.CONDITIONSAVE:
            e_ConditionSave(self, action)

    def Foo(self):
        E_MeleeAtk(self, None)


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

#should only by called by other Resolve_ functions
def __ResolveRealDamage__(self : Character, sender: Character, a : act.MeleeAtk, dmg_modifier : int):
    #do damage rolls
    damage = 0
    for d in range(0,a.dice[aic.QTY]):
        damage += rand.randint(1,a.dice[aic.DICETYPE])

    #change the damage to reflect the receiver's resistance
    damage = mth.floor(damage * aic.dmgmod_dict[dmg_modifier])

    #have the receiver take the damage
    self.health.SubHP(damage)




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
    dmg_modifier = self.dmg_mods[a.dmg_type].GetValue()
    if (dmg_modifier != aic.IMMUNE and real):
        toHit = (a.use_prof*sender.prof_bonus)+rand.randint(1,20)
        if toHit >= self.ac.GetValue():
            __ResolveRealDamage__(self,sender,a,dmg_modifier)
    elif (dmg_modifier != aic.IMMUNE and not real):
        pass

def ResolveRangedAtk(self : Character, a : act.RangedAtk, real : bool):
    """
    Function that modifies a character as if they had just been affected
    by the described action.
    * `self` : the character to be affected/changed by the action
    * `a` : the action that will affect the character
    * `real` : boolean value representing if real mode should be used to
    resolve the action. `True` -> real mode, `False` -> expected mode.
    """
    print(self.name)

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
    