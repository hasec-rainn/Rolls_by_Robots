#include<iostream>
#include<cstring>
#include<typeinfo>
#include<cmath>

#ifndef __CONSTANTS_INCLUDED__
#define __CONSTANTS_INCLUDED__
#include "constants.cpp"
#endif


/*Object that has a base value that can be influenced by multiple
modifers. */
class ModObj {

    protected:
        short baseVal; //base value that we are modifying
        short nMods;    //number of modifers acting on baseVal
        short modifiers[MAXMODS]; //all the values that are modifying the base value
        short modDur[MAXMODS];  //time left for each modifer

        /*removes the modifier at index i
        should not be called except for in timestep to ensure
        nMods doesn't go below 0*/
        void RemoveMod(short i) {
            nMods--;
            modifiers[i] = 0;
        }

    public:
        void Init(short BaseVal, short* Modifiers, short* ModDur,\
        short NMods) {  
            baseVal = BaseVal;
            nMods = NMods;

            short i;
            for(i=0; i<MAXMODS; i++) {
                modifiers[i] = Modifiers[i];
                modDur[i] = ModDur[i];
            }
        }

        void Init(short BaseVal) {
            baseVal = BaseVal;
            nMods = 0;

            short i;
            for(i=0; i<MAXMODS; i++) {
                modifiers[i] = 0;
                modDur[i] = 0;
            }
        }

        /*Add a modifier to modBag that will influence the value of 
        baseVal*/
        void AddMod(short modVal, short duration) {
            nMods++;

            //iterate to next open slot, then place 
            short i=0;
            while(modifiers[i] != 0) {
                i++;
                if(i>=MAXMODS) {
                    cout << "\nERROR: too many modifiers!";
                    exit(1);
                }
            }
            modifiers[i] = modVal;
            modDur[i] = duration;
        }

        /*Changes the modifiers as if one round had passed*/
        void TimeStep() {
            //we don't need to do anything if there are no modifiers
            if(nMods > 0) {
                short i;
                for(i=0; i<MAXMODS; i++) { 
                    modDur[i]--;
                    if(modDur[i] == 0) { RemoveMod(i); }
                }
            }
        }

        /*Returns the modified value of baseVal: baseVal + sum(modifiers)*/
        short GetValue() {
            if(nMods != 0) {
                short sum = 0;
                short i;
                for(i=0; i<MAXMODS; i++) { sum = sum + modifiers[i]; }
                return baseVal+sum;
            } else { //there's nothing modifying it; just return baseVal
                return baseVal;
            }
        }

        /*Performs copy by value of two ModObjs*/
        void operator=(ModObj modObj) {
            baseVal = modObj.baseVal;
            nMods = modObj.nMods;
            short i;
            for(i=0; i<MAXMODS; i++) {
                modifiers[i] = modObj.modifiers[i];
                modDur[i] = modObj.modDur[i];
            }
        }
};

class HP : public ModObj {
    public:
        /*Takes away an ammount of HP specifed by "damage"*/
        void SubHP(short damage) {
            
            if(nMods<=0) { //nothing fancy: just subtract directly from baseVal
                baseVal = baseVal - damage;
            } else {    //this player has temp HP; eat through temp HP before base HP
                for(short i=MAXMODS; i>=0; i--) {
                    modifiers[i] = modifiers[i] - damage; //eating through tempHP
                    damage = damage - (damage + modifiers[i]) ; //damage being soaked up by tempHP
                    if( modifiers[i] > 0 ) { //temp health ate up all the damage
                        return; //we don't need to do anything else
                    } else { //damage ate through this stack of temp hp
                        RemoveMod(i);
                    }
                }

                /*Looks like tempHP wasn't enough to absorb all
                the damage; baseVal takes a hit to HP too*/
                baseVal = baseVal - damage;
            }
        }

        /*Heals "healVal" amount of HP by directly adding to baseVal
        of HP. Cannot heal for an ammount greater than "hpMax".*/
        void HealHP(short healVal, short hpMax) {
            baseVal = baseVal + healVal;
            if(baseVal > hpMax) {
                baseVal = hpMax;
            }
        }

