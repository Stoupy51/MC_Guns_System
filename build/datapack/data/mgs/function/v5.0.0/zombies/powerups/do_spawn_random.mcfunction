
#> mgs:v5.0.0/zombies/powerups/do_spawn_random
#
# @executed	at @s
#
# @within	mgs:v5.0.0/zombies/powerups/check_drop with storage mgs:temp _pu_spawn
#
# @args		x (int)
#			y (int)
#			z (int)
#

$execute if score #pu_spawn_type mgs.data matches 1 run function mgs:v5.0.0/zombies/powerups/spawn_type/max_ammo {x:$(x),y:$(y),z:$(z)}
$execute if score #pu_spawn_type mgs.data matches 2 run function mgs:v5.0.0/zombies/powerups/spawn_type/insta_kill {x:$(x),y:$(y),z:$(z)}
$execute if score #pu_spawn_type mgs.data matches 3 run function mgs:v5.0.0/zombies/powerups/spawn_type/double_points {x:$(x),y:$(y),z:$(z)}
$execute if score #pu_spawn_type mgs.data matches 4 run function mgs:v5.0.0/zombies/powerups/spawn_type/carpenter {x:$(x),y:$(y),z:$(z)}
$execute if score #pu_spawn_type mgs.data matches 5 run function mgs:v5.0.0/zombies/powerups/spawn_type/unlimited_ammo {x:$(x),y:$(y),z:$(z)}
$execute if score #pu_spawn_type mgs.data matches 6 run function mgs:v5.0.0/zombies/powerups/spawn_type/nuke {x:$(x),y:$(y),z:$(z)}
$execute if score #pu_spawn_type mgs.data matches 7 run function mgs:v5.0.0/zombies/powerups/spawn_type/random_perk {x:$(x),y:$(y),z:$(z)}
$execute if score #pu_spawn_type mgs.data matches 8 run function mgs:v5.0.0/zombies/powerups/spawn_type/free_pap {x:$(x),y:$(y),z:$(z)}
$execute if score #pu_spawn_type mgs.data matches 9 run function mgs:v5.0.0/zombies/powerups/spawn_type/cash_drop {x:$(x),y:$(y),z:$(z)}

