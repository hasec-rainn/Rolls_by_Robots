#include<stdio.h>
#include<stdlib.h>
using namespace std;

//actions.cpp, modifiable_obj.cpp, and constants.cpp are all included
//in characters.cpp
#include "characters.cpp"

int main() {
    //how the character receives dif types of damage
    DmgMod dmgModifiers;
    //the stats for each of the character's attributes
    CharacterAttributes attributes;
    attributes.Init(18,16,16,10,8,8);
    //Effects currently afflicting character
    Effects effects; effects.Init();
    //actions that the character can take
    short nAct = 3;
    MeleeAtk clubStrike("Club Strike\0",STR,true,5,8,BLDG);
    RangedAtk javlinThrow("Javin Throw\0", DEX, true,30,12,PIRC);
    DamageSave bearHug("Bear Hug\0",STR,5,20,BLDG,DEX,false);
    Action* atkPtrArr[3];
    atkPtrArr[0] = &clubStrike;
    atkPtrArr[1] = &javlinThrow;
    atkPtrArr[2] = &bearHug;

    //actual character object
    char name[STRSIZE] = "Thageth\0";
    Character thageth(name,58,58,16,30,dmgModifiers,attributes,effects,atkPtrArr,nAct);

    thageth.PrintAll();

    nAct = 2;
    MeleeAtk dagger("Dagger",DEX,true,5,8,SLSH);
    RangedAtk bow("Bow",DEX,true,120,12,PIRC);
    Action* goblinAtks[2];
    goblinAtks[0] = &dagger;
    goblinAtks[1] = &bow;

    CharacterAttributes goblinAtt;
    goblinAtt.Init(8,14,14,12,8,16);

    Character boblinGoblin("Boblin Goblin",16,16,14,20,dmgModifiers,goblinAtt,effects,goblinAtks,nAct);
    boblinGoblin.PrintAll();

    thageth.ReceiveAction(boblinGoblin.GetAction(0),boblinGoblin.Attributes(),\
    boblinGoblin.ActiveEffects(),boblinGoblin.ProfBonus());
    return 0;
}