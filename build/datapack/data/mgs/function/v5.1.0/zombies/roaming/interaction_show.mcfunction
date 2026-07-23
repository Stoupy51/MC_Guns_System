
#> mgs:v5.1.0/zombies/roaming/interaction_show
#
# @executed	as @e[tag=mgs.mystery_box_pos] & at @s
#
# @within	mgs:v5.1.0/zombies/mystery_box/sync_interaction_one
#			mgs:v5.1.0/zombies/wunderfizz/sync_visibility_one
#

tp @s ~ ~512 ~
tag @s remove mgs.roam_hidden