        /*Grants "tempHP" amount of temporary HP. Exactly the
        same as "AddMod"*/
        void GiveTempHP(short tempHP, short dur) {
            AddMod(tempHP, dur);
        }

        /*Returns how much temporary HP a character has*/
        short nTempHP() {
            short sum = 0;
            for(short i=0; i<MAXMODS; i++) {
                sum = sum + modifiers[i];}
            return sum;
        }
};

/*Basically just ModObj, but with ability to specifically request
attribute scores and statistic mods (eg str score and str mod)*/
class Attribute : public ModObj {
    public:
        /*Literally just another name for GetValue*/
        short GetScore() { return GetValue(); }

        /*Returns the attribute modifier*/
        short GetMod() {
            float score = GetScore();
            return floor(( score - 10) / 2);
        }
};

/*Container for all the different attributes a DND character has.
ie, STR, DEX, CON, WIS, INT, and CHA*/
class CharacterAttributes {
    private:
        Attribute attArr[NATT];
    public:
        void Init(short str, short dex, short con, short wis, short intel, short cha) {
            attArr[STR].Init(str);
            attArr[DEX].Init(dex);
            attArr[CON].Init(con);
            attArr[WIS].Init(wis);
            attArr[INT].Init(intel);
            attArr[CHA].Init(cha);
        }

        /*Returns a pointer to a requested attribute*/
        Attribute* operator[](short att) {
            return &attArr[att];
        }

        /*Performs copy by value between two Character Attributes*/
        void operator=(CharacterAttributes ca) {
            attArr[STR] = ca.attArr[STR];
            attArr[DEX] = ca.attArr[DEX];
            attArr[CON] = ca.attArr[CON];
            attArr[WIS] = ca.attArr[WIS];
            attArr[INT] = ca.attArr[INT];
            attArr[CHA] = ca.attArr[CHA];
        }
};

/*Object meant to represent the concept of how a character or
creature may take more/less damage, depending on the type of damage*/
class DmgMod {

    protected:
        short baseMods[NDMGTYPE]; //base damage modifiers for each damage type
        short nMods;    //number of modifers acting on the base damage modifiers
        short modifiers[NDMGTYPE]; //all the values that are modifying the base mods
        short modDur[NDMGTYPE];  //time left for each modifer in "modifiers"

        /*Note that, with this set up, only one thing can be modifying the
        base modifier of a particular damage type at once. In other words,
        this model cannot represent multiple modifers acting on one damage
        type at once.*/

        /*Removes the modifier of type "dmgType" from modifiers*/
        void RemoveMod(short dmgType) {
            nMods--;
            modifiers[dmgType] = NORM;
        }

    public:
        /*Takes no arguments. Assumes all values in baseMods are NORM*/
        DmgMod() {
            nMods = 0;

            short i;
            for(i=0; i<NDMGTYPE; i++) {
                baseMods[i] = NORM;
                modifiers[i] = 0;
                modDur[i] = 0;
            }
        }

        /*Takes one argument: an array that defines how the
        character/creature reacts to each damage type*/
        DmgMod(short* BaseMods) {
            nMods = 0;

            short i;
            for(i=0; i<NDMGTYPE; i++) {
                baseMods[i] = BaseMods[i];
                modifiers[i] = 0;
                modDur[i] = 0;
            }
        }

        /*Takes 3 arguments: an array that defines how the
        character/creature reacts to each damage type*/
        void Init(short* BaseMods, short* Modifiers, short* ModDur, short NMods) {
            nMods = NMods;

            short i;
            for(i=0; i<NDMGTYPE; i++) {
                baseMods[i] = BaseMods[i];
                modifiers[i] = Modifiers[i];
                modDur[i] = ModDur[i];
            }
        }

        /*Adds the modifier value "mod" of damage type "dmgtype" to
        the modifiers array. This modifier lasts for "dur" rounds*/
        void AddMod(short dmgType, short mod, short dur) {
            nMods++;

            modifiers[dmgType] = mod;
            modDur[dmgType] = dur;
        }
        
