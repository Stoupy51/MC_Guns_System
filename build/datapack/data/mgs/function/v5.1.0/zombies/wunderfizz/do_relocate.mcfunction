
#> mgs:v5.1.0/zombies/wunderfizz/do_relocate
#
# @within	mgs:v5.1.0/zombies/wunderfizz/move_tick
#

tag @e[tag=mgs.wf_active] add mgs.wf_prev_active
tag @e[tag=mgs.wf_active] remove mgs.wf_active
execute as @n[tag=mgs.wunderfizz_machine,tag=!mgs.wf_prev_active,sort=random] run tag @s add mgs.wf_active
tag @e[tag=mgs.wf_prev_active] remove mgs.wf_prev_active

function mgs:v5.1.0/zombies/wunderfizz/sync_displays
function mgs:v5.1.0/zombies/wunderfizz/sync_visibility

# Arrival particles/sound at the new active cabinet
execute as @n[tag=mgs.wf_active] at @s run particle minecraft:end_rod ~ ~-1 ~ 0.3 1.5 0.3 0.05 25 force @a[distance=..64]
execute as @n[tag=mgs.wf_active] at @s run playsound minecraft:entity.lightning_bolt.impact ambient @a[scores={mgs.zb.in_game=1}] ~ ~ ~ 0.6 1.6

