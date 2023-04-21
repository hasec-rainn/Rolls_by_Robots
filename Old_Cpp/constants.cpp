//attribute related constants
#define NATT 6 //number of attributes
#define STR 0
#define DEX 1
#define CON 2
#define INT 3
#define WIS 4
#define CHA 5

//damage type related constants
#define NDMGTYPE 13
#define ACID 0 //Acid damage
#define BLDG 1 //Blugeoning damage
#define COLD 2 //Cold damage
#define FIRE 3 //Fire damage
#define FORC 4 //Force damage
#define LITN 5 //Lightning damage
#define NECR 6 //Necrotic damage
#define PIRC 7 //Piercing damage
#define POSN 8 //Poison damage
#define PSYC 9 //Pyshcic damage
#define RADI 10 //Radiant damage
#define SLSH 11 //Slashing damage
#define THDR 12 //Thunder damage

//effect and condition related constants
#define NEFFECT 22
#define BLIND 0
#define CHARMED 1
#define DEAFENED 2
#define EX1 3 //Exhausted 1-6
#define EX2 4
#define EX3 5
#define EX4 6
#define EX5 7
#define EX6 8
#define FLYING 9
#define FRIGHTENED 10
#define GRAPPLED 11
#define INCAPACITATED 12
#define INVINCIBLE 13
#define INVISIBLE 14
#define PARALYZED 15
#define PETRIFIED 16
#define POISONED 17
#define PRONE 18
#define RESTRAINED 19
#define STUNNED 20
#define UNCONSCIOUS 21

//action type based constants
#define NACTIONS 11
#define UNDEF -1
#define MELEE 1
#define RANGED 2
#define DMGSAVE 3
#define CONDITIONSAVE 4
#define HEAL 5
#define SELFHEAL 6
#define CONDITIONBUFF 7
#define SELFCONDITIONBUFF 8
#define POLYMORPH 9
#define COMPLEX 10

//damage modifier constants
#define NDMGMOD 4
#define IMMUNE 0 //immune to damage source
#define RESIST 3 //resistant to damage source
#define NORM 1
#define VULN 2

//misc constants
#define STRSIZE 16 //how many char in string
#define INF -1
#define MAXMODS 20 //max number of elements that can modifer base value

//pseudo-dictionaries used for converting the constants above
//into strings for printing

const char attDict[NATT][STRSIZE] =\
    {"Strength\0","Dexterity\0", "Constitution\0",\
    "Intelligence\0", "Wisedom\0", "Charisma\0"};

const char statusDict[NEFFECT][STRSIZE] =\
                {"Blinded\0", "Charmed\0", "Deafened\0",\
                "Exhaustion I\0", "Exhaustion II\0",  "Exhaustion III\0", "Exhaustion IV\0",\
                "Exhaustion V\0", "Exhaustion VI\0","Flying\0","Frightened\0", "Grappled\0",\
                "Incapacitated\0", "Invincible\0", "Invisible\0", "Paralyzed\0", "Petrified\0",\
                "Poisoned\0", "Prone\0", "Restrained\0", "Stunned\0",\
                "Unconscious\0"};

const char actionDict[][STRSIZE] = {"MeleeAtk\0", "SpellAtk\0", "RangedAtk\0",\
                    "HealBuff\0", "SelfHealBuff\0", "ConditionBuff\0",\
                    "SelfCondBuff\0","ConditionSave\0",\
                    "DamageSave\0","DamageAOE\0", "ConditionAOE\0"};

const char dmgTypeDict[NDMGTYPE][STRSIZE] =\
                {"Acid\0", "Bludgeoning\0", "Cold\0", "Fire\0",\
                "Force\0", "Lightning\0", "Necrotic\0", "Piercing\0",\
                "Poison\0", "Psychic\0", "Radiant\0", "Slashing\0",\
                "Thunder\0"};

const char dmgModDict[NDMGMOD][STRSIZE] = {"Immune","Normal", "Vulnerable","Resistant"};