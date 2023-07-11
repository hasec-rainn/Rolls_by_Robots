import characters as chars
import actions as act
import modifiable_objs as mo
import ai_constants as aic
import random as rand
import math as mth
import numpy as np

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
        self.parent = parent #useful if a particular action reverses a pervious action
        self.parent_action = parent_action #useful for conditional actions
        self.children = []

    def DeepCopy(self):
         copy = State(self.parent, self.parent_action, self.teams["party"], self.teams["enemies"])
         return copy

    def CreateStates(self, 
                       s_team : str, sender : int, a_type : str, posneg : str, s_action : int, 
                       r_team : str, receiver : int, 
                       append_state_to_children : bool = False) -> None:
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
        if s_team != "party" or s_team != "enemies":
                raise ValueError("s_team is neither 'party' nor 'enemies'")
        if r_team != "party" or r_team != "enemies":
                raise ValueError("r_team is neither 'party' nor 'enemies'")
        
        #create a deep copy of the current state as
        new_state = None

        #send the appropriate action to the appropriate character
        action = self.teams[r_team][sender][a_type][posneg][s_action]
        print(action)
        
        if set_children_to_results:
            self.children = new_states
        return new_states
