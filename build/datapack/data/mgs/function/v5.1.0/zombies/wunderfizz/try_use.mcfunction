
#> mgs:v5.1.0/zombies/wunderfizz/try_use
#
# @executed	at @n[tag=bs.interaction.target]
#
# @within	mgs:v5.1.0/zombies/wunderfizz/machine_click
#

execute unless score @s mgs.zb.points >= #wf_price mgs.data run return run function mgs:v5.1.0/zombies/wunderfizz/deny_not_enough_points
scoreboard players operation @s mgs.zb.points -= #wf_price mgs.data

# Stable buyer id
execute unless score @s mgs.zb.wf_pid matches 1.. run function mgs:v5.1.0/zombies/wunderfizz/assign_pid

# Pick a random available perk via the shared pool (all_perks widens it to every perk)
tag @s add mgs.pool_target
scoreboard players operation #pool_all_perks mgs.data = #wf_allperks mgs.data
function mgs:v5.1.0/zombies/perks/pool/choose
tag @s remove mgs.pool_target

# No perk available → refund + notify
execute if score #pool_chosen mgs.data matches ..-1 run scoreboard players operation @s mgs.zb.points += #wf_price mgs.data
execute if score #pool_chosen mgs.data matches ..-1 run return run function mgs:v5.1.0/zombies/wunderfizz/deny_all_owned

# Spawn the spinning orb above the machine and stamp it
function mgs:v5.1.0/zombies/wunderfizz/spawn_orb
scoreboard players operation @n[tag=mgs.wf_orb_new] mgs.zb.wf.buyer = @s mgs.zb.wf_pid
scoreboard players operation @n[tag=mgs.wf_orb_new] mgs.zb.wf.perk = #pool_chosen mgs.data
scoreboard players set @n[tag=mgs.wf_orb_new] mgs.zb.wf.anim 100
# Timeslip: this buyer's spin runs 2x faster (see orb_tick)
scoreboard players set @n[tag=mgs.wf_orb_new] mgs.zb.wf.timeslip 0
execute if score @s mgs.special.timeslip matches 1.. run scoreboard players set @n[tag=mgs.wf_orb_new] mgs.zb.wf.timeslip 1
tag @e[tag=mgs.wf_orb_new] remove mgs.wf_orb_new

playsound minecraft:block.conduit.activate ambient @a[scores={mgs.zb.in_game=1}] ~ ~ ~ 1.0 1.2
playsound minecraft:block.beacon.activate ambient @a[scores={mgs.zb.in_game=1}] ~ ~ ~ 0.6 1.6
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.der_wunderfizz_spinning","color":"gold"}]

