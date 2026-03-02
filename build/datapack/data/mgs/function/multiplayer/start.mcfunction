
#> mgs:multiplayer/start
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

# Set timer from time_limit
execute store result score #mp_timer mgs.data run data get storage mgs:multiplayer game.time_limit
scoreboard players operation @a mgs.mp.timer = #mp_timer mgs.data

# Call register hooks (external datapacks can set up maps/classes)
function #mgs:multiplayer/register_maps
function #mgs:multiplayer/register_classes

# Signal game start
function #mgs:multiplayer/on_game_start

# Announce
tellraw @a ["",{"translate": "mgs.game_started","color":"gold","bold":true},{"translate": "mgs.good_luck","color":"yellow"}]

