
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

# Give loadout to players who already have a class (positive = standard, negative = custom)
execute as @a at @s unless score @s mgs.mp.class matches 0 run function mgs:v5.0.0/multiplayer/apply_class

# For players with no class: auto-apply default custom loadout if set, otherwise show class dialog
execute as @a at @s if score @s mgs.mp.class matches 0 if score @s mgs.mp.default matches 1.. run function mgs:v5.0.0/multiplayer/auto_apply_default
execute as @a at @s if score @s mgs.mp.class matches 0 run function mgs:v5.0.0/multiplayer/select_class

# Announce
tellraw @a ["",[{"text":"","color":"gold","bold":true},"⚔ ",{"translate": "mgs.game_started"},"! "],{"translate": "mgs.pick_your_class","color":"yellow"}]

