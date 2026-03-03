
#> mgs:v5.0.0/multiplayer/start
#
# @within	???
#

# Initialize game
data modify storage mgs:multiplayer game.state set value "active"

# Reset scores
scoreboard players set #red mgs.mp.team 0
scoreboard players set #blue mgs.mp.team 0
scoreboard players set @a mgs.mp.kills 0
scoreboard players set @a mgs.mp.deaths 0
scoreboard players set @a mgs.mp.death_count 0

# Set timer from time_limit
execute store result score #mp_timer mgs.data run data get storage mgs:multiplayer game.time_limit
scoreboard players operation @a mgs.mp.timer = #mp_timer mgs.data

# Call register hooks (external datapacks can set up maps/classes)
function #mgs:multiplayer/register_maps
function #mgs:multiplayer/register_classes

# Signal game start
function #mgs:multiplayer/on_game_start

# Give loadout to players who already have a class, show dialog to those who don't
execute as @a at @s if score @s mgs.mp.class matches 1.. run function mgs:v5.0.0/multiplayer/apply_class
execute as @a at @s unless score @s mgs.mp.class matches 1.. run function mgs:v5.0.0/multiplayer/select_class

# Announce
tellraw @a ["",{"translate": "mgs.game_started","color":"gold","bold":true},{"translate": "mgs.pick_your_class","color":"yellow"}]

