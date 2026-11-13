
#> mgs:v5.4.2/zombies/mystery_box/sync_presence_display
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/mystery_box/setup_positions
#			mgs:v5.4.2/zombies/save/restore_box
#

kill @e[tag=mgs.mb_presence]
kill @e[tag=mgs.mb_disabled]
execute as @n[tag=mgs.mystery_box_active] at @s positioned ~ ~-0.9 ~ run function mgs:v5.4.2/zombies/mystery_box/summon_presence {extra_tags:""}

function mgs:v5.4.2/zombies/mystery_box/refresh_disabled

