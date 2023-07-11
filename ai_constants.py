import numpy as np

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
NEFFECT = 28
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
FLY = 21

GENERAL_ADV = 22
MELEE_ADV = 23
RANGEDADV = 24
GENERAL_DISADV = 25
MELEE_DISADV = 26
RANGED_DISADV = 27

# a vector that marks attacker.effects that give an attacker advantage 
# (on a melee attack) as 1, and then marks every other effect as 0
ATTACKER_ADV_MELEE_MASK = np.zeros(NEFFECT)
ATTACKER_ADV_MELEE_MASK[[GENERAL_ADV, MELEE_ADV]] = 1

# a vector that marks attacker.effects that give an attacker disadv 
# (on a melee attack) as 1, and then marks every other effect as 0
ATTACKER_DISADV_MELEE_MASK = np.zeros(NEFFECT)
ATTACKER_DISADV_MELEE_MASK[[GENERAL_DISADV, MELEE_DISADV, BLIND,
                   EX3, EX4, EX5, 
                   POISONED, PRONE, RESTRAINED]] = 1

# a vector that marks receiver.effects that give the attacker advantage
# (on a melee attack) as 1, and then marks every other effect as 0
RECEIVER_ADV_MELEE_MASK = np.zeros(NEFFECT)
RECEIVER_ADV_MELEE_MASK[[STUNNED, RESTRAINED, BLIND, 
                         PARALYZED, PETRIFIED, PRONE, UNCONSCIOUS]] = 1

# a vector that marks receiver.effects that give the attacker disadvantage
# (on a melee attack) as 1, and then marks every other effect as 0
RECEIVER_DISADV_MELEE_MASK = np.zeros(NEFFECT)
RECEIVER_DISADV_MELEE_MASK[[INVISIBLE]] = 1

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
EAS = {"pos": [], "neg": []}
"""
Empty Action Set: Contains no "pos" or "neg" actions
"""

#damage modifier constants
NDMGMOD = 4
IMMUNE = -99 #immune to damage source
RESIST = -1 #resistant to damage source
NORM = 0 
VULN = 1
MAXDMGMODS = 5 #max number of items that can modify a DmgMod's base value
dmgmod_dict = {IMMUNE:-99, RESIST:0.5, NORM:1, VULN: 2} #used to multiply damage by the corresponding modifier

#Dice related constants
DICEQTY = 0
DICETYPE = 1

# Advantage / Disadvantage related constants
DISADV = -1
ADV = 1

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