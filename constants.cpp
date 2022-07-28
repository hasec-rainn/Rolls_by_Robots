#define STRSIZE 16
#define INF -1

#define NDMGTYPE 13
#define NEFFECT 23
#define NATT 6

char status[NEFFECT][STRSIZE] =\
                {"None\0", "Blinded\0", "Charmed\0", "Deafened\0",\
                "Exhaustion I\0", "Exhaustion II\0",  "Exhaustion III\0", "Exhaustion IV\0",\
                "Exhaustion V\0", "Exhaustion VI\0","Flying\0","Frightened\0", "Grappled\0",\
                "Incapacitated\0", "Invincible\0", "Invisible\0", "Paralyzed\0", "Petrified\0",\
                "Poisoned\0", "Prone\0", "Restrained\0", "Stunned\0",\
                "Unconscious\0"};

char aType[][STRSIZE] = {"MeleeAtk\0", "SpellAtk\0", "RangedAtk\0",\
                    "HealBuff\0", "SelfHealBuff\0", "ConditionBuff\0",\
                    "SelfCondBuff\0","ConditionSave\0",\
                    "DamageSave\0","DamageAOE\0", "ConditionAOE\0"};

char dmgType[NDMGTYPE][STRSIZE] =\
                {"Acid\0", "Bludgeoning\0", "Cold\0", "Fire\0",\
                "Force\0", "Lightning\0", "Necrotic\0", "Piercing\0",\
                "Poison\0", "Psychic\0", "Radiant\0", "Slashing\0",\
                "Thunder\0"};