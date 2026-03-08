
#> mgs:v5.0.0/zombies/stop
#
# @within	mgs:v5.0.0/zombies/game_over 100t [ scheduled ]
#

# Set state to lobby
data modify storage mgs:zombies game.state set value "lobby"

# Cancel scheduled functions
schedule clear mgs:v5.0.0/zombies/end_prep
schedule clear mgs:v5.0.0/zombies/start_round

# Restore movement
execute as @a[scores={mgs.zb.in_game=1}] run attribute @s minecraft:movement_speed base set 0.1
execute as @a[scores={mgs.zb.in_game=1}] run attribute @s minecraft:jump_strength base set 0.42

# Clear effects
effect clear @a[scores={mgs.zb.in_game=1}] darkness
effect clear @a[scores={mgs.zb.in_game=1}] blindness
effect clear @a[scores={mgs.zb.in_game=1}] night_vision

# Restore adventure mode for spectating players
gamemode adventure @a[scores={mgs.zb.in_game=1},gamemode=spectator]

# Kill all zombies mode entities
kill @e[tag=mgs.zombie_round]
kill @e[tag=mgs.gm_entity]

# Remove forceload (only if bounds were set)
execute if score #zb_has_bounds mgs.data matches 1 run function mgs:v5.0.0/zombies/remove_forceload

# Remove sidebar
scoreboard objectives setdisplay sidebar
scoreboard objectives remove mgs.zb_sidebar

# Announce
tellraw @a [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.zombies_game_ended","color":"red"}]

# Reset in-game state
scoreboard players set @a mgs.zb.in_game 0
scoreboard players set @a mgs.zb.points 0
scoreboard players set @a mgs.zb.kills 0
scoreboard players set @a mgs.zb.downs 0
scoreboard players set @a mgs.zb.passive 0
scoreboard players set @a mgs.zb.ability 0
scoreboard players set @a mgs.zb.ability_cd 0
scoreboard players set @a mgs.mp.spectate_timer 0
tag @a[tag=mgs.give_class_menu] remove mgs.give_class_menu

# Reset mystery box
function mgs:v5.0.0/zombies/mystery_box/reset

