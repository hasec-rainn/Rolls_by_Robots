
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
        short id = UNDEF;
        char* name; //make sure its \0 terminated char*
        short att; //what stat (STR, DEX, ect) is associated with performing this action?
        short range;

    protected:

        void InitBase(char* Name, short Range, short Att) {
            name = Name;
            att = Att; 
            range = Range;
        }

        /*Displays the basic attributes of an Action object via printing to
        stdout*/
        void PrintBase() {
            cout << "\n###### " << name << " Attributes ######";
            cout << "\n\tAssociated attribute: " << attDict[att];
            cout << "\n\tRange: " << range;
            cout << "\n";
        }

    public:
        /*Returns the range of the Action, in feet*/
        short GetRange() { return range; }
        short GetAtt() { return att; }
        char* GetName() { return name; }
        short ID() {return id;}

        virtual void PrintAtt() {
            cout << "DEFAULT PRINTATT";
            return;
        }
};

class MeleeAtk : public Action {
    protected:
        short damage;
        short dmgType;
        bool useProf;

    public:

        MeleeAtk(char* Name, short Att, bool UseProf, short Range,\
                  short Dmg, short DmgT)\
        {
            InitBase(Name, Range, Att);
            id = MELEE;
            damage = Dmg;
            useProf = UseProf;
            dmgType = DmgT;
        }

        /*Returns true if a character uses proficiency bonus for this atk*/
        bool IsProf() { return useProf; }
        short GetDamage() {return damage;}
        short GetDmgType() {return dmgType;}

        /*Displays the attributes of an Action object via printing to
        stdout*/
        void PrintAtt() {
            PrintBase();
            cout << "\n\tDamage: " << damage;
            cout << "\n\tDamage type: " << dmgTypeDict[dmgType];
            cout << "\n\tUses proficiency? " << useProf;
        }

        /*Performs copy by value of two MeleeAtks*/
        void operator=(MeleeAtk atk) {
            //only name is copied by reference (not value) since it never changes
            name = atk.name;
            att = atk.att;
            range = atk.range;

            damage = atk.damage;
            useProf = atk.useProf;
            dmgType = atk.dmgType;

        }
};



class RangedAtk : public Action {
    protected:
        short damage;
        short dmgType;
        bool useProf;

    public:
        RangedAtk(char* Name, short Att, bool UseProf, short Range,\
                  short Dmg, short DmgT)\
        {
            InitBase(Name,Range, Att);

            id = RANGED;
            useProf = UseProf;
            damage = Dmg;
            dmgType = DmgT;
        }

        /*Returns true if a character uses proficiency bonus for this atk*/
        bool IsProf() { return useProf; }
        short GetDamage() {return damage;}
        short GetDmgType() {return dmgType;}

        /*Displays the attributes of an Action object via printing to
        stdout*/
        void PrintAtt() {
            PrintBase();
            cout << "\n\tDamage: " << damage;
            cout << "\n\tDamage type: " << dmgTypeDict[dmgType];
            cout << "\n\tUses proficiency? " << useProf;
        }

        /*Performs copy by value of two RangedAtks*/
        void operator=(RangedAtk atk) {
            //only name is copied by reference since it never changes
            name = atk.name;
            att = atk.att;
            range = atk.range;

            damage = atk.damage;
            useProf = atk.useProf;
            dmgType = atk.dmgType;
        }
};



/*Action that requires someone to make a saving throw. 
If they fail, they take damage.*/
class DamageSave : public Action {
    protected:
        short damage;
        short dmgType;
        short saveType; //what type of save (STR,DEX,etc) will recipient make?
        bool halfOnSuccess;     //even if someone succeeds, still take 1/2 dmg

    public:
        DamageSave(char* Name, short Att, short Range, short Dmg, short DmgT,\
                  short SaveType, bool HalfOnSucc)
        {
            InitBase(Name,Range,Att);

            id = DMGSAVE;
            damage = Dmg;
            dmgType = DmgT;
            saveType = SaveType;
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
            cout << "\n\tDamage type: " << dmgTypeDict[dmgType];
            cout << "\n\tSave Type: " << attDict[saveType];
            cout << "\n\tHalf DMG on success? " << halfOnSuccess;
        }
};


/*Action that requires someone to make a saving throw. 
If they fail, they are subjected to a negative condition.*/
class ConditionSave : public Action {
    protected:
        short condition;
        short duration; //in rounds
        short saveType; //what type of save (STR,DEX,etc) will recipient make?

    public:
        ConditionSave(char* Name, short Att, short Range, short Condition,\
                  short Duration, short SaveType) {
            InitBase(Name, Range, Att);

            id = CONDITIONSAVE;
            condition = Condition;
            duration = Duration;

            saveType = SaveType;
        }

        /*Calculates the current save DC of the DamageSave*/
        short SaveDC(short attBonus, short profBonus) {
            return attBonus+profBonus;
        }

        /*Displays the attributes of an Action object via printing to
        stdout*/
        void PrintAtt() {
            PrintBase();
            cout << "\n\tCondition: " << statusDict[condition];
            cout << "\n\tDuration: " << duration;
            cout << "\n\tSave Type: " << attDict[saveType];
        }
};



/*Action that heals a target character a certain amount*/
class HealBuff : public Action {
    protected:
        short healing;

    public:
        HealBuff(char* Name, short Att, short Range, short Healing) {
            InitBase(Name, Range, Att);

            id = HEAL;
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

        SelfHealBuff(char* Name, short Att, short Healing) {
            InitBase(Name, 0, Att);

            id = SELFHEAL;
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
        short effect;
        short duration;

    public:

        ConditionBuff(char* Name, short Att, short Range, short Effect, short Duration) {
            InitBase(Name, Range, Att);

            id = CONDITIONBUFF;
            effect = Effect;
            duration = Duration;
        }

        /*Displays the attributes of an Action object via printing to
        stdout*/
        void PrintAtt() {
            PrintBase();
            cout << "\n\tCondition: " << statusDict[effect];
            cout << "\n\tDuration: " << duration;
        }
};



/*Action that gives a positive condition to the character that has
this buff. CANNOT BE USED ON OTHER CHARACTERS*/
class SelfCondBuff : public Action {
    protected:
        short effect;
        short duration;

    public:
        SelfCondBuff(char* Name, short Att, short Effect, short Duration) {
            InitBase(Name,0, Att);

            id = SELFCONDITIONBUFF;
            effect = Effect;
            duration = Duration;
        }

        /*Displays the attributes of an Action object via printing to
        stdout*/
        void PrintAtt() {
            PrintBase();
            cout << "\n\tCondition: " << statusDict[effect];
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
        Polymorph(Action** Actions, short NActions, char* BeastName, short att[NATT]) {
            InitBase(BeastName, 60, WIS);
            
            id = POLYMORPH;
            nActions = NActions;
            actions = new Action*[nActions];
        }
};

/*ComplexAction is a list of simple actions.
It is useful for creating complex actions that do
more than one thing to a character or characters*/
class ComplexAction : public Action {
    protected:
        short nActions;
        Action** actions;
    public:
        ComplexAction(Action** Actions, short NActions) {
            id = COMPLEX;
            nActions = NActions;
            actions = new Action*[nActions];
        }

        void PrintAtt() {
            for(int i=0; i<nActions; i++) {
                cout << "action type [" << i << "]: " << actions[i]->GetName();
            }
        }
};