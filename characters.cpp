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
        ModObj maxHP; HP hp; //hp is ModObj to represent temp hp
        short ac;   //assume armor is static: system cannot represent taking cover
        ModObj speed;   //speed boosts & reductions are representable
        short profBonus;

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

        /*Each index in "effects" corresponds to a specific status effect
        (see the char[][] status at top of file.)
        True (1) means that the particular effect is active, false means
        the particular effect is not active.*/
        bool effects[NEFFECT];
        bool effectImmunities[NEFFECT]; //1 for vulnurable, 0 for immune (for bitwise multiplication)
        short effectDurations[NEFFECT];

        Attribute attributes[NATT]; //str, dex, con, int, wis, cha

        short nAct; Action** actions; //an array of nAct-many Action*
        /*create three total action arrays: one for actions that can only
        be used on the character that holds them, one for actions that should
        only be used on allies, and one that should only be used on enemies*/

    public:

        Character(char* Name, short MaxHP, short HP, short AC, short Speed,\
                  DmgMod DmgMods, Attribute* Attributes, bool* EffectImmunities,
                  bool* Effects, Action** Actions, short NAct)
        {
            name = Name; //copy by reference since name will never change
            maxHP.Init(MaxHP); hp.Init(HP);
            ac = AC;
            speed.Init(Speed);
            
            //copy in str, dex, con, ... into respective attribute slots
            for(short att=0; att<NATT; att++) {
                attributes[att] = Attributes[att];}

            //copy in any active effects on the character
            for(int i=0; i<NEFFECT; i++) {
                effects[i] = Effects[i];}

            nAct = NAct; actions = Actions;

        }

        /*Print everything you'd ever want to know about the character*/
        void PrintAll() {
            cout << "\n###### " << name << " Info ######";
            cout << "\n\tMax HP: " << maxHP.GetValue();
            cout << "\n\tCurrent HP: " << hp.GetValue();
            cout << "\n\tAC: " << ac;
            cout << "\n\tSpeed: " << speed.GetValue();
            cout << "\n\tDamage Modifier Array: ";
            for(int i=0; i<NDMGTYPE; i++) {
                cout << "\n\t\tDmgType[" << dmgTypeDict[i] << ", mod: " << damageMods[i];
            }
            cout << "\n\tActive effects:";
            for(int i=0; i<NEFFECT; i++) {
                cout << "\n\t\t" << statusDict[i] << ": " << effects[i];
            }
            cout << "\n\tAttribute scores:";
            for(short att=0; att<NATT; att++) {
                cout << "\n\t\t" << attDict[att] << ": " << attributes[att].GetScore();
            }
            cout << "\n\tActions:";
            for(int i=0; i<nAct; i++) {
                cout << "\n\t\tAction[" << i << "]: " << actions[i]->GetName();
            }
        }

        short GetHP() {return hp.GetValue();}
        short GetSpeed() {return speed.GetValue();}
        /*Used by the AI to retrieve a particular action from a character*/
        Action* GetAction(short actionID) { return actions[actionID]; }
        bool* GetActiveEffects() {
            /* Should only be affected by an effect that you have AND that
            you are NOT immune to*/
            bool activeEffects[NEFFECT];
            for(short i=0; i<NEFFECT; i++) {
                activeEffects[i] = effects[i] * effectImmunities[i]; }
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

            //Assume a meleeAtk can't hit a flying creature if the
            //attacker can't fly as well
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

            }

            //calculate final damage taken
            if(damageMods[ma->GetDmgType()] == -2 ) {
                float damageTaken = (hitChance * ma->GetDamage());
            } else { //creature is immune, vuln, or takes normal dmg
                float damageTaken =
                (hitChance * ma->GetDamage())
                * damageMods[ma->GetDmgType()];
            }

            return;
        }

        /*
        Attacked.ReceiveAction(Attacker.GetAction(0), Attacker.GetAtt(), Attack.GetEffects() )
        */

};