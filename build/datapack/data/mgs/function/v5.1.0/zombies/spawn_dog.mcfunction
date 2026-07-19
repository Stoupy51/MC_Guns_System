
#> mgs:v5.1.0/zombies/spawn_dog
#
# @within	mgs:v5.1.0/zombies/spawn_dog_capped
#

# Tag unlocked special spawns near any alive player (32->64->any helper)
function mgs:v5.1.0/zombies/tag_special_spawns_near_players

# Activation-box gating works exactly as it does for zombie spawns.
execute as @e[tag=mgs.zb_near] if data entity @s data.abox run function mgs:v5.1.0/zombies/filter_spawn_abox

# Pick random from tagged set and spawn
execute as @n[tag=mgs.zb_near,sort=random] at @s run function mgs:v5.1.0/zombies/do_spawn_dog

# Cleanup
tag @e[tag=mgs.zb_near] remove mgs.zb_near

