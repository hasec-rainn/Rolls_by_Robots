
#include<iostream>
#include<cstring>
#include<typeinfo>
#include<cmath>

#ifndef __CONSTANTS_INCLUDED__
#define __CONSTANTS_INCLUDED__
#include "constants.cpp"
#endif

using namespace std;

// https://rpg.stackexchange.com/questions/70335/how-do-i-calculate-the-chance-to-hit-a-given-ac?newreg=7e3de3c84d9a42ba96b932f394793d7f


class Action {
    protected:
        char name[STRSIZE]; //make sure its \0 terminated char*
        short range;

    protected:
        void InitBase(char* Name, char* Type, short Range)\
        {
            memcpy(name, Name, STRSIZE);
            memcpy(type, Type, STRSIZE);       
            range = Range;
        }

        /*Displays the basic attributes of an Action object via printing to
        stdout*/
        void PrintBase() {
            cout << "\n###### " << type << " Attributes ######";
            cout << "\n\tName: " << name;
            cout << "\n\tRange: " << range;
            cout << "\n";
        }

    public:
        char type[STRSIZE] = "DEFAULT\0";

        /*Returns the range of the Action, in feet*/
        short GetRange() {
            return range;
        }

        virtual void PrintAtt() {
            cout << "DEFAULT PRINTATT";
            return;
        }
};



class MeleeAtk : public Action {
    protected:
        short damage;
        char dmgType[STRSIZE];
        short toHit;       //how much do we + (or -) from dice roll?

    public:

        char type[STRSIZE] = "MeleeAtk\0";

        void Init(char* Name, short ToHit, short Range,\
                  short Dmg, char* DmgT)\
        {
            InitBase(Name,type,Range);

            toHit = ToHit;
            damage = Dmg;
            memcpy(dmgType, DmgT, STRSIZE);
        }

        /*Displays the attributes of an Action object via printing to
        stdout*/
        void PrintAtt() {
            PrintBase();
            cout << "\n\tDamage: " << damage;
            cout << "\n\tDamage type: " << dmgType;
            cout << "\n\tTo hit bonus: " << toHit;
        }
};



class RangedAtk : public Action {
    protected:
        short damage;
        char dmgType[STRSIZE];
        short toHit;       //how much do we + (or -) from dice roll?

    public:

        char type[STRSIZE] = "RangedAtk\0";

        void Init(char* Name, short ToHit, short Range,\
                  short Dmg, char* DmgT)\
        {
            InitBase(Name,type,Range);

            toHit = ToHit;
            damage = Dmg;
            memcpy(dmgType, DmgT, STRSIZE);
        }

        /*Displays the attributes of an Action object via printing to
        stdout*/
        void PrintAtt() {
            PrintBase();
            cout << "\n\tDamage: " << damage;
            cout << "\n\tDamage type: " << dmgType;
            cout << "\n\tTo hit bonus: " << toHit;
        }
};



/*Action that requires someone to make a saving throw. 
If they fail, they take damage.*/
class DamageSave : public Action {
    protected:
        short damage;
        char dmgType[STRSIZE];
        
        short saveDC;
        char saveType[STRSIZE];
        bool halfOnSuccess;     //even if someone succeeds, still take 1/2 dmg

    public:

        char type[STRSIZE] = "DamageSave\0";

        void Init(char* Name, short Range, short Dmg, char* DmgT,\
                  short SaveDC,char* SaveType, bool HalfOnSucc)
        {
            InitBase(Name,type,Range);

            damage = Dmg;
            memcpy(dmgType, DmgT, STRSIZE);
            saveDC = SaveDC;
            memcpy(saveType, SaveType, STRSIZE);
            halfOnSuccess = HalfOnSucc;
        }

        /*Displays the attributes of an Action object via printing to
        stdout*/
        void PrintAtt() {
            PrintBase();
            cout << "\n\tDamage: " << damage;
            cout << "\n\tDamage type: " << dmgType;
            cout << "\n\tSave DC: " << saveDC;
            cout << "\n\tSave Type: " << saveType;
            cout << "\n\tHalf DMG on success? " << halfOnSuccess;
        }
};


