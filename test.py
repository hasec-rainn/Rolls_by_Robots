import modifiable_objs as mo
import ai_constants as aic
import characters as chr
import actions as act
import rolls_by_robots as rbr
import character_list as char_list
import sys

desired_tests = sys.argv[1:]

if "health" in desired_tests:
    hp = mo.Health(30)
    
    #check to ensure basic functionality
    if hp.max_hp != 30:
        print("hp should have hp.max_health=30")
        raise ValueError("hp.max_health was " + str(hp.max_hp))

    #check to ensure SubHP method works with temp hp
    hp.GiveTempHP(10,30) #give 10 temp for 30 rounds
    hp.GiveTempHP(5,25) #give 5 temp for 25 rounds
    hits = [3,4,7,2,1,1]
    hp_copy = hp.ReturnCopy()
    max_hp = 45 #30 hp + 10 temp + 5 temp
    for h in hits:
        hp.SubHP(h)
        max_hp = max_hp - h
        if hp.CurrentHP() != max_hp:
            print("hp.GetValue should be", max_hp)
            raise ValueError("For hit " + str(h) + " hp.GetValue()=" + str(hp.GetValue()))

    #check to ensure copy by value works
    if hp.CurrentHP() == hp_copy.CurrentHP():
        raise ValueError("Copy by reference failed: hp and hp_copy have same values")
    
    print("Health class is functional")




if "attribute" in desired_tests:

    #check to make sure init, GetScore, and GetMod work
    dex = mo.Attribute(aic.DEX,10)
    if dex.GetScore() != 10:
        raise ValueError("error: dex score != 10")
    if dex.GetMod() != 0:
        raise ValueError("error: dex mod != 0")
    
    #Check to make sure GetMod and GetScore produce correct values
    dex.AddMod(2,1)
    if dex.GetScore() != 12:
        raise ValueError("error: dex score != 12")
    if dex.GetMod() != 1:
        raise ValueError("error: dex mod != 1")
    
    #Check to make sure GetMod and GetScore produce correct values
    dex.AddMod(3,5)
    if dex.GetScore() != 15:
        raise ValueError("error: dex score != 15")
    if dex.GetMod() != 2:
        raise ValueError("error: dex mod != 2")
    
    #Check to make sure Timestep works and produces the correct value
    dex.TimeStep()
    if dex.GetScore() != 13:
        raise ValueError("error: dex score != 13")
    if dex.GetMod() != 1:
        raise ValueError("error: dex mod != 1")
    
    #ensure ReturnCopy works by returning a deep copy 
    dex_copy = dex.ReturnCopy()
    for i in range(0,4):
        dex.TimeStep()
    if dex.GetScore() == dex_copy.GetScore():
        raise ValueError("error: dex score is equal to dex_copy score")
    if dex.GetMod() == dex_copy.GetMod():
        raise ValueError("error: dex modifier is equal to dex_copy modifier")


    
    print("Attribute class is functional")




if "dmgmod" in desired_tests:
    fire = mo.DmgMod(aic.NORM)

    # test that __init__ works
    if fire.GetValue() != aic.NORM:
        raise ValueError("error: fire damage mod is not correct value from init")

    #test that AddMod works
    fire.AddMod(aic.VULN,6)
    if fire.GetValue() != aic.VULN:
        raise ValueError("error: fire damage mod is not correct value after AddMod (1)")
    
    fire.AddMod(aic.RESIST,5)
    if fire.GetValue() != aic.NORM:
        raise ValueError("error: fire damage mod is not correct value after AddMod (2)")
    
    fire.AddMod(aic.RESIST,5)
    if fire.GetValue() != aic.RESIST:
        print(fire)
        raise ValueError("error: fire damage mod is not correct value after AddMod (3)")
    
    fire.AddMod(aic.RESIST,5)
    if fire.GetValue() != aic.RESIST:
        raise ValueError("error: fire damage mod is not correct value after AddMod (4)")
    
    fire.AddMod(aic.IMMUNE,5)
    if fire.GetValue() != aic.IMMUNE:
        raise ValueError("error: fire damage mod is not correct value after AddMod (5)")
    
    #test that TimeStep works
    for i in range(0,5):
        fire.TimeStep()
    if fire.GetValue() != aic.VULN:
        raise ValueError("error: fire damage mod is not correct value after TimeStep (1)")
    
    fire.TimeStep()
    if fire.GetValue() != aic.NORM:
        raise ValueError("error: fire damage mod is not correct value after TimeStep (2)")
    
    print("DmgMod class is functional")




