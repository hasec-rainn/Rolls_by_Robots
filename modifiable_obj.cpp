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

        /*removes the modifier at index i*/
        void RemoveMod(short i) {
            nMods--;

            modifiers[i] = 0;
            modDur[i] = 0;
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