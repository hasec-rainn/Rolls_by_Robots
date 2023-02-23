import numpy as np
from math import floor
import ai_constants as aic

# Object that has a base value that can be influenced by multiple
# modifers.
class ModObj:

    def __init__(self, base_val):
        self.base_val = base_val #base value that we are modifying
        self.n_mods = 0    #number of modifers acting on baseVal
        self.modifiers = np.zeros(aic.MAXMODS) #all the values that are modifying the base value
        self.mod_durs = np.zeros(aic.MAXMODS)  #time left for each modifer

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
            

    # Returns deep of this ModObj (note that name att is copy by reference)
    def ReturnCopy(self):
        copy = ModObj(self.base_val,self.n_mods)

        copy.modifiers = self.modifiers.copy()
        copy.mod_durs = self.mod_durs.copy()

        return copy
    



class Health(ModObj):

    def __init__(self,max_hp):
        ModObj.__init__(self,max_hp)
        self.max_hp = max_hp
    
    def __str__(self):
        return ("\nVV Max HP VV" + ModObj.__str__(self))

    # Takes away an ammount of HP specifed by "damage"
    def SubHP(self, damage):
        print("damage", damage)
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
    
    def __str__(self):
        return ("\nAttribute: " + aic.att_dict[self.att_id] + ModObj.__str__(self))
        
    def GetScore(self):
        return self.GetValue(self)

    
    def GetMod(self):
        return floor(( self.GetValue(self) - 10) / 2)

# /*Container for all the different attributes a DND character has.
# ie, STR, DEX, CON, WIS, INT, and CHA*/
# class CharacterAttributes {
#     private:
#         Attribute attArr[NATT];
#     public:
#         void Init(short str, short dex, short con, short wis, short intel, short cha) {
#             attArr[STR].Init(str);
#             attArr[DEX].Init(dex);
#             attArr[CON].Init(con);
#             attArr[WIS].Init(wis);
#             attArr[INT].Init(intel);
#             attArr[CHA].Init(cha);
#         }

#         /*Returns a pointer to a requested attribute*/
#         Attribute* operator[](short att) {
#             return &attArr[att];
#         }

#         /*Performs copy by value between two Character Attributes*/
#         void operator=(CharacterAttributes ca) {
#             attArr[STR] = ca.attArr[STR];
#             attArr[DEX] = ca.attArr[DEX];
#             attArr[CON] = ca.attArr[CON];
#             attArr[WIS] = ca.attArr[WIS];
#             attArr[INT] = ca.attArr[INT];
#             attArr[CHA] = ca.attArr[CHA];
#         }
# };

# /*Object meant to represent the concept of how a character or
# creature may take more/less damage, depending on the type of damage*/
# class DmgMod {

#     protected:
#         short baseMods[NDMGTYPE]; #base damage modifiers for each damage type
#         short nMods;    #number of modifers acting on the base damage modifiers
#         short modifiers[NDMGTYPE]; #all the values that are modifying the base mods
#         short modDur[NDMGTYPE];  #time left for each modifer in "modifiers"

#         /*Note that, with this set up, only one thing can be modifying the
#         base modifier of a particular damage type at once. In other words,
#         this model cannot represent multiple modifers acting on one damage
#         type at once.*/

#         /*Removes the modifier of type "dmgType" from modifiers*/
#         void RemoveMod(short dmgType) {
#             nMods--;
#             modifiers[dmgType] = NORM;
#         }

#     public:
#         /*Takes no arguments. Assumes all values in baseMods are NORM*/
#         DmgMod() {
#             nMods = 0;

#             short i;
#             for(i=0; i<NDMGTYPE; i++) {
#                 baseMods[i] = NORM;
#                 modifiers[i] = 0;
#                 modDur[i] = 0;
#             }
#         }

#         /*Takes one argument: an array that defines how the
#         character/creature reacts to each damage type*/
#         DmgMod(short* BaseMods) {
#             nMods = 0;

#             short i;
#             for(i=0; i<NDMGTYPE; i++) {
#                 baseMods[i] = BaseMods[i];
#                 modifiers[i] = 0;
#                 modDur[i] = 0;
#             }
#         }

#         /*Takes 3 arguments: an array that defines how the
#         character/creature reacts to each damage type*/
#         void Init(short* BaseMods, short* Modifiers, short* ModDur, short NMods) {
#             nMods = NMods;

#             short i;
#             for(i=0; i<NDMGTYPE; i++) {
#                 baseMods[i] = BaseMods[i];
#                 modifiers[i] = Modifiers[i];
#                 modDur[i] = ModDur[i];
#             }
#         }

#         /*Adds the modifier value "mod" of damage type "dmgtype" to
#         the modifiers array. This modifier lasts for "dur" rounds*/
#         void AddMod(short dmgType, short mod, short dur) {
#             nMods++;

