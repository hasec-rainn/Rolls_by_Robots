import modifiable_objs as mo
import ai_constants as aic

desired_tests = ["DmgMod","Attribute"]

if "Health" in desired_tests:
    hp = mo.Health(30)
    
    #check to ensure basic functionality
    if hp.max_hp != 30:
        print("hp should have hp.max_health=30")
        raise ValueError("hp.max_health was " + str(hp.max_hp))

    #check to ensure SubHP method works
    hp.GiveTempHP(10,30)
    hp.GiveTempHP(5,25)
    hits = [3,4,7,2,1,1]
    hp_copy = hp.ReturnCopy()
    max_hp = 45
    for h in hits:
        hp.SubHP(h)
        max_hp = max_hp - h
        if hp.GetValue() != max_hp:
            print("hp.GetValue should be", max_hp)
            raise ValueError("For hit " + str(h) + " hp.GetValue()=" + str(hp.GetValue()))

    #check to ensure copy by value works
    if hp.GetValue() == hp_copy.GetValue():
        raise ValueError("Copy by reference failed: hp and hp_copy have same values")
    
    print("Health class is functional")

if "Attribute" in desired_tests:

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

if "DmgMod" in desired_tests:
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