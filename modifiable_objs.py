import numpy as np
from math import floor
import ai_constants as aic

#might try using matrix multiplication to replace self.modifiers
#and self.mod_durs to see which one runs faster

# Object that has a base value that can be influenced by multiple 
# modifers.
class ModObj:

    def __init__(self, base_val):
        self.base_val = base_val #base value that we are modifying
        self.n_mods = 0    #number of modifers acting on baseVal
        self.modifiers = np.zeros(aic.MAXMODS) #all the values that are modifying the base value
        self.mod_durs = np.zeros(aic.MAXMODS)  #time left for each modifer

    # Returns deep copy of this ModObj
    def ReturnCopy(self):
        copy = ModObj(self.base_val)
        copy.n_mods = self.n_mods
        copy.modifiers = self.modifiers.copy()
        copy.mod_durs = self.mod_durs.copy()

        return copy

    def __str__(self):
        return_string = "\nBase Value: " + str(self.base_val)
        if self.n_mods > 0:
            return_string += "\nNumber of mods: " + str(self.n_mods)
            return_string += "\nModified Value: " + str(self.GetValue())
        for m in range(0,aic.MAXMODS):
            if self.modifiers[m] != 0:
                return_string += ("\nMod[" + str(m) + "] = " + str(self.modifiers[m]) 
                + "\t(duration = " + str(self.mod_durs[m]) + ")")
        return return_string

    def AddMod(self, mod_val, dur):
        self.n_mods = self.n_mods + 1

        #find an empty slot in self.modifers to place the new mod
        #should be able to find one in one of the 20 slots...
        for mod in range(0,aic.MAXMODS):
            if self.modifiers[mod] == 0:
                self.modifiers[mod] = mod_val
                self.mod_durs[mod] = dur
                return

        raise IndexError("Maximum number of modifiers exceeded in ModObj")
        


    #Changes the modifiers as if one round had passed*/
    def TimeStep(self):
        #we don't need to do anything if there are no modifiers
        if(self.n_mods > 0):

            #go through the modifiers, decrementing each one until they reach 0
            for m in range(0, aic.MAXMODS): 
                if(self.mod_durs[m] - 1) == 0:
                    self.n_mods = self.n_mods - 1
                    self.mod_durs[m] = 0
                    self.modifiers[m] = 0 #setting to zero is effectively removing it
                elif (self.mod_durs[m] - 1) > 0:
                    self.mod_durs[m] = self.mod_durs[m] - 1
                #third case is that self.mod_durs[m] - 1 is -1. 
                    # In this case, we do nothing
            

    #Returns the modified value of baseVal: baseVal + sum(modifiers)
    def GetValue(self):
        if(self.n_mods > 0):
            return self.base_val + np.sum(self.modifiers)
        else: #there's nothing modifying it; just return baseVal
            return self.base_val
    



class Health(ModObj):

    def __init__(self,max_hp):
        ModObj.__init__(self,max_hp)
        self.max_hp = max_hp
    
    # Returns deep of this Health Object
    def ReturnCopy(self):
        copy = Health(self.base_val)
        copy.max_hp = self.max_hp
        copy.n_mods = self.n_mods
        copy.modifiers = self.modifiers.copy()
        copy.mod_durs = self.mod_durs.copy()

        return copy

    def __str__(self):
        return ("\nVV Max HP VV" + ModObj.__str__(self))

    # Takes away an ammount of HP specifed by "damage"
    def SubHP(self, damage):
        #print("damage", damage)
        if(self.n_mods <=0): #nothing fancy: just subtract directly from baseVal
            self.base_val = self.base_val - damage
        else:    #this player has temp HP; eat through temp HP before base HP
            for m in range(0, aic.MAXMODS):
                self.modifiers[m] = self.modifiers[m] - damage #eating through tempHP
                damage = damage - (damage + self.modifiers[m]) #damage being soaked up by tempHP
                if( self.modifiers[m] > 0 ): #temp health ate up all the damage AND still has some left
                    return #we don't need to do anything else
                elif(self.modifiers[m] == 0): #temp health ate up all damage AND temp health gone
                    self.n_mods = self.n_mods - 1
                    self.mod_durs[m] = 0
                    self.modifiers[m] = 0 #setting to zero is effectively removing it
                    return
                else: #damage ate through this stack of temp hp
                    self.n_mods = self.n_mods - 1
                    self.mod_durs[m] = 0
                    self.modifiers[m] = 0 #setting to zero is effectively removing it

            #Looks like tempHP wasn't enough to absorb all
            #the damage; baseVal takes a hit to HP too
            self.base_val = self.base_val - damage

    #Heals "healVal" amount of HP by directly adding to baseVal
    #of HP. Cannot heal for an ammount greater than "hpMax".*/
    def HealHP(self,heal):
        self.base_val = self.base_val + heal
        if(self.base_val > self.max_hp):
            self.base_val = self.max_hp

    #Grants "tempHP" amount of temporary HP. Exactly the
    #same as "AddMod"*/
    def GiveTempHP(self,temp_hp, dur):
        self.AddMod(temp_hp, dur)




