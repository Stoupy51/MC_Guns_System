
#> mgs:v5.1.0/zombies/wunderfizz/sync_visibility_one
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/wunderfizz/sync_visibility [ at @s ]
#

execute if entity @s[tag=mgs.wf_active] if entity @s[tag=mgs.roam_hidden] run function mgs:v5.1.0/zombies/roaming/interaction_show
execute unless entity @s[tag=mgs.wf_active] unless entity @s[tag=mgs.roam_hidden] run function mgs:v5.1.0/zombies/roaming/interaction_hide

