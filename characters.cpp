#include<iostream>
#include<cstring>
#include<typeinfo>
#include<cmath>


#ifndef __MODOBJ_INCLUDED__
#define __MODOBJ_INCLUDED__
#include "modifiable_obj.cpp"
#endif

#ifndef __ACTIONS_INCLUDED__
#define __ACTIONS_INCLUDED__
#include "actions.cpp"
#endif
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
        char* name;
        short maxHP; HP hp; //hp is ModObj to represent temp hp
        short ac;   //assume armor is static: system cannot represent taking cover
        ModObj speed;   //speed boosts & reductions are representable
        short profBonus;

        CharacterAttributes attributes;

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
        //an array of nAct-many Action*
        /*create three total action arrays: one for actions that can only
        be used on the character that holds them, one for actions that should
        only be used on allies, and one that should only be used on enemies*/

    public:

        Character(char* Name, short MaxHP, short HP, short AC, short Speed,\
                DmgMod DmgMods, CharacterAttributes CA, Effects EFF,
                Action** Actions, short NAct)
        {
            name = Name; //copy by reference since name will never change
            maxHP = MaxHP; hp.Init(HP);
            ac = AC;
            speed.Init(Speed);
            //copy in str, dex, con, ... into respective attribute slots
            attributes = CA;
            //copy in DmgMods array, if one was provided
            damageMods = DmgMods;
            //copy in any active effects on the character
            effects = EFF;
            //copy in actions that character can take (and # of actions)
            nAct = NAct; actions = Actions;
        }

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

        short GetHP() {return hp.GetValue();}
        short GetSpeed() {return speed.GetValue();}
        /*Used by the AI to retrieve a particular action from a character*/
        Action* GetAction(short actionID) { return actions[actionID]; }
        bool* GetActiveEffects() {
            return effects.GetActive();
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
        void ReceiveAction(MeleeAtk* ma, Attribute* attributes,\
        bool* attackerEffects, short ProfBonus) {

            bool* victimEffects = GetActiveEffects();

            //Assume a melee atk can't hit a flying creature if the
            //attacker isn't flying as well
            if(victimEffects[FLYING] && !attackerEffects[FLYING]) {
                return; }

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

            //Calculate hitChance
            float hitChance;
            short toHitBonus = (ma->IsProf() * profBonus) + attributes[ma->GetAtt()].GetMod();
            if(disadvSum > advSum) { //attacker is rolling with disadv
                hitChance = ((21 + toHitBonus - ac)^2) / 400;
            } else if (disadvSum == advSum) { //attacker rolls normally
                hitChance = (21 + toHitBonus) / 20;
            } else { //attack is rolling with advantage
                hitChance = 1 - ((21 + toHitBonus - ac)^2) / 400;
            }

            //calculate final damage taken
            if(damageMods[ma->GetDmgType()] == RESIST ) {
                float damageTaken = (hitChance * ma->GetDamage());
            } else { //creature is immune, vuln, or takes normal dmg
                float damageTaken =
                (hitChance * ma->GetDamage())
                * damageMods[ma->GetDmgType()];
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
        void ReceiveAction(RangedAtk* ra, Attribute* attributes,\
        bool* attackerEffects, short ProfBonus) {

            bool* victimEffects = GetActiveEffects();

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

            //Calculate hitChance
            float hitChance;
            short toHitBonus = (ra->IsProf() * profBonus) + attributes[ra->GetAtt()].GetMod();
            if(disadvSum > advSum) { //attacker is rolling with disadv
                hitChance = ((21 + toHitBonus - ac)^2) / 400;
            } else if (disadvSum == advSum) { //attacker rolls normally
                hitChance = (21 + toHitBonus) / 20;
            } else { //attack is rolling with advantage
                hitChance = 1 - ((21 + toHitBonus - ac)^2) / 400;
            }

            //calculate final damage taken
            short damageTaken;
            if(damageMods[ra->GetDmgType()] == RESIST ) {
                damageTaken = (hitChance * ra->GetDamage());
            } else { //creature is immune, vuln, or takes normal dmg
                damageTaken =
                (hitChance * ra->GetDamage())
                * damageMods[ra->GetDmgType()];
            }

            hp.SubHP(damageTaken);
        }

        /*
        Attacked.ReceiveAction(Attacker.GetAction(0), Attacker.GetAtt(), Attack.GetEffects() )
        */

};