#Basically just ModObj, but with ability to specifically request
#attribute scores and statistic mods (eg str score and str mod)
class Attribute(ModObj):
    #Literally just another name for GetValue
    def __init__(self, att_id, att_score):
        self.att_id = att_id # ID of the attriubte (eg, STR, CON, DEX)
        ModObj.__init__(self, att_score)

    def ReturnCopy(self):
        copy = Attribute(self.att_id,self.base_val)
        copy.n_mods = self.n_mods
        copy.modifiers = self.modifiers.copy()
        copy.mod_durs = self.mod_durs.copy()
        return copy

    def __str__(self):
        return ("\nAttribute: " + aic.att_dict[self.att_id] 
                + "\nMod: " + str(self.GetMod())
                + ModObj.__str__(self)
                )
    
    def AddMod(self, score_mod, dur):
        self.n_mods = self.n_mods + 1

        #find an empty slot in self.modifers to place the new mod
        #should be able to find one in one of the 20 slots...
        for mod in range(0,aic.MAXMODS):
            if self.modifiers[mod] == 0:
                self.modifiers[mod] = score_mod
                self.mod_durs[mod] = dur
                return

        raise IndexError("Maximum number of modifiers exceeded in ModObj")

    def GetScore(self):
        return self.GetValue()

    
    def GetMod(self):
        return floor(( self.GetValue() - 10) / 2)




class DmgMod:
    def __init__(self, base_val):
        self.base_val = base_val #base value that we are modifying
        self.n_mods = 0    #number of modifers acting on baseVal
        self.modifiers = np.zeros(aic.MAXDMGMODS) #all the values that are modifying the base value
        self.mod_durs = np.zeros(aic.MAXDMGMODS)  #time left for each modifer
    
    def __str__(self):
        return "\tGetValue:" + str(self.GetValue())

    # Returns deep of this ModObj
    def ReturnCopy(self):
        copy = DmgMod(self.base_val)
        copy.n_mods = self.n_mods
        copy.modifiers = self.modifiers.copy()
        copy.mod_durs = self.mod_durs.copy()
        return copy

    def AddMod(self, mod_val, dur):
        self.n_mods = self.n_mods + 1

        #find an empty slot in self.modifers to place the new mod
        #should be able to find one in one of the 5 slots...
        for mod in range(0,aic.MAXDMGMODS):
            if self.modifiers[mod] == 0:
                self.modifiers[mod] = mod_val
                self.mod_durs[mod] = dur
                return

        raise IndexError("Maximum number of modifiers exceeded in ModObj")

    #Changes the modifiers as if one round had passed*/
    def TimeStep(self):
        #we don't need to do anything if there are no modifiers
        if(self.n_mods > 0):

            #go through the modifiers, decrementing each one until they reach 0
            for m in range(0, aic.MAXDMGMODS): 
                if(self.mod_durs[m] - 1) == 0:
                    self.n_mods = self.n_mods - 1
                    self.mod_durs[m] = 0
                    #setting to 0 is effectively removing it by making it a "normal" damage modifier
                    self.modifiers[m] = 0
                elif (self.mod_durs[m] - 1) > 0:
                    self.mod_durs[m] = self.mod_durs[m] - 1

    def GetValue(self):
        if(self.n_mods <= 0):
            return self.base_val
        else: #we need to combine the other modifiers to our base dmg mod
            s = np.sum(self.modifiers)
            
            if s == aic.NORM:
                return aic.NORM
            elif s <= aic.IMMUNE:
                return aic.IMMUNE
            elif s <= aic.RESIST:
                return aic.RESIST
            elif s >= aic.VULN:
                return aic.VULN
            else:
                raise ValueError("Error: invalid dmgmod from DmgMod.GetValue")




class Effects:

    def __init__(self):
        self.n_effects = 0
        self.effects = np.zeros(aic.NEFFECT)
        self.effect_durs =  np.zeros(aic.NEFFECT)

    def ReturnCopy(self):
        copy = Effects()
        copy.n_effects = self.n_effects
        copy.effects = self.effects
        copy.effect_durs = self.effect_durs

    def __str__(self):
        if self.n_effects == 0:
            print("There are no effects currently active")
            return
        else:
            print("Active Effects:")
            for e in range(0,aic.NEFFECT):
                if(self.effects[e]):
                    print("\t", aic.effect_dict[e])
        for e in range(0,aic.NEFFECT):
            if self.effect_durs[e] > 0:
               print("\t",aic.effect_dict[e], "for", self.effect_durs[e])

    #Changes the modifiers as if one round had passed*/
    def TimeStep(self):
        #we don't need to do anything if there are no modifiers
        if(self.n_effects > 0):

            #go through the modifiers, decrementing each one until they reach 0
            for e in range(0, aic.NEFFECT): 
                if(self.effect_durs[e] - 1) == 0:
                    self.n_effects = self.n_effects - 1
                    self.effect_durs[e] = 0
                    #setting to 0 is effectively removing it by making it a "normal" damage modifier
                    self.effects[e] = 0
                elif (self.effect_durs[e] - 1) > 0:
                    self.effect_durs[e] = self.effect_durs[e] - 1

    def GetEffects(self):
        return self.effects