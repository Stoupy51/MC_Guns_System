
#> mgs:v5.1.0/shared/probe_pos
#
# @executed	at @s
#
# @within	mgs:v5.1.0/shared/check_bounds [ at @s ]
#			mgs:v5.1.0/zombies/check_bounds_player [ at @s ]
#			mgs:v5.1.0/zombies/dog_max_ammo_at_self [ at @s ]
#			mgs:v5.1.0/zombies/powerups/spawn_random_at_self [ at @s ]
#			mgs:v5.1.0/zombies/revive/void_revive_whos_who [ at @s ]
#			mgs:v5.1.0/multiplayer/check_bounds [ at @s ]
#			mgs:v5.1.0/multiplayer/spawn_calc_dist [ at @p[tag=mgs.spawn_enemy] ]
#			mgs:v5.1.0/missions/update_compass [ at @n[tag=mgs.mission_enemy] ]
#

data modify storage mgs:temp _probe_pos set from entity @s Pos
tp @s ~ -1000000 ~
kill @s

