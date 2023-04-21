# Rolls_by_Robots

# A Need for Improvment
Dungeons and Dragons (D&D) is an incredibly popular tabletop game with over 50 million players and a 33% global year-on-year growth as of 2021[^1]. The 5th, and most popular, edition of D&D is centered around narrating players' adventures as they travel through fictional worlds and complete quests. 

A large part of players' adventures involves fighting monsters they encounter while traveling or completeing quests, and the narrator of the game, known as a Dungeon Master (DM), is responsible for crafting each of these encounters. Thus, to create a fun game, it is important that these encounters provide the right amount of challenge to players. If intimidating, powerful-appearing enemies are a pushover, players will be underwhelmed. Similarly, smaller, unimportant-appearing enemies end up killing the party, players will be frusterated at having their in-game characters killed by something insignificant.

Creating a balanced encounter is difficult as a DM, however. With over 2500 types of enemies to choose from & over 1000 items and spells that can be wielded by players & enemies alike, DMs are often overwhelmed by possibilities[^2].  Though DMs are offered tools to balance their combat encounters, namely the CR system, it is difficult to consider all the items, abilities, and scenarios that could unbalance an encounter.


# The Goal of the Project
My goal is to create software that can quickly emulate and evaluate a combat encounter in D&D 5e, providing a user with feedback on how well the input party is likely to perform in a user-defined combat encounter.
Through this, I hope to provide a powerful tool for creating balanced combat encounters in D&D.

# How Will it Be Accomplished?
The underlying idea behind this project is to use tree search AI to emulate actual combat in D&D. 
Each combat encounter will be represented as a tree, where nodes are "combat-states" (that contain information about the characters, the enemies, and individuals' health)
and edges are actions (a fighter swinging his sword at a goblin might result in a child combat-state node where the goblin has less health).
Starting from the initial combat state, minimax and heuristics will be used to dictate the edge that will be traversed in the tree (the action that will be taken) for the 
player team and the enemy team until eventually no more traversals can be made (ie, one of the teams emerges victorious).

As a dice-based game, luck plays a prominent role in D&D. To account for this, many trees will be generated for the same combat encounter, and the victor for each tree
will be tallied. From this, the expected/average winrate for the given encounter can be deduced from $partyWins \div numTrees$, where $partyWins$ is the number of times
the players won out of the $numTree$ trees that were generated.


[^1]: C. Corliss. "Dungeons and Dragons Infographic Shows How Popular the Game Has Become". *GameRant*. May 19, 2021. [Online], available: https://gamerant.com/dungeons-and-dragons-infographic-2021/. [Accessed March 24, 2023].

[^2]: "Game Rules", *dndbeyond.com*. [Online]. Available: https://www.dndbeyond.com/. [Accessed March 24, 2023]
