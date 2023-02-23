from actions import *

/********************************************************************
 * Class: Character
 * Desc: Character contains all the relevant information regarding a
 *       player character or NPC.
 * 
 * Ideology: 
********************************************************************/
class Character:
    
    def __init__(self, name, max_hp, hp, ac, speed, prof_bonus):
        self.name = name
        self.max_hp = max_hp 
        self.hp = hp #hp is ModObj to represent temp hp
        self.ac = ac  #assume armor is static: system cannot represent taking cover
        self.speed = speed   #speed boosts & reductions are representable
        self.prof_bonus = prof_bonus

    attributes =;

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
    Effects effects;

    short nAct; Action** actions; 
    #an array of nAct-many Action*
    /*create three total action arrays: one for actions that can only
    be used on the character that holds them, one for actions that should
    only be used on allies, and one that should only be used on enemies*/

    public:

        Character(char* Name, short MaxHP, short HP, short AC, short Speed,\
                DmgMod DmgMods, CharacterAttributes CA, Effects EFF,\
                Action** Actions, short NAct)
        {
            name = Name; #copy by reference since name will never change
            maxHP = MaxHP; hp.Init(HP);
            ac = AC;
            speed.Init(Speed);
            #copy in str, dex, con, ... into respective attribute slots
            attributes = CA;
            #copy in DmgMods array, if one was provided
            damageMods = DmgMods;
            #copy in any active effects on the character
            effects = EFF;
            #copy in actions that character can take (and # of actions)
            nAct = NAct; actions = Actions; #copy by reference
        }

        #Return methods
        short CurrentHP() {return hp.GetValue();}
        short CurrentSpeed() {return speed.GetValue();}
        short ProfBonus() {return profBonus;}
        bool* ActiveEffects() { return effects.GetActive(); }
        void* GetAction(short actionID) { return actions[actionID]; }
        CharacterAttributes* Attributes() {return (&attributes);}

        /*Print everything you'd ever want to know about the character*/
        void PrintAll() {
            cout << "\n###### " << name << " Info ######";
            cout << "\n\tMax HP: " << maxHP;
            cout << "\n\tCurrent HP: " << hp.GetValue();
            cout << "\n\tAC: " << ac;
            cout << "\n\tSpeed: " << speed.GetValue();

            cout << "\n\tDamage Modifier Array: ";
            for(int i=0; i<NDMGTYPE; i++) {
                cout << "\n\t\tDmgType[" << dmgTypeDict[i] << "]: " << damageMods[i];
                cout << " (" << dmgModDict[damageMods[i]] << ")";
            }

            cout << "\n\tActive effects:";
            short nActiveEffects = 0;
            for(short i=0; i<NEFFECT; i++) {
                if(effects[i] == true) {
                    nActiveEffects++;
                    cout << "\n\t\t" << statusDict[i] << ": " << effects[i]; 
                }
            }
            if(nActiveEffects < 1) {cout << "\n\t\t" << "No active effects"; }

            cout << "\n\tAttribute scores:";
            for(short att=0; att<NATT; att++) {
                cout << "\n\t\t" << attDict[att] << ": " << attributes[att]->GetScore();
            }

            cout << "\n\tActions:";
            for(short i=0; i<nAct; i++) {
                cout << "\n\t\tAction[" << i << "]: " << actions[i]->GetName();
            }
        }

        
        /***********************************************************
         * Function: ReceiveAction(Character* sender, short sentAction)
         * 
         * Parameters: Character*, short
         * 
         * Desc: Applies the action at index "action" held owned by the
         *  Character "sender" to the character whom called this method.
         * 
         * Ex: A bard is attacked by a goblin's knife atk (action at index 0)
         *     bard.ReceiveAction(&goblin, 0);
        ***********************************************************/
        void ReceiveAction(Character* sender, short action) {

            if(sender->actions[action]->ID() == POLYMORPH) {
                #do something else
            } else { #its another type of action, we can handle it.
                typedef void(*ActionFuncPtr)();
            }

            
        }

        /*Looks at all the effects afflicting the attacker and the
        victim, then determines if the attacker has disadvantage,
        advantage, or just normal hit chance.
        Returns 1 if attacker has advantage, 0 if normal, or -1 if disadv*/
        short AttackerAdv(bool* victimEffects, bool* attackerEffects) {
            short disadvSum = 
              attackerEffects[BLIND] 
            + attackerEffects[EX3]
            + attackerEffects[FRIGHTENED]
            + attackerEffects[POISONED]
            + attackerEffects[PRONE]
            + attackerEffects[RESTRAINED]
            + victimEffects[INVISIBLE];

            short advSum =
            victimEffects[BLIND] 
            + victimEffects[EX3]
            + victimEffects[FRIGHTENED]
            + victimEffects[POISONED]
            + victimEffects[PRONE]
            + victimEffects[RESTRAINED];

            if(advSum>disadvSum) {
                return 1;
            } else if (disadvSum>advSum) {
                return -1;
            } else {
                return 0;
            }
        }


        /***********************************************************
         * Function: ReceiveAction(MeleeAtk*, Attribute*, 
         *           bool*, short profBonus
         * 
         * Note: the bool* should be created from the character method
         * "GetActiveEffects"
         * 
         * Desc: Takes in another character's attributes, activeEffects,
         * and one of their actions. Then, calculates what would happen to 
         * this character (the character whom is calling this method) 
         * based off that information. 
        ***********************************************************/
        void ReceiveMelee(Character* sender, short action) {
            #Assume a melee atk can't hit a flying creature if the
            #attacker isn't flying as well
            if(effects[FLYING] && !sender->ActiveEffects()[FLYING]) {
                return; }

            # 1 if attacker has adv, 0 if normal, -1 if disadv
            short result = AttackerAdv(effects.GetActive(), sender->ActiveEffects());

            #Calculate hitChance
            MeleeAtk* ma = sender->GetAction(action);
            float hitChance;
            short toHitBonus = (ma->IsProf() * profBonus) + attributes[ma->GetAtt()]->GetMod();
            if(result==-1) { #attacker is rolling with disadv
                hitChance = ((21 + toHitBonus - ac)^2) / 400;
            } else if (result==0) { #attacker rolls normally
                hitChance = (21 + toHitBonus) / 20;
            } else { #attack is rolling with advantage
                hitChance = 1 - ((21 + toHitBonus - ac)^2) / 400;
            }

            #calculate final damage taken
            float damageTaken;
            if(damageMods[ma->GetDmgType()] == RESIST ) {
                damageTaken = (hitChance * ma->GetDamage());
            } else { #creature is immune, vuln, or takes normal dmg
                damageTaken =
                (hitChance * ma->GetDamage())
                * damageMods[ma->GetDmgType()];
            }

            hp.SubHP(damageTaken);
        }

        /***********************************************************
         * Function: ReceiveAction(MeleeAtk*, Attribute*, 
         *           bool*, short profBonus
         * 
         * Note: the bool* should be created from the character method
         * "GetActiveEffects"
         * 
         * Desc: Takes in another character's attributes, activeEffects,
         * and one of their actions. Then, calculates what would happen to 
         * this character (the character whom is calling this method) 
         * based off that information. 
        ***********************************************************/
        void ReceiveAction(RangedAtk* ra, CharacterAttributes attributes,\
        bool* attackerEffects, short ProfBonus) {

            # 1 if attacker has adv, 0 if normal, -1 if disadv
            short result = AttackerAdv(effects.GetActive(), attackerEffects);

            #Calculate hitChance
            float hitChance;
            short toHitBonus = (ra->IsProf() * profBonus) + attributes[ra->GetAtt()]->GetMod();
            if(result==-1) { #attacker is rolling with disadv
                hitChance = ((21 + toHitBonus - ac)^2) / 400;
            } else if (result==0) { #attacker rolls normally
                hitChance = (21 + toHitBonus) / 20;
            } else { #attack is rolling with advantage
                hitChance = 1 - ((21 + toHitBonus - ac)^2) / 400;
            }

            #calculate final damage taken
            short damageTaken;
            if(damageMods[ra->GetDmgType()] == RESIST ) {
                damageTaken = (hitChance * ra->GetDamage());
            } else { #creature is immune, vuln, or takes normal dmg
                damageTaken =
                (hitChance * ra->GetDamage())
                * damageMods[ra->GetDmgType()];
            }

            hp.SubHP(damageTaken);
        }

        /*
        Attacked.ReceiveAction(Attacker.GetAction(0), Attacker.GetAtt(), Attack.GetEffects() )
        */
