
#> mgs:v5.1.0/zombies/wunderfizz/on_right_click
#
# @executed	as @n[tag=mgs.wf_new]
#
# @within	mgs:v5.1.0/zombies/wunderfizz/setup_iter {run:"function mgs:v5.1.0/zombies/wunderfizz/on_right_click",executor:"source"} [ as @n[tag=mgs.wf_new] ]
#

execute unless data storage mgs:zombies game{state:"active"} run return fail

# Usable only on the active machine, or a machine that still has an orb here to collect
scoreboard players set #wf_usable mgs.data 0
execute if entity @e[tag=bs.interaction.target,tag=mgs.wf_active] run scoreboard players set #wf_usable mgs.data 1
execute at @n[tag=bs.interaction.target] if entity @n[type=item_display,tag=mgs.wunderfizz_orb,distance=..3] run scoreboard players set #wf_usable mgs.data 1
execute if score #wf_usable mgs.data matches 0 run return fail

# The active machine can be mid-roam: deny
execute if score #wf_move_timer mgs.data matches 1.. if entity @e[tag=bs.interaction.target,tag=mgs.wf_active] run return run function mgs:v5.1.0/zombies/wunderfizz/deny_moving

# Power requirement
execute store result score #wf_power mgs.data run scoreboard players get @n[tag=bs.interaction.target] mgs.zb.wf.power
execute if score #wf_power mgs.data matches 1 unless score #zb_power mgs.data matches 1 run return run function mgs:v5.1.0/zombies/wunderfizz/deny_requires_power

# Capture this machine's config (scores persist into the dispatched function)
scoreboard players operation #wf_mid mgs.data = @n[tag=bs.interaction.target] mgs.zb.wf.id
scoreboard players operation #wf_price mgs.data = @n[tag=bs.interaction.target] mgs.zb.wf.price
scoreboard players operation #wf_allperks mgs.data = @n[tag=bs.interaction.target] mgs.zb.wf.allperks

execute at @n[tag=bs.interaction.target] run function mgs:v5.1.0/zombies/wunderfizz/machine_click

