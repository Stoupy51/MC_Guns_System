
#> mgs:v5.1.0/zombies/spawn_zombie
#
# @within	mgs:v5.1.0/zombies/spawn_batch_tick
#

# Tag unlocked zombie spawns near any alive player (shared 32->64->any helper). On return,
# #zb_near_found is 0 iff nothing was tagged, so no global @e existence scan is needed here.
function mgs:v5.1.0/zombies/tag_spawns_near_players

# Activation-box gating: a spawn that defines an activation box is only usable while an alive
# player stands inside that box. Drop box-gated candidates whose box is currently empty.
execute as @e[tag=mgs.zb_near] if data entity @s data.abox run function mgs:v5.1.0/zombies/filter_spawn_abox

# Pick random from tagged set and spawn
execute as @n[tag=mgs.zb_near,sort=random] at @s run function mgs:v5.1.0/zombies/do_spawn_zombie

# Cleanup
tag @e[tag=mgs.zb_near] remove mgs.zb_near

