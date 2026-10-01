
#> mgs:zombies/recover
#
# @within	mgs:v5.1.0/zombies/watchdog_tick
#			dialog mgs:v5.1.0/zombies/admin
#

execute unless data storage mgs:zombies game{state:"active"} run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.no_zombies_game_is_active","color":"red"}]

scoreboard players set #zb_wd_ticks mgs.data 0

# Hidden blockers: a desynced dog-portal counter, and portals that never struck (their dogs are lost either way).
scoreboard players set #zb_dog_pending mgs.data 0
kill @e[tag=mgs.dog_portal]

# So recovery cannot race a schedule landing a tick later.
schedule clear mgs:v5.1.0/zombies/start_round

tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.round_was_frozen_recovering","color":"yellow"}]

# round_complete ran (it parks #zb_to_spawn at -1) but start_round never landed.
execute if score #zb_to_spawn mgs.data matches ..-1 run return run function mgs:v5.1.0/zombies/start_round

# Empty map, nothing queued, round never closed.
kill @e[tag=mgs.zombie_round]
scoreboard players set #zb_to_spawn mgs.data 0
function mgs:v5.1.0/zombies/round_complete

