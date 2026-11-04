
#> mgs:v5.3.0/zombies/portal_strike
#
# @within	mgs:v5.3.0/dialog/close_then
#			mgs:v5.3.0/zombies/portal_tick
#

function mgs:v5.3.0/zombies/portal_strike_fx

# Delivered at ground level and awake, so no rise.
data modify storage mgs:temp _mob set from entity @s data.mob
data modify storage mgs:temp _mob.no_ai set value 0b
scoreboard players operation #zb_spawn_sid mgs.data = @s mgs.zb.spawn.sid
execute store result score #zb_spawn_x mgs.data run data get entity @s Pos[0]
execute store result score #zb_spawn_z mgs.data run data get entity @s Pos[2]
execute positioned ~ ~0.2 ~ run function mgs:v5.3.0/zombies/mob/spawn
function mgs:v5.3.0/zombies/arrival/land

scoreboard players remove #zb_portal_pending mgs.data 1
kill @s

