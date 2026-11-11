
#> mgs:v5.4.1/player/fx_reset
#
# @executed	as @a
#
# @within	mgs:v5.4.1/load/confirm_load [ as @a ]
#			mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/player/fx_after_death
#			mgs:v5.4.1/player/fx_after_rejoin
#			mgs:v5.4.1/zombies/start [ as @a[scores={mgs.zb.in_game=1}] ]
#			mgs:v5.4.1/zombies/stop [ as @a[scores={mgs.zb.in_game=1}] ]
#			mgs:v5.4.1/multiplayer/start [ as @a[scores={mgs.mp.in_game=1}] ]
#			mgs:v5.4.1/multiplayer/stop [ as @a[scores={mgs.mp.in_game=1}] ]
#			mgs:v5.4.1/missions/start [ as @a[scores={mgs.mi.in_game=1}] ]
#			mgs:v5.4.1/missions/stop [ as @a[scores={mgs.mi.in_game=1}] ]
#

scoreboard players set #hurt_was mgs.data 0
execute if score @s mgs.hurt_fx matches 1.. run scoreboard players operation #hurt_was mgs.data = @s mgs.hurt_fx
posteffect remove @s mgs:debug_clock
posteffect remove @s mgs:debug_depth
posteffect remove @s mgs:flash_0
posteffect remove @s mgs:flash_1
posteffect remove @s mgs:flash_zoom_0
posteffect remove @s mgs:flash_zoom_1
posteffect remove @s mgs:flash_pap_0
posteffect remove @s mgs:flash_pap_1
posteffect remove @s mgs:flash_pap_zoom_0
posteffect remove @s mgs:flash_pap_zoom_1
posteffect remove @s mgs:zoom_iron
posteffect remove @s mgs:zoom_acog
posteffect remove @s mgs:zoom_mk4
posteffect remove @s mgs:zoom_pu
posteffect remove @s mgs:zoom_pso
posteffect remove @s mgs:zoom_iron_out
posteffect remove @s mgs:zoom_acog_out
posteffect remove @s mgs:zoom_mk4_out
posteffect remove @s mgs:zoom_pu_out
posteffect remove @s mgs:zoom_pso_out
posteffect remove @s mgs:crosshair_0_0
posteffect remove @s mgs:crosshair_0_1
posteffect remove @s mgs:crosshair_0_2
posteffect remove @s mgs:crosshair_0_3
posteffect remove @s mgs:crosshair_0_4
posteffect remove @s mgs:crosshair_0_5
posteffect remove @s mgs:crosshair_1_0
posteffect remove @s mgs:crosshair_1_1
posteffect remove @s mgs:crosshair_1_2
posteffect remove @s mgs:crosshair_1_3
posteffect remove @s mgs:crosshair_1_4
posteffect remove @s mgs:crosshair_1_5
posteffect remove @s mgs:crosshair_2_0
posteffect remove @s mgs:crosshair_2_1
posteffect remove @s mgs:crosshair_2_2
posteffect remove @s mgs:crosshair_2_3
posteffect remove @s mgs:crosshair_2_4
posteffect remove @s mgs:crosshair_2_5
posteffect remove @s mgs:crosshair_3_0
posteffect remove @s mgs:crosshair_3_1
posteffect remove @s mgs:crosshair_3_2
posteffect remove @s mgs:crosshair_3_3
posteffect remove @s mgs:crosshair_3_4
posteffect remove @s mgs:crosshair_3_5
posteffect remove @s mgs:crosshair_4_0
posteffect remove @s mgs:crosshair_4_1
posteffect remove @s mgs:crosshair_4_2
posteffect remove @s mgs:crosshair_4_3
posteffect remove @s mgs:crosshair_4_4
posteffect remove @s mgs:crosshair_4_5
posteffect remove @s mgs:crosshair_5_0
posteffect remove @s mgs:crosshair_5_1
posteffect remove @s mgs:crosshair_5_2
posteffect remove @s mgs:crosshair_5_3
posteffect remove @s mgs:crosshair_5_4
posteffect remove @s mgs:crosshair_5_5
posteffect remove @s mgs:hurt_0_1
posteffect remove @s mgs:hurt_0_2
posteffect remove @s mgs:hurt_1_0
posteffect remove @s mgs:hurt_1_1
posteffect remove @s mgs:hurt_1_2
posteffect remove @s mgs:hurt_2_0
posteffect remove @s mgs:hurt_2_1
posteffect remove @s mgs:hurt_2_2
posteffect remove @s mgs:hit_dir_0_0
posteffect remove @s mgs:hit_dir_0_1
posteffect remove @s mgs:hit_dir_1_0
posteffect remove @s mgs:hit_dir_1_1
posteffect remove @s mgs:hit_dir_2_0
posteffect remove @s mgs:hit_dir_2_1
posteffect remove @s mgs:hit_dir_3_0
posteffect remove @s mgs:hit_dir_3_1
posteffect remove @s mgs:hit_dir_4_0
posteffect remove @s mgs:hit_dir_4_1
posteffect remove @s mgs:hit_dir_5_0
posteffect remove @s mgs:hit_dir_5_1
posteffect remove @s mgs:hit_dir_6_0
posteffect remove @s mgs:hit_dir_6_1
posteffect remove @s mgs:hit_dir_7_0
posteffect remove @s mgs:hit_dir_7_1
posteffect remove @s mgs:hit_dir_8_0
posteffect remove @s mgs:hit_dir_8_1
posteffect remove @s mgs:hit_dir_9_0
posteffect remove @s mgs:hit_dir_9_1
posteffect remove @s mgs:hit_dir_10_0
posteffect remove @s mgs:hit_dir_10_1
posteffect remove @s mgs:hit_dir_11_0
posteffect remove @s mgs:hit_dir_11_1
posteffect remove @s mgs:hit_dir_12_0
posteffect remove @s mgs:hit_dir_12_1
posteffect remove @s mgs:hit_dir_13_0
posteffect remove @s mgs:hit_dir_13_1
posteffect remove @s mgs:hit_dir_14_0
posteffect remove @s mgs:hit_dir_14_1
posteffect remove @s mgs:hit_dir_15_0
posteffect remove @s mgs:hit_dir_15_1
posteffect remove @s mgs:hit_dir_16_0
posteffect remove @s mgs:hit_dir_16_1
posteffect remove @s mgs:hit_dir_17_0
posteffect remove @s mgs:hit_dir_17_1
posteffect remove @s mgs:hit_dir_18_0
posteffect remove @s mgs:hit_dir_18_1
posteffect remove @s mgs:hit_dir_19_0
posteffect remove @s mgs:hit_dir_19_1
posteffect remove @s mgs:hit_dir_20_0
posteffect remove @s mgs:hit_dir_20_1
posteffect remove @s mgs:hit_dir_21_0
posteffect remove @s mgs:hit_dir_21_1
posteffect remove @s mgs:hit_dir_22_0
posteffect remove @s mgs:hit_dir_22_1
posteffect remove @s mgs:hit_dir_23_0
posteffect remove @s mgs:hit_dir_23_1
posteffect remove @s mgs:hit_dir_24_0
posteffect remove @s mgs:hit_dir_24_1
posteffect remove @s mgs:hit_dir_25_0
posteffect remove @s mgs:hit_dir_25_1
posteffect remove @s mgs:hit_dir_26_0
posteffect remove @s mgs:hit_dir_26_1
posteffect remove @s mgs:hit_dir_27_0
posteffect remove @s mgs:hit_dir_27_1
posteffect remove @s mgs:hit_dir_28_0
posteffect remove @s mgs:hit_dir_28_1
posteffect remove @s mgs:hit_dir_29_0
posteffect remove @s mgs:hit_dir_29_1
posteffect remove @s mgs:hit_dir_30_0
posteffect remove @s mgs:hit_dir_30_1
posteffect remove @s mgs:hit_dir_31_0
posteffect remove @s mgs:hit_dir_31_1
posteffect remove @s mgs:hit_dir_32_0
posteffect remove @s mgs:hit_dir_32_1
posteffect remove @s mgs:hit_dir_33_0
posteffect remove @s mgs:hit_dir_33_1
posteffect remove @s mgs:hit_dir_34_0
posteffect remove @s mgs:hit_dir_34_1
posteffect remove @s mgs:hit_dir_35_0
posteffect remove @s mgs:hit_dir_35_1
scoreboard players reset @s mgs.flash_id
scoreboard players reset @s mgs.flash_slot
scoreboard players reset @s mgs.flash_off
scoreboard players reset @s mgs.zoom_fx
scoreboard players reset @s mgs.zoom_fx_off
scoreboard players reset @s mgs.cross_from
scoreboard players reset @s mgs.cross_to
scoreboard players reset @s mgs.hurt_fx
scoreboard players reset @s mgs.hurt_from
scoreboard players reset @s mgs.hurt_pending
scoreboard players reset @s mgs.hurt_fall_until
scoreboard players reset @s mgs.hurt_out_until
scoreboard players reset @s mgs.hit_dir_sector
scoreboard players reset @s mgs.hit_dir_slot
scoreboard players reset @s mgs.hit_dir_off

# The red overlay fades out instead of vanishing
execute if score #hurt_was mgs.data matches 1.. run function mgs:v5.4.1/player/hurt_fade_out

