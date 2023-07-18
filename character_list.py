import characters as chars
import actions as act
import modifiable_objs as mo
import ai_constants as aic
import random as rand
import math as mth
import numpy as np


dmg_mods = {}
for dm in range(0,aic.NDMGTYPE):
    dmg_mods[dm] = mo.DmgMod(aic.NORM)

att = {}
for a in range(0,aic.NATT):
    att[a] = mo.Attribute(a,8)

boblin_goblin = chars.Character("Boblin the Goblin", 10, 12, 25, 2, dmg_mods,att,
                                {"pos":[], "neg": [act.MeleeAtk("tiny fists", aic.STR,5,2,[1,4],aic.BLDG,True), act.RangedAtk("lil bow", aic.DEX,30,4,[1,6], aic.PIRC,True)]}, 
                                aic.EAS,aic.EAS,aic.EAS)


for a in range(0,aic.NATT):
    att[a] = mo.Attribute(a,30)

bongo = chars.Character("Bongo.",1000,5,60,10,dmg_mods,att,
                        {"pos":[], "neg":[act.RangedAtk("True Power Word Kill",aic.CHA,300,2000,[1000,4],aic.NECR,True),act.MeleeAtk("tiny fists", aic.STR,5,2,[1,4],aic.BLDG,True)]},
                        aic.EAS, aic.EAS, aic.EAS)

att[aic.STR] = mo.Attribute(aic.STR,20)
att[aic.DEX] = mo.Attribute(aic.DEX,16)
att[aic.CON] = mo.Attribute(aic.CON,18)
att[aic.WIS] = mo.Attribute(aic.WIS,12)
att[aic.INT] = mo.Attribute(aic.INT,6)
att[aic.CHA] = mo.Attribute(aic.CHA,10)

grog = chars.Character("Grog", 50, 16, 30, 6, dmg_mods,att, 
                       {"pos": [], "neg": [act.MeleeAtk("Axe Swing",aic.STR,5,24,(4,12),aic.SLSH, True), act.MeleeAtk("Fists",aic.STR,5,8,(4,4),aic.BLDG, True) ]},
                         aic.EAS,aic.EAS, aic.EAS)

att[aic.STR] = mo.Attribute(aic.STR,8)
att[aic.DEX] = mo.Attribute(aic.DEX,14)
att[aic.CON] = mo.Attribute(aic.CON,12)
att[aic.WIS] = mo.Attribute(aic.WIS,10)
att[aic.INT] = mo.Attribute(aic.INT,10)
att[aic.CHA] = mo.Attribute(aic.CHA,20)
scanlan = chars.Character("Scanlan", 30, 15, 25, 6, dmg_mods, att, 
                          {"pos": [], "neg": [act.MeleeAtk("tiny fists", aic.STR,5,2,[1,4],aic.BLDG,True)]},
                            {"pos": [act.Heal("Healing Word", aic.CHA, 30, 4, (1,4))], "neg": []})