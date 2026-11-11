
#> mgs:v5.4.2/zombies/revive/respawn_near_player
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/revive/revive_complete
#			mgs:v5.4.2/zombies/revive/do_round_respawn
#			mgs:v5.4.2/zombies/revive/void_revive_whos_who
#			mgs:v5.4.2/zombies/revive/void_revive_solo_qr
#

execute unless data entity @s LastDeathLocation run return run function mgs:v5.4.2/zombies/revive/respawn_at_random_spawn

# The player is excluded from the teammates they join.
tag @s add mgs.spawn_pending
data modify storage mgs:temp _body set value {}
data modify storage mgs:temp _body.dimension set from entity @s LastDeathLocation.dimension
execute store result storage mgs:temp _body.x int 1 run data get entity @s LastDeathLocation.pos[0]
execute store result storage mgs:temp _body.y int 1 run data get entity @s LastDeathLocation.pos[1]
execute store result storage mgs:temp _body.z int 1 run data get entity @s LastDeathLocation.pos[2]
scoreboard players set #respawn_done mgs.data 0
function mgs:v5.4.2/zombies/revive/respawn_at_body with storage mgs:temp _body
tag @s remove mgs.spawn_pending
execute if score #respawn_done mgs.data matches 0 run function mgs:v5.4.2/zombies/revive/respawn_at_random_spawn

