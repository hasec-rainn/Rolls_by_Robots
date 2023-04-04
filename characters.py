import actions as act
import modifiable_objs as mo
import ai_constants as aic

class Character:
    
    def __init__(self, name, max_hp, ac, speed, prof_bonus,
                 dmg_mods : dict, attributes : dict, actions, 
                 bonus_actions : dict, reactions : dict, leg_actions : dict):
        """
        Creates a new character object with a specified name, maximum hp, ac,
        and proficiency bonus.    

        * `dmg_mods` should be a dict of mo.DmgMod objects, where the key = damage type
        * `attributes` should be a dict of mo.Attribute objects, where key = attribute type
        * `actions` should be a dict of two arrays with the keys `pos` and `neg`. These arrays contain actions that benefit and harm targets, respectively.
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
    
    def __init__(self):
        """
        Creates a new, *empty* character object.
        Should not be called except by ReturnCopy method
        """
        self.name = None
        self.health = mo.Health(-1) 
        self.ac = mo.ModObj(-1)  #assume armor is static: system cannot represent taking cover
        self.prof_bonus = -1
        self.speed = mo.ModObj(-1)   #speed boosts & reductions are representable
        self.effects = mo.Effects()

        self.dmg_mods = {}
        for type in range(0,aic.NDMGMOD):
            self.dmg_mods[type] = -1

        self.attributes = {}
        for att in range(0,aic.NATT):
            self.attributes[att] = -1
        self.used_reaction = False
        
        self.all_actions = {"actions": {"pos": [], "neg": []},
                      "bonus_actions": {"pos": [], "neg": []},
                      "reactions": {"pos": [], "neg": []},
                      "leg_actions": {"pos": [], "neg": []}
                      }


    def ReturnCopy(self):
        """
        Returns a deep copy* of the `character` object
        * Note that all_actions is not a deep copy, as it should never
        be changed
        """
        copy = Character()
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