if "effects" in desired_tests:

    # make sure basic init and AddEff works
    eff_obj = mo.Effects()
    eff_obj.AddEff(aic.CHARMED,3)
    eff_obj.AddEff(aic.INVISIBLE,5)
    if eff_obj.effects[aic.CHARMED] == False or eff_obj.effects[aic.INVISIBLE] == False:
        raise ValueError("error: eff_obj has incorrect value after adding effects")
    
    #make sure TimeStep works
    eff_obj_copy = eff_obj.ReturnCopy()
    for i in range(0,3):
        eff_obj.TimeStep()
    if eff_obj.effects[aic.CHARMED] == True:
        raise ValueError("error: eff_obj has incorrect value after TimeStep (1)")
    eff_obj.TimeStep()
    eff_obj.TimeStep()
    if eff_obj.effects[aic.INVISIBLE] == True:
        raise ValueError("error: eff_obj has incorrect value after TimeStep (2)")
    
    #make sure ReturnCopy returns a deep copy
    if eff_obj_copy.effects[aic.CHARMED] == False or eff_obj_copy.effects[aic.INVISIBLE] == False:
        raise ValueError("error: eff_obj has same values as eff_obj_copy")

    print("Effects class is functional")




if "character" in desired_tests:
    dmg_mods = {}
    for dm in range(0,aic.NDMGTYPE):
        dmg_mods[dm] = mo.DmgMod(aic.NORM)

    att = {}
    for a in range(0,aic.NATT):
        att[a] = mo.Attribute(a,8)

    boblins_actions = {"pos":[], "neg": [act.MeleeAtk("tiny fists", aic.STR,5,2,[1,4],aic.BLDG,True), act.RangedAtk("lil bow", aic.DEX,30,4,[1,6], aic.PIRC,True)]}

    boblin_goblin = chr.Character("Boblin the Goblin", 10, 12, 25, 2, dmg_mods,att,
                                  boblins_actions, aic.EAS,aic.EAS,aic.EAS)

    #check name
    if boblin_goblin.name != "Boblin the Goblin":
        raise ValueError("error: boblin has the incorrect name")
    
    #check actions
    if boblin_goblin.all_actions["actions"]["neg"][0].name != "tiny fists":
        raise ValueError("error: tiny fists is not in the neg array")
    if len(boblin_goblin.all_actions["actions"]["pos"]) > 0:
        raise ValueError("error: the pos array doesn't contains actions")
    if len(boblin_goblin.all_actions["bonus_actions"]["pos"]) > 0 or len(boblin_goblin.all_actions["bonus_actions"]["neg"]) > 0:
        raise ValueError("bonus_actions is non-empty")
    if len(boblin_goblin.all_actions["reactions"]["pos"]) > 0 or len(boblin_goblin.all_actions["reactions"]["neg"]) > 0:
        raise ValueError("reactions is non-empty")
    if len(boblin_goblin.all_actions["leg_actions"]["pos"]) > 0 or len(boblin_goblin.all_actions["leg_actions"]["neg"]) > 0:
        raise ValueError("leg_actions is non-empty")
    
    #test the sender/receiver action system
    boblin_goblin.RecieveAction(boblin_goblin, boblin_goblin.all_actions["actions"]["neg"][0], False)
    if boblin_goblin.health.CurrentHP() != 9:
        raise ValueError("Boblin's tinyfist attack didn't do the expected ammount of damage")
    boblin_goblin.RecieveAction(boblin_goblin, boblin_goblin.all_actions["actions"]["neg"][0], False)
    if boblin_goblin.health.CurrentHP() != 8:
        raise ValueError("Boblin's tinyfist attack didn't do the expected ammount of damage")

    print(boblin_goblin.all_actions["actions"]["neg"][1])
    boblin_goblin.RecieveAction(boblin_goblin, boblin_goblin.all_actions["actions"]["neg"][1], False)
    if boblin_goblin.health.CurrentHP() != 6:
        raise ValueError("Boblin's lil bow attack didn't do the expected ammount of damage")

    boblin_goblin.RecieveAction(boblin_goblin, boblin_goblin.all_actions["actions"]["neg"][1], False)
    if boblin_goblin.health.CurrentHP() != 4:
        raise ValueError("Boblin's lil bow attack didn't do the expected ammount of damage")

    boblin_goblin.effects.AddEff(aic.GENERAL_ADV, 1)
    boblin_goblin.RecieveAction(boblin_goblin, boblin_goblin.all_actions["actions"]["neg"][0], False)
    print(boblin_goblin)

    #Check that Characters can be deep copied
    boblin_clone = boblin_goblin.ReturnCopy()
    
    boblin_goblin.health.HealHP(40)
    boblin_goblin.ac.AddMod(5,1)
    boblin_goblin.dmg_mods[aic.BLDG].AddMod(5,1)
    boblin_goblin.effects.AddEff(aic.INVISIBLE,1)
    boblin_goblin.speed.AddMod(5,1)
    boblin_goblin.prof_bonus = 9
    boblin_goblin.attributes[aic.STR].AddMod(10,1)
    
    if boblin_goblin.health.GetValue() != boblin_goblin.health.max_hp:
        raise ValueError("Boblin's current hp was not his max hp")
    if boblin_goblin.health.GetValue() == boblin_clone.health.GetValue():
        raise ValueError("Boblin has the same health as his clone")
    if boblin_goblin.ac.GetValue() == boblin_clone.ac.GetValue():
        raise ValueError("boblin and his clone have the same AC")
    if boblin_goblin.dmg_mods[aic.BLDG].GetValue() == boblin_clone.dmg_mods[aic.BLDG].GetValue():
        raise ValueError("boblin and his clone have the same BLDG damage modifiers")
    if boblin_goblin.speed.GetValue() == boblin_clone.speed.GetValue():
        raise ValueError("boblin and his clone have the same speed")
    if boblin_goblin.prof_bonus == boblin_clone.prof_bonus:
        raise ValueError("boblin and his clone have the same proficiency bonus")
    if boblin_goblin.attributes[aic.STR].GetScore() == boblin_clone.attributes[aic.STR].GetScore():
        raise ValueError("boblin's clone is just as ripped as he is")
    perfect_match = True
    boblin_effects = boblin_goblin.effects.GetEffects()
    clone_effects = boblin_clone.effects.GetEffects()
    for e in range(0, aic.NEFFECT):
        if boblin_effects[e] != clone_effects[e]:
            perfect_match = False
    if perfect_match:
        raise ValueError("boblin and his clone are under the same effects")

    print("Character class is functional")




if "rbr" in desired_tests:
    
    root = rbr.State(None, None, [char_list.boblin_goblin], [char_list.bongo])

    #check to see if basic initialization worked
    if root.teams["party"][0].name != char_list.boblin_goblin.name:
        raise ValueError("Boblin is not a member of the party")
    if root.teams["enemies"][0].name != char_list.bongo.name:
        raise ValueError("Bongo is not a member of the enemies")
    
    #next, check to make sure states are copy by value
    #and not copy by references
    new_state = root.CreateState("party", 0, "actions", "neg", 0, "enemies", 0)
    if new_state.teams["enemies"][0].health.GetValue() == root.teams["enemies"][0].health.GetValue():
        raise ValueError("root Bongo has the same HP as the new_state Bongo")
    

    
    print("RbR is functional")