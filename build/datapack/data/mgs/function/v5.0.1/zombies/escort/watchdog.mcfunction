
#> mgs:v5.0.1/zombies/escort/watchdog
#
# @executed	as @e[tag=mgs.zb_escorted] & at @s
#
# @within	mgs:v5.0.1/zombies/escort/zombie_tick
#

execute store result score #zb_esc_x mgs.data run data get entity @s Pos[0]
execute store result score #zb_esc_z mgs.data run data get entity @s Pos[2]
scoreboard players set #zb_esc_moved mgs.data 0
execute unless score #zb_esc_x mgs.data = @s mgs.zb.stuck_x run scoreboard players set #zb_esc_moved mgs.data 1
execute unless score #zb_esc_z mgs.data = @s mgs.zb.stuck_z run scoreboard players set #zb_esc_moved mgs.data 1
scoreboard players operation @s mgs.zb.stuck_x = #zb_esc_x mgs.data
scoreboard players operation @s mgs.zb.stuck_z = #zb_esc_z mgs.data

# Moved a block since last second: reset the still counter and keep escorting
execute if score #zb_esc_moved mgs.data matches 1 run return run scoreboard players set @s mgs.zb.stuck_ticks 0

# Still in the same block: the trader is stuck too -> teleport-rescue fallback
scoreboard players add @s mgs.zb.stuck_ticks 1
execute if score @s mgs.zb.stuck_ticks matches 5.. run function mgs:v5.0.1/zombies/escort/give_up

