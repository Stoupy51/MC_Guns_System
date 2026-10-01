
#> mgs:v5.1.0/zombies/spawn_zombie
#
# @within	mgs:v5.1.0/zombies/spawn_batch_tick
#

# On return #zb_near_found is 0 if nothing was tagged.
function mgs:v5.1.0/zombies/tag_spawns_near_players

# A spawn with an activation box is only usable while an alive player stands in that box.
execute as @e[tag=mgs.zb_near] if data entity @s data.abox run function mgs:v5.1.0/zombies/filter_spawn_abox

execute as @n[tag=mgs.zb_near,sort=random] at @s run function mgs:v5.1.0/zombies/do_spawn_zombie

tag @e[tag=mgs.zb_near] remove mgs.zb_near

