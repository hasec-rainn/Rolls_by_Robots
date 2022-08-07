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

            short i=0;
            while(modifiers[i] != 0) {i++;}
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
};

/*Basically just ModObj, but with ability to specifically request
attribute scores and statistic mods (eg str score and str mod)*/
class Attribute : public ModObj {
    public:
        /*Literally just another name for GetValue*/
        short GetScore() { return GetValue(); }

        /*Returns the attribute modifier*/
        short GetMod() {
            /*Negative values may be off by 1*/
            return (GetValue() - 10) / 2;
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

        /*Removes the modifier of type "dmgType" from modifiers*/
        void RemoveMod(short dmgType) {
            nMods--;
            modifiers[dmgType] = NORM;
        }

    public:
        /*Takes no arguments. Assumes all values in baseMods are NORM*/
        void Init() {  
            nMods = 0;

            short i;
            for(i=0; i<NDMGTYPE; i++) {
                baseMods[i] = NORM;
                modifiers[i] = NULL;
                modDur[i] = NULL;
            }
        }

        /*Takes one argument: an array that defines how the
        character/creature reacts to each damage type*/
        void Init(short* BaseMods) {
            nMods = 0;

            short i;
            for(i=0; i<NDMGTYPE; i++) {
                baseMods[i] = BaseMods[i];
                modifiers[i] = NULL;
                modDur[i] = NULL;
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

        void operator=(DmgMod* dmgModifiers) {
            short i;
            for(i=0;i<NDMGTYPE; i++) {
                nMods = dmgModifiers->nMods;
                baseMods[i] = dmgModifiers->baseMods[i];
                modifiers[i] = dmgModifiers->modifiers[i];
                modDur[i] = dmgModifiers->modDur[i];
            }
        }
};