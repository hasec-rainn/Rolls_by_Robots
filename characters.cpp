#include<iostream>
#include<cstring>
#include<typeinfo>
#include<cmath>


#include "actions.cpp"
#include "modifiable_obj.cpp"
#ifndef __CONSTANTS_INCLUDED__
#define __CONSTANTS_INCLUDED__
#include "constants.cpp"
#endif



// https://rpg.stackexchange.com/questions/70335/how-do-i-calculate-the-chance-to-hit-a-given-ac?newreg=7e3de3c84d9a42ba96b932f394793d7f

/********************************************************************
 * Class: Character
 * Desc: Character contains all the relevant information regarding a
 *       player character or NPC.
 * 
 * Ideology: 
********************************************************************/
class Character {
    private:
        ModObj maxHP; short hp; //note: this system cannot represent temp HP
        short ac;   //assume armor is static: system cannot represent taking cover
        ModObj speed;   //speed boosts & reductions are representable
        short profBonus;

        /*dmgMods is an object which details
        how the character is afflicted by a certain damage type.
        The value contained for a particular damage type describes how 
        the character is impacted. 
        Below are the possible values that may show up:

        0 -> character takes no damage (has immunity to damage source)
        -2 -> character takes half damage (has resistance to dmg source)
        1 -> character takes normal damage
        2 -> character takes double damage (has vulnerability to dmg source)*/
        DmgMod damageMods;

        /*Each index in "effects" corresponds to a specific status effect
        (see the char[][] status at top of file.)
        True (1) means that the particular effect is active, false means
        the particular effect is not active.*/
        bool effects[NEFFECT];
        bool effectImmunities[NEFFECT]; //1 for vulnurable, 0 for immune (for bitwise multiplication)
        short effectDurations[NEFFECT];

        Attribute attributes[NATT]; //str, dex, con, int, wis, cha

        bool attAdv[NATT];  //true if adv for respective ability
        bool attDis[NATT];  //true if disadv for respective ability

        short nAct; Action** actions; //an array of nAct-many Action*

    public:

        Character(ModObj MaxHP, short HP, short AC, ModObj Speed,\
                  DmgMod DmgMods, Attribute* Attributes, bool* Effects,
                  Action** Actions, short NAct)
        {
            maxHP = MaxHP; hp = HP;
            ac = AC;
            speed = Speed;
            
            //copy in str, dex, con, ... into respective attribute slots
            for(short att=0; att<NATT; att++) {
                attributes[att] = Attributes[att];}

            for(int i=0; i<NEFFECT; i++) {
                effects[i] = Effects[i];}

            nAct = NAct; actions = Actions;

            //for(short act=0; act<NAct; act++) {
            //    actions[act] = Actions[act]; }
        }

        /*Print everything you'd ever want to know about the character*/
        void PrintAtt() {
            cout << "\n###### Character Attributes ######";
            cout << "\n\tMax HP: " << maxHP.GetValue();
            cout << "\n\tCurrent HP: " << hp;
            cout << "\n\tAC: " << ac;
            cout << "\n\tSpeed: " << speed.GetValue();
            cout << "\n\tDamage Modifier Array: ";
            for(int i=0; i<NDMGTYPE; i++) {
                cout << "\n\t\tDmgType[" << i << "]:" << dmgTypeDict[i] << ", mod: " << damageMods[i];
            }
            cout << "\n\tActive effects:";
            for(int i=0; i<NEFFECT; i++) {
                cout << "\n\t\teffect " << statusDict[i] << ": " << effects[i];
            }

            cout << "\n\tAttribute scores:";
            for(short att=0; att<NATT; att++) {
                cout << "\n\t\t" << attDict[att] << ": " << attributes[att].GetScore();
            }
            
            cout << "\n\tAction types:";
            for(int i=0; i<nAct; i++) {
                cout << "\n\t\tAction[" << i << "] type: " << actions[i]->GetName();
            }



        }

        short GetHP() {return hp;}
        short GetSpeed() {return speed.GetValue();}

        /***********************************************************
         * Function: ApplyAction(MeleeAtk* action, short hitMod, short dmgMod)
         * 
         * Desc: Applies a particular action to this character.
         *       The action may come from another character, or
         *       it could potentially come from this character.
         *  
         *       Since this action is an attack, the character may lose 
         *       health and/or receive a negative effect.
        ***********************************************************/
        void ApplyAction(MeleeAtk* a, short hitMod, short dmgMod) {
            cout << "\nlooks like this is a melee attack";
            return;
        }

        /***********************************************************
         * Function: ApplyAction(RangedAtk* action, short hitMod, short dmgMod)
         * 
         * Desc: Applies a particular action to this character.
         *       The action may come from another character, or
         *       it could potentially come from this character.
         *  
         *       Since this action is an attack, the character may lose 
         *       health and/or receive a negative effect.
        ***********************************************************/
        void ApplyAction(RangedAtk* a, short hitMod, short dmgMod) {
            cout << "\nlooks like this is a ranged attack";
            return;
        }

        /***********************************************************
         * Function: ApplyAction(DamageSave* action, short dmgMod)
         * 
         * Desc: Applies a particular action to this character.
         *       The action may come from another character, or
         *       it could potentially come from this character.
         *  
         *       Since this action is an attack, the character may lose 
         *       health and/or receive a negative effect.
        ***********************************************************/
        void ApplyAction(DamageSave* a, short dmgMod) {
            cout << "\nlooks like this is a Damage Save";
            return;
        }

        /***********************************************************
         * Function: ApplyAction(ConditionSave* action)
         * 
         * Desc: Applies a particular action to this character.
         *       The action may come from another character, or
         *       it could potentially come from this character.
         *  
         *       Since this action is an attack, the character may lose 
         *       health and/or receive a negative effect.
        ***********************************************************/
        void ApplyAction(ConditionSave* a) {
            cout << "\nlooks like this is a Condition Save";
            return;
        }

        /***********************************************************
         * Function: ApplyAction(HealBuff* action, short hitMod, short healMod)
         * 
         * Desc: Applies a particular action to this character.
         *       The action may come from another character, or
         *       it could potentially come from this character.
         *  
         *       Since this action is an buff, the character may recieve 
         *       health and/or receive a positive effect.
        ***********************************************************/
        void ApplyAction(HealBuff* a, short hitMod, short healMod) {
            cout << "\nlooks like this is a Condition Save";
            return;
        }
};