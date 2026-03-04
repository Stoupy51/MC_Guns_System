
#> mgs:v5.0.0/multiplayer/my_loadouts/prep_btn
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/multiplayer/my_loadouts/build_list_favs
#			mgs:v5.0.0/multiplayer/my_loadouts/check_private_not_fav
#			mgs:v5.0.0/multiplayer/my_loadouts/check_public_not_fav
#

# Copy entry data for macro use (all stored fields come along)
data modify storage mgs:temp _btn_data set from storage mgs:temp _iter[0]

# Compute select trigger: 1000 + id
execute store result score #trig mgs.data run data get storage mgs:temp _iter[0].id
scoreboard players add #trig mgs.data 1000
execute store result storage mgs:temp _btn_data.select_trig int 1 run scoreboard players get #trig mgs.data

# Compute toggle visibility trigger: 1400 + id
execute store result score #trig mgs.data run data get storage mgs:temp _iter[0].id
scoreboard players add #trig mgs.data 1400
execute store result storage mgs:temp _btn_data.vis_trig int 1 run scoreboard players get #trig mgs.data

# Compute delete trigger: 1300 + id
execute store result score #trig mgs.data run data get storage mgs:temp _iter[0].id
scoreboard players add #trig mgs.data 1300
execute store result storage mgs:temp _btn_data.delete_trig int 1 run scoreboard players get #trig mgs.data

# Compute perks_count from perks list size
execute unless data storage mgs:temp _btn_data.perks run data modify storage mgs:temp _btn_data.perks set value []
execute store result storage mgs:temp _btn_data.perks_count int 1 run data get storage mgs:temp _btn_data.perks

# Normalize optional fields (backwards compat for pre-update loadouts)
execute unless data storage mgs:temp _btn_data.points_used run data modify storage mgs:temp _btn_data.points_used set value 0
execute unless data storage mgs:temp _btn_data.favorites_count run data modify storage mgs:temp _btn_data.favorites_count set value 0
execute unless data storage mgs:temp _btn_data.likes run data modify storage mgs:temp _btn_data.likes set value 0
execute unless data storage mgs:temp _btn_data.equip_slot1_name run data modify storage mgs:temp _btn_data.equip_slot1_name set value "?"
execute unless data storage mgs:temp _btn_data.equip_slot2_name run data modify storage mgs:temp _btn_data.equip_slot2_name set value "?"
execute unless data storage mgs:temp _btn_data.main_gun_display run data modify storage mgs:temp _btn_data.main_gun_display set from storage mgs:temp _btn_data.main_gun
execute unless data storage mgs:temp _btn_data.secondary_gun_display run data modify storage mgs:temp _btn_data.secondary_gun_display set value "None"

# Route to correct color variant based on public flag (green=public, red=private)
execute store result score #pub mgs.data run data get storage mgs:temp _iter[0].public
execute if score #pub mgs.data matches 1 run function mgs:v5.0.0/multiplayer/my_loadouts/add_btn_public with storage mgs:temp _btn_data
execute if score #pub mgs.data matches 0 run function mgs:v5.0.0/multiplayer/my_loadouts/add_btn_private with storage mgs:temp _btn_data

