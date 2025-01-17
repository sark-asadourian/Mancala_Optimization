## Summary
This project seeks to find the optimal first move for the first player in
Mancala. There are many different variations of Mancala, but this project will use 
the following rules:

- X pieces are placed in each hole
- Player 1 selects 1 hole from their side to pick up all the pieces.
- 1 piece is dropped in each hole in a counter-clockwise direction.
    - if the last piece drop lands in an empty hole on the player's turn ends.
    - if the last piece drop lands in a hole with pieces, then the player picks up all the pieces in that hole and continues dropping pieces.
    - if the last piece is in the goal, then a new hole is selected to start at from the player's side
- the score equals the total number of pieces in the goal

# Datastructure, Algorithm, and Strategy
The key insight is a player is guaranteed to win if more than half of the pieces
in their goal, since it is impossible for the other player to win. This code
seaks to find if this is possible with various board sizes and number of pieces.

This is an ongoing project.