/*Action that requires someone to make a saving throw. 
If they fail, they are subjected to a negative condition.*/
class ConditionSave : public Action {
    protected:
        char condition[STRSIZE];
        short duration; //in rounds
        
        short saveDC;
        char saveType[STRSIZE];

    public:

        char type[STRSIZE] = "ConditionSave\0";

        void Init(char* Name, short Range, char* Condition,\
                  short Duration, short SaveDC, char* SaveType)\
        {
            InitBase(Name,type,Range);

            memcpy(condition,Condition, STRSIZE);
            duration = Duration;

            saveDC = SaveDC;
            memcpy(saveType, SaveType, STRSIZE);
        }

        /*Displays the attributes of an Action object via printing to
        stdout*/
        void PrintAtt() {
            PrintBase();
            cout << "\n\tCondition: " << condition;
            cout << "\n\tDuration: " << duration;
            cout << "\n\tSave DC: " << saveDC;
            cout << "\n\tSave Type: " << saveType;
        }
};



/*Action that heals a target character a certain amount*/
class HealBuff : public Action {
    protected:
        short healing;

    public:

        char type[STRSIZE] = "HealBuff\0";

        void Init(char* Name, short Range, short Healing) {
            InitBase(Name,type,Range);

            healing = Healing;
        }

        /*Displays the attributes of an Action object via printing to
        stdout*/
        void PrintAtt() {
            PrintBase();
            cout << "\n\tHealing Amount: " << healing;
        }
};



/*Action that heals the character using this action a certain amount
CANNOT BE USED ON OTHER CHARACTERS*/
class SelfHealBuff : public Action {
    protected:
        short healing;

    public:

        char type[STRSIZE] = "SelfHealBuff\0";

        void Init(char* Name, short Range, short Healing) {
            InitBase(Name,type,Range);

            healing = Healing;
        }

        /*Displays the attributes of an Action object via printing to
        stdout*/
        void PrintAtt() {
            PrintBase();
            cout << "\n\tHealing Amount: " << healing;
        }
};


/*Action that gives a positive condition to a character*/
class ConditionBuff : public Action {
    protected:
        char effect[STRSIZE];
        short duration;

    public:

        char type[STRSIZE] = "ConditionBuff\0";

        void Init(char* Name, short Range, char* Effect, short Duration) {
            InitBase(Name,type,Range);

            memcpy(effect, Effect,STRSIZE);
            duration = Duration;
        }

        /*Displays the attributes of an Action object via printing to
        stdout*/
        void PrintAtt() {
            PrintBase();
            cout << "\n\tCondition: " << effect;
            cout << "\n\tDuration: " << duration;
        }
};



/*Action that gives a positive condition to the character that has
this buff. CANNOT BE USED ON OTHER CHARACTERS*/
class SelfCondBuff : public Action {
    protected:
        char effect[STRSIZE];
        short duration;

    public:

        char type[STRSIZE] = "SelfCondBuff\0";

        void Init(char* Name, short Range, char* Effect, short Duration) {
            InitBase(Name,type,Range);

            memcpy(effect, Effect,STRSIZE);
            duration = Duration;
        }

        /*Displays the attributes of an Action object via printing to
        stdout*/
        void PrintAtt() {
            PrintBase();
            cout << "\n\tCondition: " << effect;
            cout << "\n\tDuration: " << duration;
        }
};

/*The action bundle is a list of simple actions.
The action bundle is useful for creating complex actions that do
more than one thing to a character or characters*/
class ActionBundle : public Action {
    protected:
        short nActions;
        Action** actions;
    public:
        void Init(Action** Actions, short NActions) {
            nActions = NActions;
            actions = new Action*[nActions];
        }

        void PrintAtt() {
            for(int i=0; i<nActions; i++) {
                cout << "action type [" << i << "]: " << actions[i]->type;
            }
        }
};
