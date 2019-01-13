# Monopoly Probability
#### Created by Adiel Felsen

## Description
This is a python application used for analyzing the statistics of a monopoly game. This application can either be used for simulating a single game of monopoly, gathering data from thousands of simulated games or finding ideal gameplay strategies.

## Modules of Game class
* This program uses [graphics](http://www.pas.rochester.edu/~rsarkis/csc161/python/pip-graphics.html) to display game board and data
* This program also uses [colour](https://pypi.org/project/colour/) to color code the data with a gradient

## Methods
1. simulate(): This method simulates a game of monopoly. If turnByTurn == True, the game board is displayed on the _graphics_ display and clicking the screen advances the game.
2. simulateMany(n): This method simulates n number of games. At the end, statistics are displayed on the game board.
3. drawBoard(): This method draws the game board. This is used to display turn information or statistics at the end of a multi-game simulation
4. findStrategy(): This method changes key variables to track the best strategy for the best odds of winning.
5. displayWinLossTieRatio(): This method displays the win/loss/tie ratio. Displayed in the center of the game board.
6. displayPercentLandedOn(): This method displays the percent each property was landed on. Displayed on the bottom row of each property.
7. displayLostOnProperties(): This method displays the percent of the time a property was lost on. Displayed on the bottom row of each property.
8. displayLosingProperties(): This method displays the percent of the time a player who placed second owned each property. Displayed on the bottom row of each property.
9. displayWinningProperties(): This method displays the percent of the time a winner owned each property. Displayed on the upper row of each property.
10. displaySpecificGame(): This method allows the user to display the ending of a specific game played in a multi-game simulation.


## Changing modes, altering starting conditions:
* Certain parts of the code can be edited to change modes and the starting conditions of players. These parts are clearly indicated in main(), surrounded by # symbols.

  ############### Edit Values Below ##############

  values

  ################################################

Values:
* numPlayers: The number of players in the game
* turnByTurn: Set as "True" for a single game simulation. False for a 10,000 game analysis
* turnSkip: During a single game, this determines how many turns are played after each mouse click
* playerMoneyList: The starting money for each player
* propertiesOwnedList: Properties owned for each player
* posList: The starting points for each player
* masterHousesList: The number of houses on each property
   * For example: masterHousesList[9] = 4 would put 4 houses on the ninth square (Connecticut Avenue)
* masterMortgageList: The number values of all mortgaged properties
* middlePot: The amount of money in the middle pot

## Explanation of symbols
1. Gameplay information:
   * Circles: Represent the players
   * Colored numbers below property names: The player who owns the property
   * Red M on the bottom right of property names: Indicate that a property is mortgaged
   * Green number on the bottom left of property names: Indicate the number of houses on that property
   * Red "J" on "In Jail": Indicates whether a player is currently in jail (rather than "just visiting")
   * Center: Displays other gameplay information - player money, dice roll, middle pot, chance/community card values

2. Upon completion of many games:
   * Upper numbers on properties: Represents the percent of winners who owned the property
   * Lower numbers on properties: Represents one of many statistics
      1. Percent of the time the property was landed on
      2. Times the property was lost on
      3. Percent of the time a player in 2nd place owned the property
   * Middle-Top: Percent of properties owned by winner and second place
   * Middle-Bottom: Percent wins, losses and ties for each player

## Rules that the players follow (in order):
Before roll
1. Unmortgaging: If the player has the money, try to unmortgage properties - prioritizing properties with houses
2. Houses: If the player has a monopoly and $200 more  than the cost of a house, try to build as many houses as possible

After Roll
1. Jail: If the player is in jail, try to get out in this order - get out of jail card --> pay $50 --> roll for doubles --> if player has rolled 3 times, automatic
2. Doubles 3 times: If the player rolled doubles three times, go to jail
3. Snake eyes: If the player rolled double 1s, get $100
4. Landing on go: Get extra $200
5. Landing on/passing go: Get $200
6. Landing on "Go to jail": Go to jail
7. Landing on "Free Parking": Get middle pot ($500 plus taxes payed to the middle)
8. Landing on "Chance" or "Community Chest": Follow instructions on the card
9. Buying properties: If the player has the money and lands on an unowned property, buy it
10. Paying rent: If the player lands on an already owned property, pay the rent
11. Paying taxes: If the player lands on a square that requires taxes, pay the taxes
12. Mortgaging: If the player has zero or negative money after paying, mortgage properties - prioritizing properties without houses
13. Losing: If the player has zero or negative money at the end of the turn, the player loses and properties are returned to the bank.
14. Winning: If there is only one player at the end of a turn, that player wins
15. Tying: If the game has been played for 1000 turns without a winner, the game is called as a draw

## Interesting Findings (so far)
* In a three person game without trades, about 50% of games end in a stalemate
* Starting out with the dark purple/brown monopoly and building on it immediately significantly reduces your odds of winning. The lack of money at the beginning is far worse than the slight benefit of the purple monopoly
  * However, starting with and building on any other monopoly is beneficial
* Properties that winners tend to have does not seem to directly correlate with the most landed on properties
* Boardwalk is the most common property owned by winners
* The dark purple/brown properties are least likely to be landed on and among the least common owned by winners


## Example
<img src="READMEexamples/MonopolySingle1.png" width="48%"/> <img src="READMEexamples/MonopolyTenThousand.png" width="48%"/>
