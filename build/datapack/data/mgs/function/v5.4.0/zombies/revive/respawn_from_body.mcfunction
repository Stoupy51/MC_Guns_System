
#> mgs:v5.4.0/zombies/revive/respawn_from_body
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/zombies/revive/respawn_at_body
#

execute store success score #respawn_done mgs.data run tag @n[tag=mgs.spawn_point,tag=mgs.spawn_zb_player,tag=mgs.spawn_unlocked,distance=..20] add mgs.spawn_candidate
execute if score #respawn_done mgs.data matches 1 as @n[tag=mgs.spawn_candidate] run function mgs:v5.4.0/shared/tp_to_spawn {mode:"zombies"}
tag @e[tag=mgs.spawn_candidate] remove mgs.spawn_candidate
execute if score #respawn_done mgs.data matches 1 run return 1

execute store success score #respawn_done mgs.data if entity @p[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator,tag=!mgs.spawn_pending]
execute if score #respawn_done mgs.data matches 1 run tp @s @p[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator,tag=!mgs.spawn_pending]

