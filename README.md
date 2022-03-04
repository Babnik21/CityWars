# CityWars
Strategy game. Goal is to develop cities, train your army and defeat enemies.

Goals of this project are:
* Develop the game in python and make a simple user interface with `pygame` module.
* Make simple non-player characters (NPCs) for singleplayer mode
* Make a smarter AI opponent (bot) to hopefully make the game challenging to play in singleplayer mode
* (Multiplayer support - if there's time and will :) )

## Game description
CityWars is a turn-based strategy game where the goal is to develop cities and build armies to defeat opponents. 
It takes inspiration from other similar online games such as Travian and Tribal Wars. The goal is to 
conquer all the cities on the map in order to win the game (subject to change).

There are 4 types of tasks/moves a player can start each turn:
* Build 
* Upgrade buildings
* (Demolish buildings)
* Train troops
* Attack opponents

A player is not only limited to 3 tasks/moves each turn, but is also limited with available resources, 
that can be produced in certain buildings or stolen from other players. By upgrading those buildings or 
training larger armies, one is able to produce or steal more resources and progress faster.

Each city has a pre-determined size (6, 9 or 12 building slots + extra wall slot). It is important to 
think in advance which buildings are really neccessary for each city, in order to not run out of 
space for other buildings one desperately needs.

## NPC description

I'm looking to create NPC cities that develop by themselves. The main purpose for those is to be conquered
by player characters. They are meant to develop at a slightly slower pace than players in order to not 
get completely annihilated by every player and instead at least put up a fight. Their task selection logic
is very basic; randomly select actions among available ones and do not send attacks on other players (subject
to change based on effectivenes of such approach).

## Bot desctiption

Now the bot, on the other hand, is meant to pose a bigger threat for the player and actually compete 
for the victory and challenge the user. More on this topic later once I get to it.
