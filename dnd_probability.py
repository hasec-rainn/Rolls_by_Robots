# Putting together some D&D logic for Chase

# This class is the bulk of the 'probability' part.
# For ease of reading, run this file and check out the outcomes (reading along from line 56).
# Or not; I'm a comment not a cop!
class OutcomeSet:
  def __init__(self, name, valueMap):
    self.name = name
    self.valueMap = valueMap
  
  # Helper function: return set of values and probabilities
  def vps(self):
    return self.valueMap.items()  # Example: [(1,0.25), (2,0.25), (3,0.25), (4,0.25)] for a d4

  # Return the OutcomeSet of every combination of possible events.  E.G. d6.cross(d6) returns 36 tuple values in an OutcomeSet: (1,1), (1,2), ...
  def cross(self, otherSet):
    return OutcomeSet(f"{self.name} * {otherSet.name})", {(x,y): px*py for x,px in self.vps() for y,py in otherSet.vps()})
  
  # Where the magic happens.  Map a function onto the values in the OutcomeSet, combine probabilities if the function is many:one.  Examples later on.
  def map(self, fn, newName):
    newMap = {}
    for v,p in self.vps():
      newV = fn(v)
      # Allow OutccomeSet-valued results
      if isinstance(newV, OutcomeSet):
        for vv,pp in newV.vps() :
          newMap[vv] = p*pp + newMap.setdefault(vv,0)
      else:
        newMap[newV] = p + newMap.setdefault(newV,0)
    return OutcomeSet(newName, newMap)
  
  # Weighted average of values.
  # Prereq: valueMap values must be numeric, otherwise this will error out.
  def expected_value(self):
    outcome = 0
    for v,p in self.vps():
      outcome += v*p
    return outcome
  
  # Pretty-print the results and probabilities (to 4 significant digits, arbitrarily)
  def print(self):
    print(f"== {self.name} ==")
    N = len(self.valueMap)
    for v,p in sorted(self.vps()):
      print('%.4f: %s' % (p,v))
    print()

def UniformSet(name, values):
  N = len(values)
  return OutcomeSet(name, {v: 1.0/N for v in values})

# d4, d6, d20, etc.
def Die(maxValue):
  return UniformSet(f"d{maxValue}", range(1,maxValue+1))

# Examples: d6, d20
d6 = Die(6)
d6.print()
print(f"Average value: {d6.expected_value()}")
print()

d20 = Die(20)
d20.print()

def ge12(v):
  if v >= 12:
    return "yes"
  return "no"

Die(20).map(ge12, "Roll d20, Is result >= 12 ?").print()

def reroll_ones(v):
  if v == 1:
    return Die(20)
  return v

Die(20).map(reroll_ones, "Roll d20, re-roll ones.  Halflings are lucky buggers.").print()

twod20 = Die(20).cross(Die(20))
twod20.map(max, "Roll with Advantage, no modifier.").print()

def SavingThrow(modifier, DC):
  def STresult(v):
    if v + modifier >= DC:
      return "success"
    return "failure"
  modifier_sign = "+" if modifier >= 0 else ""
  return Die(20).map(STresult, f"Saving Throw: DC {DC}, modifier {modifier_sign}{modifier}")

SavingThrow(4,15).print()
SavingThrow(-1,15).print()

def AbilityCheck(modifier, DC):
  def ACresult(v):
    if v + modifier >= DC:
      return "pass"
    return "fail"
  modifier_sign = "+" if modifier >= 0 else ""
  return Die(20).map(ACresult, f"Ability Check: DC {DC}, modifier {modifier_sign}{modifier}")

SavingThrow(2,10).print()
SavingThrow(0,25).print()

def AttackRoll(modifier, AC):
  def AtkResult(v):
    if v == 20:
      return "critical hit"
#    if v == 1:
#      return "critical failure"
    if v + modifier >= AC:
      return "hit"
    return "miss"
  modifier_sign = "+" if modifier >= 0 else ""
  return Die(20).map(AtkResult, f"Attack Roll: AC {AC}, attack bonus {modifier_sign}{modifier}")


