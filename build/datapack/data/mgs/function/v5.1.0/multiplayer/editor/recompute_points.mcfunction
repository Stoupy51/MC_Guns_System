
#> mgs:v5.1.0/multiplayer/editor/recompute_points
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/multiplayer/editor/commit_check
#			mgs:v5.1.0/multiplayer/editor/hub
#			mgs:v5.1.0/multiplayer/editor/show_primary_dialog
#			mgs:v5.1.0/multiplayer/editor/show_secondary_pistol_dialog
#			mgs:v5.1.0/multiplayer/editor/show_secondary_overkill_dialog
#			mgs:v5.1.0/multiplayer/editor/show_scope_primary_full
#			mgs:v5.1.0/multiplayer/editor/show_scope_primary_no4
#			mgs:v5.1.0/multiplayer/editor/show_scope_primary_1only
#			mgs:v5.1.0/multiplayer/editor/show_scope_secondary_4only
#			mgs:v5.1.0/multiplayer/editor/show_primary_camo_dialog
#			mgs:v5.1.0/multiplayer/editor/show_secondary_camo_dialog
#			mgs:v5.1.0/multiplayer/editor/show_equip1_camo_dialog
#			mgs:v5.1.0/multiplayer/editor/show_equip2_camo_dialog
#			mgs:v5.1.0/multiplayer/editor/show_primary_mags_dialog
#			mgs:v5.1.0/multiplayer/editor/show_secondary_mags_dialog
#			mgs:v5.1.0/multiplayer/editor/show_equip_slot1_dialog
#			mgs:v5.1.0/multiplayer/editor/show_equip_slot2_dialog
#			mgs:v5.1.0/multiplayer/editor/show_perks_dialog
#			mgs:v5.1.0/multiplayer/editor/save
#

scoreboard players set #lc_cost mgs.data 0
execute unless data storage mgs:temp editor{primary:""} run scoreboard players add #lc_cost mgs.data 1
execute unless data storage mgs:temp editor{primary:""} unless data storage mgs:temp editor{primary_scope:""} run scoreboard players add #lc_cost mgs.data 1
execute unless data storage mgs:temp editor{primary:""} store result score #lc_t mgs.data run data get storage mgs:temp editor.primary_mag_count 1
execute unless data storage mgs:temp editor{primary:""} run scoreboard players operation #lc_cost mgs.data += #lc_t mgs.data
execute unless data storage mgs:temp editor{secondary:""} run scoreboard players add #lc_cost mgs.data 1
execute unless data storage mgs:temp editor{secondary:""} unless data storage mgs:temp editor{secondary_scope:""} run scoreboard players add #lc_cost mgs.data 1
execute unless data storage mgs:temp editor{secondary:""} store result score #lc_t mgs.data run data get storage mgs:temp editor.secondary_mag_count 1
execute unless data storage mgs:temp editor{secondary:""} run scoreboard players operation #lc_cost mgs.data += #lc_t mgs.data
execute unless data storage mgs:temp editor{equip_slot1:""} run scoreboard players add #lc_cost mgs.data 1
execute unless data storage mgs:temp editor{equip_slot2:""} run scoreboard players add #lc_cost mgs.data 1
execute store result score #lc_t mgs.data run data get storage mgs:temp editor.perks 1
scoreboard players operation #lc_cost mgs.data += #lc_t mgs.data
scoreboard players set @s mgs.mp.edit_points 10
scoreboard players operation @s mgs.mp.edit_points -= #lc_cost mgs.data

