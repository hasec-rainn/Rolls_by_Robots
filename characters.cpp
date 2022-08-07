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
        char name[STRSIZE];
        ModObj maxHP; ModObj hp;
        ModObj ac;
        ModObj speed;
        short profBonus;

        /*The dmgModArr is an array which details
        how the character is afflicted by a certain damage type. Each index
        corresponds to to the corresponding damage type in the "dmgType"
        array.
        The value contained at a particular index describes how the character
        is impacted. Below are the possible values that may show up:

        0 -> character takes no damage (has immunity to damage source)
        -2 -> character takes half damage (has resistance to dmg source)
        1 -> character takes normal damage
        2 -> character takes double damage (has vulnerability to dmg source)*/
        short defDmgModArr[NDMGTYPE];
        short dmgModArr[NDMGTYPE];
        short dmgModDur[NDMGTYPE]; //keep track of how long

        /*Each index in "effects" corresponds to a specific status effect
        (see the char[][] status at top of file.)
        True 1 means that the particular effect is active, false means
        the particular effect is not active.*/
        bool effects[NEFFECT];
        short effectDurations[NEFFECT];

        Attribute strength;
        Attribute dexterity;
        Attribute constitution;
        Attribute intelligence;
        Attribute wisedom;
        Attribute charisma;

        bool attAdv[NATT];  //true if adv for respective ability
        bool attDis[NATT];  //true if disadv for respective ability

        short nAct; Action** actions; //an array of nAct-many Action*

    public:

        Character(short MaxHP, short HP, short AC, short Speed,\
                  short* DmgModArr, bool* Effects, short* scoreArr, short* modArr,\
                  Action** Actions, short NAct)
        {
            maxHP = MaxHP; hp = HP;
            ac = AC;
            speed = Speed;
            for(int i=0; i<NDMGTYPE; i++) {
                dmgModArr[i] = DmgModArr[i];
            }
            strScore = scoreArr[0]; strMod = modArr[0];
            dexScore = scoreArr[1]; dexMod = modArr[1];
            conScore = scoreArr[2]; conMod = modArr[2];
            intScore = scoreArr[3]; intMod = modArr[3];
            wisScore = scoreArr[4]; wisMod = modArr[4];
            chaScore = scoreArr[5]; chaMod = modArr[5];

            for(int i=0; i<NEFFECT; i++) {
                effects[i] = Effects[i];
            }

            nAct = NAct; actions = Actions;
        }

        /*Print everything you'd ever want to know about the character*/
        void PrintAtt() {
            cout << "\n###### Character " << name << " Attributes ######";
            cout << "\n\tMax HP: " << maxHP;
            cout << "\n\tCurrent HP: " << hp;
            cout << "\n\tAC: " << ac;
            cout << "\n\tSpeed: " << speed;
            cout << "\n\tDamage Modifier Array: ";
            for(int i=0; i<NDMGTYPE; i++) {
                cout << "\n\t\tDmgType[" << i << "]:" << dmgType[i] << ", mod: " << dmgModArr[i];
            }
            cout << "\n\tActive effects:";
            for(int i=0; i<NEFFECT; i++) {
                cout << "\n\t\teffect " << status[i] << ": " << effects[i];
            }

            cout << "\n\tSTR score: " << strScore << " (Mod: " << strMod << ")";
            cout << "\n\tDEX score: " << dexScore << " (Mod: " << dexMod << ")";
            cout << "\n\tCON score: " << conScore << " (Mod: " << conMod << ")";
            cout << "\n\tINT score: " << intScore << " (Mod: " << intMod << ")";
            cout << "\n\tWIS score: " << wisScore << " (Mod: " << wisMod << ")";
            cout << "\n\tCHA score: " << chaScore << " (Mod: " << chaMod << ")";
            
            cout << "\n\tAction types:";
            for(int i=0; i<nAct; i++) {
                cout << "\n\t\tAction[" << i << "] type: " << actions[i]->type;
            }



        }

        short GetHP() {return hp;}
        short GetSpeed() {return speed;}

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


int main() {

    MeleeAtk clubStrike; clubStrike.Init("Club Strike\0",8,5,7,"Bludgeoning\0");
    RangedAtk axeThrow; axeThrow.Init("Axe Throw\0", 8, 120, 12, "Piercing\0");
    DamageSave bearHug; bearHug.Init("Bear Hug\0",5,20,"Bludgeoning\0",14,"Dex\0",false);
    ConditionSave knockout; knockout.Init("Knockout Punch\0",5,"Incapacitated\0",2,14,"Con\0"); 
    HealBuff goodBerry; goodBerry.Init("Good Berry\0",5, 1);
    SelfCondBuff rage;


    short scores[] = {18,16,16,8,10,7};
    short mods[] = {4,3,3,-1,0,-2};
    bool effects[NEFFECT] = {}; 

    short nAct = 6;
    Action* atkPtrArr[6];
    atkPtrArr[0] = &clubStrike;
    atkPtrArr[1] = &axeThrow;
    atkPtrArr[2] = &bearHug;
    atkPtrArr[3] = &knockout;


    short dmgModArr[NDMGTYPE] = {1,1,1,1,1,1,1,1,1,1,1,1,1};

    // for(int i=0; i<4; i++) {
    //     atkPtrArr[i]->PrintAtt();
    // }

    Character thageth = {65,65,16,30,dmgModArr,effects,scores,mods,atkPtrArr,nAct};

    thageth.ApplyAction(&knockout);

    return 0;
}