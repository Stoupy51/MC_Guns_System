
#> mgs:v5.1.0/zombies/powerups/do_spawn_random
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/powerups/spawn_random_at_self
#

execute if score #pu_spawn_type mgs.data matches 1 run data modify storage mgs:temp _pu_spawn.type set value "max_ammo"
execute if score #pu_spawn_type mgs.data matches 2 run data modify storage mgs:temp _pu_spawn.type set value "insta_kill"
execute if score #pu_spawn_type mgs.data matches 3 run data modify storage mgs:temp _pu_spawn.type set value "double_points"
execute if score #pu_spawn_type mgs.data matches 4 run data modify storage mgs:temp _pu_spawn.type set value "carpenter"
execute if score #pu_spawn_type mgs.data matches 5 run data modify storage mgs:temp _pu_spawn.type set value "nuke"
execute if score #pu_spawn_type mgs.data matches 6 run data modify storage mgs:temp _pu_spawn.type set value "unlimited_ammo"
execute if score #pu_spawn_type mgs.data matches 7 run data modify storage mgs:temp _pu_spawn.type set value "random_perk"
execute if score #pu_spawn_type mgs.data matches 8 run data modify storage mgs:temp _pu_spawn.type set value "free_pap"
execute if score #pu_spawn_type mgs.data matches 9 run data modify storage mgs:temp _pu_spawn.type set value "cash_drop"
execute if score #pu_spawn_type mgs.data matches 10 run data modify storage mgs:temp _pu_spawn.type set value "fire_sale"
execute if score #pu_spawn_type mgs.data matches 11 run data modify storage mgs:temp _pu_spawn.type set value "bonfire_sale"
function mgs:v5.1.0/zombies/powerups/spawn_display with storage mgs:temp _pu_spawn

