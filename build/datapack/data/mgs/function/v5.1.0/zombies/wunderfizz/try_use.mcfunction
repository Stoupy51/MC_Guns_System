
#> mgs:v5.1.0/zombies/wunderfizz/try_use
#
# @executed	at @n[tag=bs.interaction.target]
#
# @within	mgs:v5.1.0/zombies/wunderfizz/machine_click
#

execute unless score @s mgs.zb.points >= #wf_price mgs.data run return run function mgs:v5.1.0/zombies/deny/not_enough_points {score:"#wf_price",obj:"mgs.data"}
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
execute if score #pool_chosen mgs.data matches ..-1 run return run function mgs:v5.1.0/zombies/deny/message {msg:'{"translate":"mgs.you_already_own_every_available_perk_points_refunded","color":"yellow"}'}

# Decide whether this pull roams the machine (teddy bear) instead of granting a perk. Shared rule
# with the Mystery Box (roaming/roll_move): after WF_MOVE_THRESHOLD uses, 1-in-3 chance. Needs >=2
# placed spots to have somewhere to go.
scoreboard players add #wf_uses mgs.data 1
scoreboard players operation #roam_uses mgs.data = #wf_uses mgs.data
scoreboard players set #roam_threshold mgs.data 4
function mgs:v5.1.0/zombies/roaming/roll_move
scoreboard players operation #wf_will_move mgs.data = #roam_will_move mgs.data
execute store result score #wf_pos_count mgs.data run data get storage mgs:zombies game.map.wunderfizz
execute if score #wf_pos_count mgs.data matches ..1 run scoreboard players set #wf_will_move mgs.data 0
execute if score #wf_will_move mgs.data matches 1 run scoreboard players set #wf_uses mgs.data 0

# Spawn the spinning orb above the machine and stamp it
function mgs:v5.1.0/zombies/wunderfizz/spawn_orb
scoreboard players operation @n[tag=mgs.wf_orb_new] mgs.zb.wf.buyer = @s mgs.zb.wf_pid
scoreboard players operation @n[tag=mgs.wf_orb_new] mgs.zb.wf.perk = #pool_chosen mgs.data
scoreboard players operation @n[tag=mgs.wf_orb_new] mgs.zb.wf.paid = #wf_price mgs.data
scoreboard players operation @n[tag=mgs.wf_orb_new] mgs.zb.wf.willmove = #wf_will_move mgs.data
scoreboard players set @n[tag=mgs.wf_orb_new] mgs.zb.wf.anim 100
# Timeslip: this buyer's spin runs 2x faster (see orb_tick)
scoreboard players set @n[tag=mgs.wf_orb_new] mgs.zb.wf.timeslip 0
execute if score @s mgs.special.timeslip matches 1.. run scoreboard players set @n[tag=mgs.wf_orb_new] mgs.zb.wf.timeslip 1
tag @e[tag=mgs.wf_orb_new] remove mgs.wf_orb_new

playsound minecraft:block.conduit.activate ambient @a[scores={mgs.zb.in_game=1}] ~ ~ ~ 1.0 1.2
playsound minecraft:block.beacon.activate ambient @a[scores={mgs.zb.in_game=1}] ~ ~ ~ 0.6 1.6
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.der_wunderfizz_spinning","color":"gold"}]

