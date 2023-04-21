import actions as act
import modifiable_objs as mo
import ai_constants as aic

class Character:
    
    def __init__(self, name, max_hp, ac, speed, prof_bonus,
                 dmg_mods : dict, attributes : dict, actions: dict, 
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
        return ("Character " + str(self.name) + "Overview:"
        + "\n\t" + str(self.health)
        + "\n\tAC: " + str(self.ac) 
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

        copy.all_actions["actions"]["pos"] = self.all_actions["actions"]["pos"]
        copy.all_actions["bonus_actions"]["pos"] = self.all_actions["bonus_actions"]["pos"]
        copy.all_actions["reactions"]["pos"] = self.all_actions["reactions"]["pos"]
        copy.all_actions["leg_actions"]["pos"] = self.all_actions["leg_actions"]["pos"]

        copy.all_actions["actions"]["neg"] = self.all_actions["actions"]["neg"]
        copy.all_actions["bonus_actions"]["neg"] = self.all_actions["bonus_actions"]["neg"]
        copy.all_actions["reactions"]["neg"] = self.all_actions["reactions"]["neg"]
        copy.all_actions["leg_actions"]["neg"] = self.all_actions["leg_actions"]["neg"]
        
        return copy    

    def RecieveAction(self, action : act.Action):
        if action.id == aic.MELEEATK:
            print("looks like a melee attack!")
        elif action.id == aic.RANGEDATK:
            print("looks like a ranged attack")