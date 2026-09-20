
#> mgs:v5.1.0/zombies/wunderfizz/setup
#
# @within	mgs:v5.1.0/zombies/preload_complete
#

scoreboard players set #wf_counter mgs.data 0
data modify storage mgs:temp _wf_iter set from storage mgs:zombies game.map.wunderfizz
execute if data storage mgs:temp _wf_iter[0] run function mgs:v5.1.0/zombies/wunderfizz/setup_iter

# Pick the active spot: a random can_start_on marker, else any marker
execute as @n[tag=mgs.wunderfizz_machine,tag=mgs.wf_can_start,sort=random] run tag @s add mgs.wf_active
execute unless entity @e[tag=mgs.wf_active] as @n[tag=mgs.wunderfizz_machine,sort=random] run tag @s add mgs.wf_active

scoreboard players set #wf_uses mgs.data 0
scoreboard players set #wf_move_timer mgs.data 0

# Live model on the active cabinet, grayed disabled model on the rest, and park inactive interactions
function mgs:v5.1.0/zombies/wunderfizz/sync_displays
function mgs:v5.1.0/zombies/wunderfizz/sync_visibility

