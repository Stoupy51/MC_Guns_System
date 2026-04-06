
#> mgs:v5.0.0/zombies/pap/anim/restore_display
#
# @executed	at @s
#
# @within	mgs:v5.0.0/zombies/pap/anim/retreat_finish
#			mgs:v5.0.0/zombies/pap/anim/collect_give
#

execute store result storage mgs:temp _pap_restore.id int 1 run scoreboard players get @s mgs.zb.pap.id
function mgs:v5.0.0/zombies/pap/anim/restore_display_lookup with storage mgs:temp _pap_restore

