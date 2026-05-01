
#> mgs:v5.0.0/zombies/powerups/spawn_display
#
# @within	mgs:v5.0.0/zombies/powerups/intercept_item with storage mgs:temp _pu_spawn
#
# @args		x (unknown)
#			y (unknown)
#			z (unknown)
#

$execute if data storage mgs:temp _pu_spawn {{"type":"max_ammo"}} run function mgs:v5.0.0/zombies/powerups/spawn_type/max_ammo {{x:$(x),y:$(y),z:$(z)}}
$execute if data storage mgs:temp _pu_spawn {{"type":"insta_kill"}} run function mgs:v5.0.0/zombies/powerups/spawn_type/insta_kill {{x:$(x),y:$(y),z:$(z)}}
$execute if data storage mgs:temp _pu_spawn {{"type":"double_points"}} run function mgs:v5.0.0/zombies/powerups/spawn_type/double_points {{x:$(x),y:$(y),z:$(z)}}
$execute if data storage mgs:temp _pu_spawn {{"type":"carpenter"}} run function mgs:v5.0.0/zombies/powerups/spawn_type/carpenter {{x:$(x),y:$(y),z:$(z)}}
$execute if data storage mgs:temp _pu_spawn {{"type":"unlimited_ammo"}} run function mgs:v5.0.0/zombies/powerups/spawn_type/unlimited_ammo {{x:$(x),y:$(y),z:$(z)}}
$execute if data storage mgs:temp _pu_spawn {{"type":"nuke"}} run function mgs:v5.0.0/zombies/powerups/spawn_type/nuke {{x:$(x),y:$(y),z:$(z)}}
$execute if data storage mgs:temp _pu_spawn {{"type":"random_perk"}} run function mgs:v5.0.0/zombies/powerups/spawn_type/random_perk {{x:$(x),y:$(y),z:$(z)}}
$execute if data storage mgs:temp _pu_spawn {{"type":"free_pap"}} run function mgs:v5.0.0/zombies/powerups/spawn_type/free_pap {{x:$(x),y:$(y),z:$(z)}}
$execute if data storage mgs:temp _pu_spawn {{"type":"cash_drop"}} run function mgs:v5.0.0/zombies/powerups/spawn_type/cash_drop {{x:$(x),y:$(y),z:$(z)}}

