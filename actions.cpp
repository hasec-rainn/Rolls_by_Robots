
#include<iostream>
#include<cstring>
#include<typeinfo>
#include<cmath>

#ifndef __CONSTANTS_INCLUDED__
#define __CONSTANTS_INCLUDED__
#include "constants.cpp"
#endif

//Need to include characters.cpp for the Polymorph class
#ifndef __CHARACTERS_INCLUDED__
#define __CHARACTERS_INCLUDED__
#include "characters.cpp"
#endif

using namespace std;

// https://rpg.stackexchange.com/questions/70335/how-do-i-calculate-the-chance-to-hit-a-given-ac?newreg=7e3de3c84d9a42ba96b932f394793d7f


class Action {
    protected:
        char name[STRSIZE]; //make sure its \0 terminated char*
        char type[STRSIZE] = "DEFAULT\0";
        short att; //what stat (STR, DEX, ect) is associated with this action?
        short range;

    protected:
        void InitBase(char* Name, char* Type, short Range, short Att) {
            memcpy(name, Name, STRSIZE);
            memcpy(type, Type, STRSIZE);
            att = Att; 
            range = Range;
        }

        /*Displays the basic attributes of an Action object via printing to
        stdout*/
        void PrintBase() {
            cout << "\n###### " << type << " Attributes ######";
            cout << "\n\tName: " << name;
            cout << "\n\tAssociated attribute: " << att;
            cout << "\n\tRange: " << range;
            cout << "\n";
        }

    public:
        /*Returns the range of the Action, in feet*/
        short GetRange() { return range; }
        char* GetType() { return type; }
        short GetAtt() { return att; }

        virtual void PrintAtt() {
            cout << "DEFAULT PRINTATT";
            return;
        }
};



class MeleeAtk : public Action {
    protected:
        short damage;
        char dmgType[STRSIZE];
        bool useProf;

    public:
        void Init(char* Name, short Att, bool UseProf, short Range,\
                  short Dmg, char* DmgT)\
        {
            InitBase(Name, "MeleeAtk\0", Range, Att);

            damage = Dmg;
            useProf = UseProf;
            memcpy(dmgType, DmgT, STRSIZE);
        }

        //calculates the to-hit modifier of an attack
        short ToHit(short attBonus, short profBonus) {
            if (profBonus) {
                return attBonus+profBonus;
            } else {
                return attBonus;
            } 
        }

        /*Displays the attributes of an Action object via printing to
        stdout*/
        void PrintAtt() {
            PrintBase();
            cout << "\n\tDamage: " << damage;
            cout << "\n\tDamage type: " << dmgType;
            cout << "\n\tUses proficiency? " << useProf;
        }
};



class RangedAtk : public Action {
    protected:
        short damage;
        char dmgType[STRSIZE];
        bool useProf;

    public:
        void Init(char* Name, short Att, bool UseProf, short Range,\
                  short Dmg, char* DmgT)\
        {
            InitBase(Name,"RangedAtk\0",Range, Att);

            useProf = UseProf;
            damage = Dmg;
            memcpy(dmgType, DmgT, STRSIZE);
        }

        //calculates the to-hit modifier of an attack
        short ToHit(short attBonus, short profBonus) {
            if (profBonus) {
                return attBonus+profBonus;
            } else {
                return attBonus;
            } 
        }

        /*Displays the attributes of an Action object via printing to
        stdout*/
        void PrintAtt() {
            PrintBase();
            cout << "\n\tDamage: " << damage;
            cout << "\n\tDamage type: " << dmgType;
            cout << "\n\tUses proficiency? " << useProf;
        }
};



/*Action that requires someone to make a saving throw. 
If they fail, they take damage.*/
class DamageSave : public Action {
    protected:
        short damage;
        char dmgType[STRSIZE];
        char saveType[STRSIZE];
        bool halfOnSuccess;     //even if someone succeeds, still take 1/2 dmg

    public:
        void Init(char* Name, short Att, bool UseProf, short Range, short Dmg, char* DmgT,\
                  char* SaveType, bool HalfOnSucc)
        {
            InitBase(Name,"DamageSave\0",Range,Att);

            damage = Dmg;
            memcpy(dmgType, DmgT, STRSIZE);
            memcpy(saveType, SaveType, STRSIZE);
            halfOnSuccess = HalfOnSucc;
        }

        /*Calculates the current save DC of the DamageSave*/
        short SaveDC(short attBonus, short profBonus) {
            return attBonus+profBonus;
        }

        /*Displays the attributes of an Action object via printing to
        stdout*/
        void PrintAtt() {
            PrintBase();
            cout << "\n\tDamage: " << damage;
            cout << "\n\tDamage type: " << dmgType;
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
        char saveType[STRSIZE];

    public:
        void Init(char* Name, short Att, short Range, char* Condition,\
                  short Duration, char* SaveType) {
            InitBase(Name, "ConditionSave\0", Range, Att);

            memcpy(condition,Condition, STRSIZE);
            duration = Duration;

            memcpy(saveType, SaveType, STRSIZE);
        }

        /*Calculates the current save DC of the DamageSave*/
        short SaveDC(short attBonus, short profBonus) {
            return attBonus+profBonus;
        }

        /*Displays the attributes of an Action object via printing to
        stdout*/
        void PrintAtt() {
            PrintBase();
            cout << "\n\tCondition: " << condition;
            cout << "\n\tDuration: " << duration;
            cout << "\n\tSave Type: " << saveType;
        }
};



/*Action that heals a target character a certain amount*/
class HealBuff : public Action {
    protected:
        short healing;

    public:
        void Init(char* Name, short Att, short Range, short Healing) {
            InitBase(Name,"HealBuff\0",Range, Att);

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

        void Init(char* Name, short Att, short Range, short Healing) {
            InitBase(Name,"SelfHealBuff\0",Range, Att);

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

        void Init(char* Name, short Att, short Range, char* Effect, short Duration) {
            InitBase(Name, "ConditionBuff\0", Range, Att);

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
        void Init(char* Name, short Att, short Range, char* Effect, short Duration) {
            InitBase(Name,"SelfCondBuff\0",Range, Att);

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


/*Action that represents Polymorph. Due to the very large number of beasts
in D&D, each instance of this Polymorph class represents one possible beast
that someone could be transformed into.*/
class Polymorph : public Action {
    protected:
        short nActions;
        Action** actions;
    
    public:
        void Init(Action** Actions, short NActions, char* BeastName, short att[NATT]) {
            InitBase(BeastName,"Polymorph\0",60,WIS);
            nActions = NActions;
            actions = new Action*[nActions];
        }
};

/*The action bundle is a list of simple actions.
The action bundle is useful for creating complex actions that do
more than one thing to a character or characters*/
class ActionBundle {
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
                cout << "action type [" << i << "]: " << actions[i]->GetType();
            }
        }
};