#include<iostream>
#include<cstring>
#include<typeinfo>

using namespace std;

#define STRSIZE 16
#define INF -1

#define NDMGTYPE 13

// https://rpg.stackexchange.com/questions/70335/how-do-i-calculate-the-chance-to-hit-a-given-ac?newreg=7e3de3c84d9a42ba96b932f394793d7f


char status[21][STRSIZE] =\
                {"None\0", "Blinded\0", "Charmed\0", "Deafened\0",\
                "Exhaustion I\0", "Exhaustion II\0",  "Exhaustion III\0", "Exhaustion IV\0",\
                "Exhaustion V\0", "Exhaustion VI\0","Frightened\0", "Grappled\0",\
                "Incapacitated\0", "Invisible\0", "Paralyzed\0", "Petrified\0",\
                "Poisoned\0", "Prone\0", "Restrained\0", "Stunned\0",\
                "Unconscious\0"};

char aType[4][STRSIZE] = {"MeleeAtk\0", "SpellAtk\0", "RangedAtk\0", "Buff\0"};

char dmgType[NDMGTYPE][STRSIZE] =\
                {"Acid\0", "Bludgeoning\0", "Cold\0", "Fire\0",\
                "Force\0", "Lightning\0", "Necrotic\0", "Piercing\0",\
                "Poison\0", "Psychic\0", "Radiant\0", "Slashing\0",\
                "Thunder\0"};

short GetSType(char* item) {

    short index;
    for(index=0; index<21; index++) {
        if (strcmp(status[index], item) == 0) {
            return index;
        }
    }

    return -1;
}

short GetAType(char* item) {

    short index;
    for(index=0; index<3; index++) {
        if (strcmp(aType[index], item) == 0) {
            return index;
        }
    }

    return -1;
}

short GetDMGType(char* item) {

    short index;
    for(index=0; index<13; index++) {
        if (strcmp(dmgType[index], item) == 0) {
            return index;
        }
    }

    return -1;
}


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
        short maxHP; short hp;
        short ac;
        short speed;
        //proficiency bonus is not included since it is included in actions

        /*complicated, is it not? The dmgModArr is an array which details
        how the character is afflicted by a certain damage type. Each index
        corresponds to to the corresponding damage type in the "dmgType"
        array.
        The value contained at a particular index describes how the character
        is impacted. Below are the possible values that may show up:
        0 -> character takes no damage (has immunity to damage source)
        -2 -> character takes half damage (has resistance to dmg source)
        1 -> character takes normal damage
        2 -> character takes double damage (has vulnerability to dmg source)*/
        short dmgModArr[NDMGTYPE];

        char effects[21][STRSIZE];
        short effectDurations[21];

        short strScore; short strMod;
        short dexScore; short dexMod;
        short conScore; short conMod;
        short intScore; short intMod;
        short wisScore; short wisMod;
        short chaScore; short chaMod;


        short nAct; Action** actions; //an array of nAct-many Action*

    public:

        Character(short MaxHP, short HP, short AC, short Speed,\
                  short* DmgModArr, short StrScore, short StrMod,\
                  short DexScore, short DexMod,short ConScore,\
                  short ConMod, short IntScore, short IntMod,\
                  short WisScore, short WisMod,\
                  short ChaScore, short ChaMod,\
                  short NAct, Action** Actions)
        {
            maxHP = MaxHP; hp = HP;
            ac = AC;
            speed = Speed;
            for(int i=0; i<NDMGTYPE; i++) {
                dmgModArr[i] = DmgModArr[i];
            }

            strScore = StrScore; strMod = StrMod;
            dexScore = DexScore; dexMod = dexMod;
            conScore = ConScore; conMod = ConMod;
            intScore = IntScore; intMod = IntMod;
            wisScore = WisScore; wisMod = WisMod;
            chaScore = ChaScore; chaMod = ChaMod;

            nAct = NAct; actions = Actions;
        }

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
            cout << "\n\tSTR score: " << strScore << " (Mod: " << strMod << ")";
            cout << "\n\tDEX score: " << dexScore << " (Mod: " << dexMod << ")";
            cout << "\n\tCON score: " << conScore << " (Mod: " << conMod << ")";
            cout << "\n\tINT score: " << intScore << " (Mod: " << intMod << ")";
            cout << "\n\tWIS score: " << wisScore << " (Mod: " << wisMod << ")";
            cout << "\n\tCHA score: " << chaScore << " (Mod: " << chaMod << ")";
            for(int i=0; i<nAct; i++) {
                cout << "\n\t\tAction[" << i << "] type: " << actions[i]->type;
            }



        }

        short GetHP() {return hp;}
        short GetSpeed() {return speed;}

        /***********************************************************
         * Function: ApplyAction
         * Parameters: Action* a
         * 
         * Desc: Applies Action at index "a" to this character. 
         *       If the action is an attack, the character may lose 
         *       health and/or receive a negative effect.
         * 
         *       If the action is a buff/heal, the character may gain
         *       health or receive a positive effect.
         * 
         * Example1: ApplyAction(fireball) -> character loses health
         *           due to fire damage
         * Example2: ApplyAction(healing_word) -> character gains
         *           health
        ***********************************************************/
        void ApplyAction(short a) {
            if( strcmp(actions[a]->type, "MeleeAtk\0") == 0 ) {

                cout << "\nlooks like this is a melee attack";

            } else if ( strcmp(actions[a]->type, "RangedAtk\0") == 0 ) {

                cout << "\nlooks like this is a ranged attack.";

            } else if ( strcmp(actions[a]->type, "ConditionSave\0") == 0 ) {

                cout << "\nlooks like this is a condition save.";

            }
            return;
        }

};




int main() {

    MeleeAtk clubStrike; clubStrike.Init("Club Strike\0",8,5,7,"Bludgeoning\0");
    RangedAtk axeThrow; axeThrow.Init("Axe Throw\0", 8, 120, 12, "Piercing\0");
    DamageSave bearHug; bearHug.Init("Bear Hug\0",5,20,"Bludgeoning\0",14,"Dex\0",false);
    ConditionSave knockout; knockout.Init("Knockout Punch\0",5,"Incapacitated\0",2,14,"Con\0"); 
    
    short nAct = 4;
    Action* atkPtrArr[4];
    atkPtrArr[0] = &clubStrike;
    atkPtrArr[1] = &axeThrow;
    atkPtrArr[2] = &bearHug;
    atkPtrArr[3] = &knockout;


    short tDmgModArr[NDMGTYPE] = {1,1,1,1,1,1,1,1,1,1,1,1,1};

    for(int i=0; i<4; i++) {
        atkPtrArr[i]->PrintAtt();
    }

    Character thageth = {65,65,16,30,tDmgModArr,18,4,14,2,16,3,8,-1,10,1,7,-2,nAct,atkPtrArr};

    thageth.PrintAtt()

    return 1;
}