#             modifiers[dmgType] = mod;
#             modDur[dmgType] = dur;
#         }
        
#         /*Changes the modifiers as if one round had passed*/
#         void TimeStep() {
#             #we don't need to do anything if there are no modifiers
#             if(nMods > 0) {
#                 short i;
#                 for(i=0; i<NDMGTYPE; i++) { 
#                     modDur[i]--;
#                     if(modDur[i] == 0) { RemoveMod(i); }
#                 }
#             }
#         }

#         /*Retrieves the character/creatures current damage modifier
#         for the damage type "dmgType"*/
#         short operator[](short dmgType) {
#             if(nMods > 0) {
#                 if(baseMods[dmgType] == NORM || modifiers[dmgType] == NORM) {
#                     #Since NORM=1, NORM*otherMod == otherMod
#                     return baseMods[dmgType] * modifiers[dmgType];
#                 } else if (baseMods[dmgType] == IMMUNE || modifiers[dmgType] == IMMUNE) {
#                     return IMMUNE;
#                 } else if (baseMods[dmgType] == modifiers[dmgType]) {
#                     /*Note that mod values can only be RESIST or VULN at this point*/
#                     return baseMods[dmgType];
#                 } else {
#                     /*Given that mod values can only be RESIST or VULN, and
#                     that our mod values are not equal, we must have one RESIST
#                     and one VULN*/
#                     return NORM;
#                 }
#             } else { #nothing modifying the base mod; just return base
#                 return baseMods[dmgType];
#             }
#         }

#         /*Performs copy by value of two DmgMods*/
#         void operator=(DmgMod dmgModifiers) {
#             nMods = dmgModifiers.nMods;
#             short i;
#             for(i=0;i<NDMGTYPE; i++) {
#                 baseMods[i] = dmgModifiers.baseMods[i];
#                 modifiers[i] = dmgModifiers.modifiers[i];
#                 modDur[i] = dmgModifiers.modDur[i];
#             }
#         }
# };

# /*Class that holds the effects currently active on a character.
# Additionally, holds information regarding which effects character
# is immune to.
# When indexed using [], each index corresponds to a specific status effect.
# (see the constants.cpp for which index represents what)
# true means that the particular effect is affecting the character, 
# false the particular effect is not affecting the character.*/
# class Effects {
#     private:
#         bool effects[NEFFECT]; #effects which are applied to the character
#         short effectDurations[NEFFECT];

#         bool effectImmunities[NEFFECT]; #1 for vulnurable, 0 for immune
#         bool activeEffects[NEFFECT]; # bitwise multiplication of effects & immunities

#     public:

#         void Init() {
#             for(short i=0; i<NEFFECT; i++) {
#                 effectImmunities[i] = 1;
#                 effects[i] = 0;
#                 effectDurations[i] = 0;
#             }
#         }

#         void Init(bool* EffectImmunities, bool* Effects, short* Durations) {
#             for(short i=0; i<NEFFECT; i++) {
#                 effectImmunities[i] = EffectImmunities[i];
#                 effects[i] = Effects[i];
#                 effectDurations[i] = Durations[i];
#             }
#         }

#         /*Adjusts the effects applied to the character as if 
#         one round had passed*/
#         void TimeStep() {
#             short i;
#             for(i=0; i<NEFFECT; i++) { 
#                 effectDurations[i]--;
#                 if(effectDurations[i] <= 0) { 
#                     effects[i] = false; 
#                     effectDurations[i] = 0; /*Prevents underflow from --*/
#                 }
#             }   
#         }

#         /*Applies the effect "effect" to the character 
#         for duration "dur"*/
#         void AddEffect(short effect, short dur) {
#             effects[effect] = true;
#             /*If the player is already affected with effect,
#             effect duration is determined by longest*/
#             if(effectDurations[effect] < dur) {
#                 effectDurations[effect] = dur;}
#         }

#         /*View the effects currently affecting the character.
#         Effect is currently affecting character if 
#         effects[i] x effectImmunities[i] = 1 */
#         bool* GetActive() {
#             for(short i=0; i<NEFFECT; i++) {
#                 activeEffects[i] = effects[i] * effectImmunities[i];
#             }
#             return activeEffects;
#         }

#         /*Returns true if the effect "effect" is currently affecting
#         the character*/
#         bool operator[](short effect) {
#             return (effects[effect] * effectImmunities[effect]);
#         }

#         /*Performs copy by value of two Effect objects*/
#         void operator=(Effects e) {
#             for(short i=0; i<NEFFECT; i++) {
#                 effectImmunities[i] = e.effectImmunities[i];
#                 effects[i] = e.effects[i];
#                 effectDurations[i] = e.effectDurations[i];
#             }
#         }
# };