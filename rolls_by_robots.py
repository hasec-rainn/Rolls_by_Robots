import characters as chars
import actions as act
import modifiable_objs as mo
import ai_constants as aic
import random as rand
import math as mth
import numpy as np
import character_list as char_list

class State:
     def __init__(self, parent : "State", parent_action : act.Action, 
                    party : list[chars.Character], enemies : list[chars.Character]):
          """
          A State is a snapshot of a particular moment in a combat encounter.
          States are connected to each other in a tree structure, where edges are actions
          that can be taken which lead to other states
          * `party` contains each of the player characters that individuals are playing
          * `enemies` contains all of the enemies that the DM is controling
          """
          self.teams = {"party" : party, "enemies" : enemies}
          self.score = self.__score__(self)
          self.parent = parent #useful if a particular action reverses a pervious action
          self.parent_action = parent_action #useful for conditional actions
          self.children = []

     def __score__(self):
          """
          Calculates the score of a state. Should only be called
          from `CreateState()` method.

          score is calculated as follows: sum(party_health) - sum(enemies_health).
          """
          score = 0
          for c in self.teams["party"]:
               score += c.health.CurrentHP()
          for c in self.teams["enemies"]:
               score -= c.health.CurrentHP()
          
          self.score = score

     def __lt__(self, s : "State"):
          return self.score < s.score

     def ReturnCopy(self):
          """
          Creates a deep copy of the state and returns it.
          """
          party = []
          for player in self.teams["party"]:
               party.append(player.ReturnCopy())

          enemies = []
          for enemy in self.teams["enemies"]:
               enemies.append(enemy.ReturnCopy())

          return State(self.parent, self.parent_action, party, enemies)

     def CreateState(self, 
                         s_team : str, sender : int, a_type : str, posneg : str, s_action : int, 
                         r_team : str, receiver : int, 
                         append_state_to_children : bool = False) -> "State":
          """
          From the team defined by `s_team`, have the character `sender` apply the action 
          `s_action` to the character `receiver` on the team `r_team`.
          The type of action being applied is determined by
          `atype`, and if the attack is helpful/harmful is determined by `posneg`.
          * `s_team` and `r_team` can take on the following values: ["party", "enemies"]
          * `a_type` can take on the following values: ["actions", "bonus_actions", "reactions", "leg_actions"]
          * `posneg` can take on the following values: ["pos", "neg"]
          * `s_action` is an integer used to index into a particular action dictionary of the character `sender`
          * `sender` amd `receiver` are integers to index into the party or enemies Character arrays
          * `append_state_to_children` determines if the new state is appended to the `self.children` 
          array
          """

          #make sure s_team and r_team are valid values
          if s_team != "party" and s_team != "enemies":
                    raise ValueError("s_team is neither 'party' nor 'enemies'")
          if r_team != "party" and r_team != "enemies":
                    raise ValueError("r_team is neither 'party' nor 'enemies'")
          
          #make sure a_type is valid
          if a_type != "actions" and a_type != "bonus_actions" \
          and a_type != "reactions" and a_type != "leg_actions":
               raise ValueError("a_type is an unexpected value")
          
          #make sure posneg is valid
          if posneg != "pos" and posneg != "neg":
               raise ValueError("posneg is an unexpected value")

          #create a deep copy of the current state for our new state
          new_state = self.ReturnCopy()
          new_state.parent = self

          #grab the appropriate action from the appropriate character
          s_character = new_state.teams[s_team][sender] 
          a = s_character.all_actions[a_type][posneg][s_action]
          new_state.parent_action = a
          
          #apply the action to the specified character (receiver) 
          new_state.teams[r_team][receiver].RecieveAction(s_character, a, False)

          #calculate the score of the state
          new_state.__score__()

          #add this state to the children list if specified
          #regardless, return the new state
          if append_state_to_children:
               self.children.append(new_state)
          return new_state



class Team:
    """
    Class which represents a particular `team`, either "enemies" or "party".
    Given a `State` object as an input, will try to maximize (if self.team = "party") 
    or minimize (if self.team = "enemies") the score of the state object.
    """
    def __init__(self, team : str):
        if team != "party" and team != "enemies":
             raise ValueError("Error: Team class initialized with invalid team string")
        
        self.team = team
        self.opp_team = None
        if team == "party":
            self.opp_team = "enemies"
        else:
             self.opp_team = "party"
        
    def MiniMax(self, s : State, c : int, a_type : str) -> State:
         """
         Actual function which performs the maximization / minimization.
         * `s` is the state which will be maximized or minimized
         * `c` is the index of the character on team `team` whose turn it is in combat. 
         This is the character which the `Team` object can control in order to perform
         its maximization.
         * `a_type` is the type of action that the character may peform. Action types
         include the following: `"actions"`, `"bonus_actions"`, `"reactions"`, `"leg_actions"`.

         Returns the state which either has the maximum (party) or minimum (enemies)
         score. Whether maximum or minimum is chosen is based off `self.team`
         """

         #ensure `a_type` is valid
         if a_type not in ["actions", "bonus_actions", "reactions", "leg_actions"]:
              raise ValueError("invalid a_type used in MiniMax")

         #try performing every action of every action type availabe to the character
         #in order to see what action(s) would be the best to take
         sorted_states = {} #entries are lists sorted on score in descending order

         sorted_states = [] #each list is accessed by using an a_type as a key
          
         #every combination of (neg_action, opp_team_character)
         n_neg_action = len(s.teams[self.team][c].all_actions[a_type]["neg"])
         n_opp_team_members = len(s.teams[self.opp_team])
         for s_action in range(0, n_neg_action):
              for receiver in n_opp_team_members:
                   sorted_states.append(s.CreateState(self.team, c, a_type, "neg", s_action, self.opp_team, receiver))

         #every combination of (pos_action, same_team_character)
         n_pos_action = len(s.teams[self.team][c].all_actions[a_type]["pos"])
         n_same_team_members = len(s.teams[self.team])
         for s_action in range(0, n_pos_action):
              for receiver in n_same_team_members:
                   sorted_states.append(s.CreateState(self.team, c, a_type, "pos", s_action, self.team, receiver))

         #now lets sort the states (in place) based on their score
         sorted_states.sort()
          
         #now that we have our states sorted, we can return the optimal one
         if self.team == "party":
              return sorted_states[ len(sorted_states)-1 ]
         else:
              return sorted_states[0]