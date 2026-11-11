
#> mgs:v5.4.2/shared/probe_pos
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/shared/check_bounds [ at @s ]
#			mgs:v5.4.2/zombies/stuck_player_bucket [ at @s ]
#			mgs:v5.4.2/zombies/check_bounds_player [ at @s ]
#			mgs:v5.4.2/zombies/max_ammo_at_self [ at @s ]
#			mgs:v5.4.2/zombies/escort/retarget [ at @p[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator] ]
#			mgs:v5.4.2/zombies/powerups/spawn_random_at_self [ at @s ]
#			mgs:v5.4.2/zombies/revive/void_revive_whos_who [ at @s ]
#			mgs:v5.4.2/multiplayer/check_bounds [ at @s ]
#			mgs:v5.4.2/multiplayer/spawn_calc_dist [ at @p[tag=mgs.spawn_enemy] ]
#			mgs:v5.4.2/missions/update_compass [ at @n[tag=mgs.mission_enemy] ]
#

data modify storage mgs:temp _probe_pos set from entity @s Pos
tp @s ~ -1000000 ~
kill @s

