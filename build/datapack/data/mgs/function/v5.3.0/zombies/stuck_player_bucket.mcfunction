
#> mgs:v5.3.0/zombies/stuck_player_bucket
#
# @within	mgs:v5.3.0/dialog/close_then
#			mgs:v5.3.0/zombies/stuck_zombie_check [ as @a[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator,distance=..96] ]
#

execute at @s summon minecraft:marker run function mgs:v5.3.0/shared/probe_pos
execute store result score #zb_dx mgs.data run data get storage mgs:temp _probe_pos[0] 10
execute store result score #zb_dy mgs.data run data get storage mgs:temp _probe_pos[1] 10
execute store result score #zb_dz mgs.data run data get storage mgs:temp _probe_pos[2] 10
scoreboard players operation #zb_dx mgs.data -= #zb_px mgs.data
scoreboard players operation #zb_dy mgs.data -= #zb_py mgs.data
scoreboard players operation #zb_dz mgs.data -= #zb_pz mgs.data
scoreboard players operation #zb_dx mgs.data *= #zb_dx mgs.data
scoreboard players operation #zb_dy mgs.data *= #zb_dy mgs.data
scoreboard players operation #zb_dz mgs.data *= #zb_dz mgs.data
scoreboard players set #zb_nine mgs.data 9
scoreboard players operation #zb_dy mgs.data *= #zb_nine mgs.data
scoreboard players operation #zb_dx mgs.data += #zb_dz mgs.data
scoreboard players operation #zb_dx mgs.data += #zb_dy mgs.data

scoreboard players set #zb_pb mgs.data 4
execute if score #zb_dx mgs.data matches ..921600 run scoreboard players set #zb_pb mgs.data 3
execute if score #zb_dx mgs.data matches ..409600 run scoreboard players set #zb_pb mgs.data 2
execute if score #zb_dx mgs.data matches ..102400 run scoreboard players set #zb_pb mgs.data 1
execute if score #zb_dx mgs.data matches ..25600 run scoreboard players set #zb_pb mgs.data 0
execute if score #zb_dx mgs.data matches ..250000 run scoreboard players set #zb_near50 mgs.data 1
execute if score #zb_pb mgs.data < #cur_dist_bucket mgs.data run scoreboard players operation #cur_dist_bucket mgs.data = #zb_pb mgs.data