AttackRoll(5,12).print()
AttackRoll(5,15).print()

print("So, you're facing a ... Ghoul, say.  AC 12, Int 7 (-2).")
print("Option 1: hit it with a Light Crossbow, you've got Dex 14 (+2) and Proficiency Bonus 2 so that's +4 to hit:")
print()

# Function-valued function: a little fucky, sorry!
def plus(n):
  def plus_fn(v):
    return v+n
  return plus_fn

# Function-valued function: atk_roll in, damage out
def light_crossbow_damage(dmg_mod):
  def light_crossbow_fn(atk_roll):
    if atk_roll == "miss":
      return 0
    if atk_roll == "hit":
      return Die(8).map(plus(dmg_mod), f"d8+{dmg_mod}")
    if atk_roll == "critical hit":
      damage_dice = Die(8).cross(Die(8))
      damage_dice_total = damage_dice.map(sum, "2d8")
      return damage_dice_total.map(plus(dmg_mod), f"2d8+{dmg_mod}")
  return light_crossbow_fn

# So the Light Crossbow calculations:
atk = AttackRoll(2, 12)
atk.print()
atk_dmg = atk.map(light_crossbow_damage(2), "Light Crossbow Damage")
atk_dmg.print()

print(f"Light Crossbow E[damage]: {atk_dmg.expected_value()}")
print()

print("Option 2: Mind Sliver.  You're a Sorcerer with Cha 18 (+4), proficiency bonus 2 so that's +6 to hit and spell save DC 14:")
print()

def mind_sliver_damage(saving_throw):
  if saving_throw == "success":
    return 0
  if saving_throw == "failure":
    return Die(6)  # Note: ignoring damage type (psychic, vs piercing above)
    # Note also: ignoring this spell's other effect on a failed save (-1d4 Ghoul's next Saving Throw)

# So the Mind Sliver calculations:
save = SavingThrow(-2, 14)
save.print()
spell_dmg = save.map(mind_sliver_damage, "Mind Sliver Damage")
spell_dmg.print()

print(f"Mind Sliver E[damage]: {spell_dmg.expected_value()}")
print()

print("Hah!  So even vs. a low-Int monster, a spellcaster with OK dex should use a crossbow rather than a cantrip.")
print("What if their dex was worse?  +0 instead of +2?")
print()

atk = AttackRoll(0, 12)
atk.print()
atk_dmg = atk.map(light_crossbow_damage(0), "Light Crossbow Damage (+0 dex)")
atk_dmg.print()

print(f"Light Crossbow E[damage] (+0 dex): {atk_dmg.expected_value()}")
print()

print("Nice, in that case the cantrip is better.")

print("Just for lulz and because it's unusual, let's do Magic Missile:")
print()

def magic_missile_damage(hittiness):
  if hittiness == "hit":
    twod4 = Die(4).cross(Die(4)).map(sum, "2d4")
    threed4 = twod4.cross(Die(4)).map(sum, "3d4") # Oh this definitely needs a helper function.
    # ... or possibly better handling of tuples at the OutcomeSet level
    return threed4

does_it_hit = OutcomeSet("Certain Hit", {"hit": 1})
does_it_hit.print()
spell_dmg = does_it_hit.map(magic_missile_damage, "Magic Missile Damage")
spell_dmg.print()

print(f"Magic Missile E[damage]: {spell_dmg.expected_value()}")
print()

# To be clear, I could've skipped most of that nonsense above and just done:
twod4 = Die(4).cross(Die(4)).map(sum, "2d4")
spell_dmg = twod4.cross(Die(4)).map(sum, "Magic Missile Damage")
# The rest was mostly to showcase a custom OutcomeSet, in case that's necessary somewhere.  And pattern matching.

print("Okay have fun! Excited to see what becomes of this.")