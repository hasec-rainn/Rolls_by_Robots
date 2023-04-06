#attribute related constants
NATT = 6 #number of attributes
STR = 0
DEX = 1
CON = 2
INT = 3
WIS = 4
CHA = 5

#Range related constants
SELF = 0
TOUCH = 5

#damage type related constants
NDMGTYPE = 13
ACID = 0 #Acid damage
BLDG = 1 #Blugeoning damage
COLD = 2 #Cold damage
FIRE = 3 #Fire damage
FORC = 4 #Force damage
LITN = 5 #Lightning damage
NECR = 6 #Necrotic damage
PIRC = 7 #Piercing damage
POSN = 8 #Poison damage
PSYC = 9 #Pyshcic damage
RADI = 10 #Radiant damage
SLSH = 11 #Slashing damage
THDR = 12 #Thunder damage

#effect and condition related constants
NEFFECT = 21
BLIND = 0
CHARMED = 1
DEAFENED = 2
EX1 = 3 #Exhausted 1-6
EX2 = 4
EX3 = 5
EX4 = 6
EX5 = 7
EX6 = 8
FRIGHTENED = 9
GRAPPLED = 10
INCAPACITATED = 11
INVINCIBLE = 12
INVISIBLE = 13
PARALYZED = 14
PETRIFIED = 15
POISONED = 16
PRONE = 17
RESTRAINED = 18
STUNNED = 19
UNCONSCIOUS = 20

#action based constants
NACTIONS = 9
UNDEF = -1
MELEEATK = 1
RANGEDATK = 2
DAMAGESAVE = 3
CONDITIONSAVE = 4
HEAL = 5
CONDITIONBUFF = 6
POLYMORPH = 7
COMPLEX = 8
# stands for "Empty Action Set" 
EAS = {"pos": [], "neg": []}

#damage modifier constants
NDMGMOD = 4
IMMUNE = -99 #immune to damage source
RESIST = -1 #resistant to damage source
NORM = 0 
VULN = 1
MAXDMGMODS = 5 #max number of items that can modify a DmgMod's base value

#misc constants
STRSIZE = 16 #how many char in string
INF = -1
MAXMODS = 20 #max number of items that can modify base value

EMPTY = -1

#pseudo-dictionaries used for converting the constants above
#into strings for printing

att_dict = {STR:"Strength", DEX:"Dexterity", CON:"Constitution",\
INT:"Intelligence", WIS:"Wisedom", CHA:"Charisma"}

effect_dict = {BLIND:"Blinded", CHARMED:"Charmed", DEAFENED:"Deafened",\
            EX1:"Exhaustion I", EX2:"Exhaustion II",  EX3:"Exhaustion III", EX4:"Exhaustion IV",\
            EX5:"Exhaustion V", EX6:"Exhaustion VI", FRIGHTENED:"Frightened", GRAPPLED:"Grappled",\
            INCAPACITATED:"Incapacitated", INVINCIBLE:"Invincible", INVISIBLE:"Invisible", PARALYZED:"Paralyzed", PETRIFIED:"Petrified",\
            POISONED:"Poisoned", PRONE:"Prone", RESTRAINED:"Restrained", STUNNED:"Stunned",\
            UNCONSCIOUS:"Unconscious"}

action_dict = {MELEEATK:"MeleeAtk", RANGEDATK:"RangedAtk",\
                HEAL:"Heal", CONDITIONBUFF:"ConditionBuff",\
                CONDITIONSAVE:"ConditionSave", DAMAGESAVE:"DamageSave"}

# const char dmgTypeDict[NDMGTYPE][STRSIZE] =\
#             {"Acid", "Bludgeoning", "Cold", "Fire",\
#             "Force", "Lightning", "Necrotic", "Piercing",\
#             "Poison", "Psychic", "Radiant", "Slashing",\
#             "Thunder"};

# const char dmgModDict[NDMGMOD][STRSIZE] = {"Immune","Normal", "Vulnerable","Resistant"};