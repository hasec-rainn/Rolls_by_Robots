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