
#> mgs:v5.4.2/zombies/revive/body_missing
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/revive/downed_tick
#

execute unless score @s mgs.zb.bleed matches 1100.. run return run function mgs:v5.4.2/zombies/revive/body_lost
scoreboard players operation @s mgs.zb.bleed -= #tick_delta mgs.data

scoreboard players operation #my_downed_id mgs.data = @s mgs.zb.downed_id
execute as @e[type=minecraft:text_display,tag=mgs.downed_hud,predicate=mgs:v5.4.2/zombies/revive/downed_id_match] run kill @s

ride @s dismount
function mgs:v5.4.2/zombies/revive/respawn_near_player
execute at @s summon minecraft:marker run function mgs:v5.4.2/shared/probe_pos
data modify storage mgs:temp _body_at set from storage mgs:temp _probe_pos
function mgs:v5.4.2/zombies/revive/spawn_downed_body
function mgs:v5.4.2/zombies/revive/tp_to_body with storage mgs:temp