        /*Changes the modifiers as if one round had passed*/
        void TimeStep() {
            //we don't need to do anything if there are no modifiers
            if(nMods > 0) {
                short i;
                for(i=0; i<NDMGTYPE; i++) { 
                    modDur[i]--;
                    if(modDur[i] == 0) { RemoveMod(i); }
                }
            }
        }

        /*Retrieves the character/creatures current damage modifier
        for the damage type "dmgType"*/
        short operator[](short dmgType) {
            if(nMods > 0) {
                if(baseMods[dmgType] == NORM || modifiers[dmgType] == NORM) {
                    //Since NORM=1, NORM*otherMod == otherMod
                    return baseMods[dmgType] * modifiers[dmgType];
                } else if (baseMods[dmgType] == IMMUNE || modifiers[dmgType] == IMMUNE) {
                    return IMMUNE;
                } else if (baseMods[dmgType] == modifiers[dmgType]) {
                    /*Note that mod values can only be RESIST or VULN at this point*/
                    return baseMods[dmgType];
                } else {
                    /*Given that mod values can only be RESIST or VULN, and
                    that our mod values are not equal, we must have one RESIST
                    and one VULN*/
                    return NORM;
                }
            } else { //nothing modifying the base mod; just return base
                return baseMods[dmgType];
            }
        }

        /*Performs copy by value of two DmgMods*/
        void operator=(DmgMod dmgModifiers) {
            nMods = dmgModifiers.nMods;
            short i;
            for(i=0;i<NDMGTYPE; i++) {
                baseMods[i] = dmgModifiers.baseMods[i];
                modifiers[i] = dmgModifiers.modifiers[i];
                modDur[i] = dmgModifiers.modDur[i];
            }
        }
};

/*Class that holds the effects currently active on a character.
Additionally, holds information regarding which effects character
is immune to.
When indexed using [], each index corresponds to a specific status effect.
(see the constants.cpp for which index represents what)
true means that the particular effect is affecting the character, 
false the particular effect is not affecting the character.*/
class Effects {
    private:
        bool effects[NEFFECT]; //effects which are applied to the character
        short effectDurations[NEFFECT];

        bool effectImmunities[NEFFECT]; //1 for vulnurable, 0 for immune
        bool activeEffects[NEFFECT]; // bitwise multiplication of effects & immunities

    public:

        void Init() {
            for(short i=0; i<NEFFECT; i++) {
                effectImmunities[i] = 1;
                effects[i] = 0;
                effectDurations[i] = 0;
            }
        }

        void Init(bool* EffectImmunities, bool* Effects, short* Durations) {
            for(short i=0; i<NEFFECT; i++) {
                effectImmunities[i] = EffectImmunities[i];
                effects[i] = Effects[i];
                effectDurations[i] = Durations[i];
            }
        }

        /*Adjusts the effects applied to the character as if 
        one round had passed*/
        void TimeStep() {
            short i;
            for(i=0; i<NEFFECT; i++) { 
                effectDurations[i]--;
                if(effectDurations[i] <= 0) { 
                    effects[i] = false; 
                    effectDurations[i] = 0; /*Prevents underflow from --*/
                }
            }   
        }

        /*Applies the effect "effect" to the character 
        for duration "dur"*/
        void AddEffect(short effect, short dur) {
            effects[effect] = true;
            /*If the player is already affected with effect,
            effect duration is determined by longest*/
            if(effectDurations[effect] < dur) {
                effectDurations[effect] = dur;}
        }

        /*View the effects currently affecting the character.
        Effect is currently affecting character if 
        effects[i] x effectImmunities[i] = 1 */
        bool* GetActive() {
            for(short i=0; i<NEFFECT; i++) {
                activeEffects[i] = effects[i] * effectImmunities[i];
            }
            return activeEffects;
        }

        /*Returns true if the effect "effect" is currently affecting
        the character*/
        bool operator[](short effect) {
            return (effects[effect] * effectImmunities[effect]);
        }

        /*Performs copy by value of two Effect objects*/
        void operator=(Effects e) {
            for(short i=0; i<NEFFECT; i++) {
                effectImmunities[i] = e.effectImmunities[i];
                effects[i] = e.effects[i];
                effectDurations[i] = e.effectDurations[i];
            }
        }
};