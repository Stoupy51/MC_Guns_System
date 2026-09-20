
#> mgs:v5.1.0/zombies/wunderfizz/sync_displays
#
# @within	mgs:v5.1.0/zombies/wunderfizz/setup
#			mgs:v5.1.0/zombies/wunderfizz/do_relocate
#

execute as @e[tag=mgs.wf_display] run function mgs:v5.1.0/zombies/wunderfizz/set_display_disabled
scoreboard players set #wf_active_id mgs.data -1
execute as @n[tag=mgs.wf_active] run scoreboard players operation #wf_active_id mgs.data = @s mgs.zb.wf.id
execute as @e[tag=mgs.wf_display] if score @s mgs.zb.wf.id = #wf_active_id mgs.data run function mgs:v5.1.0/zombies/wunderfizz/set_display_live

