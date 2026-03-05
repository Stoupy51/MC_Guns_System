
#> mgs:v5.0.0/multiplayer/marketplace/prep_btn
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/multiplayer/marketplace/build_list_favs
#			mgs:v5.0.0/multiplayer/marketplace/build_list_rest
#			mgs:v5.0.0/multiplayer/marketplace/sort_build_list
#

# Copy entry data for macro use
data modify storage mgs:temp _btn_data set from storage mgs:temp _iter[0]

# Compute triggers
execute store result score #trig mgs.data run data get storage mgs:temp _iter[0].id
scoreboard players add #trig mgs.data 1000
execute store result storage mgs:temp _btn_data.select_trig int 1 run scoreboard players get #trig mgs.data
execute store result score #trig mgs.data run data get storage mgs:temp _iter[0].id
scoreboard players add #trig mgs.data 1200
execute store result storage mgs:temp _btn_data.like_trig int 1 run scoreboard players get #trig mgs.data
execute store result score #trig mgs.data run data get storage mgs:temp _iter[0].id
scoreboard players add #trig mgs.data 1100
execute store result storage mgs:temp _btn_data.fav_trig int 1 run scoreboard players get #trig mgs.data

# Normalize and compute perk display
execute unless data storage mgs:temp _btn_data.perks run data modify storage mgs:temp _btn_data.perks set value []
execute store result storage mgs:temp _btn_data.perks_count int 1 run data get storage mgs:temp _btn_data.perks
data modify storage mgs:temp _btn_data.perk0 set value ""
data modify storage mgs:temp _btn_data.perk1 set value ""
data modify storage mgs:temp _btn_data.perk2 set value ""
execute if data storage mgs:temp _btn_data{perks:["quick_reload"]} run data modify storage mgs:temp _btn_data.perk0 set value "\\n- Sleight of Hand"
execute if data storage mgs:temp _btn_data{perks:["quick_swap"]} run data modify storage mgs:temp _btn_data.perk1 set value "\\n- Fast Hands"
execute if data storage mgs:temp _btn_data{perks:["infinite_ammo"]} run data modify storage mgs:temp _btn_data.perk2 set value "\\n- Overkill"
execute unless data storage mgs:temp _btn_data.points_used run data modify storage mgs:temp _btn_data.points_used set value 0
execute unless data storage mgs:temp _btn_data.favorites_count run data modify storage mgs:temp _btn_data.favorites_count set value 0
execute unless data storage mgs:temp _btn_data.likes run data modify storage mgs:temp _btn_data.likes set value 0
execute unless data storage mgs:temp _btn_data.equip_slot1_name run data modify storage mgs:temp _btn_data.equip_slot1_name set value "?"
execute unless data storage mgs:temp _btn_data.equip_slot2_name run data modify storage mgs:temp _btn_data.equip_slot2_name set value "?"
execute unless data storage mgs:temp _btn_data.main_gun_display run data modify storage mgs:temp _btn_data.main_gun_display set from storage mgs:temp _btn_data.main_gun
execute unless data storage mgs:temp _btn_data.secondary_gun_display run data modify storage mgs:temp _btn_data.secondary_gun_display set value "None"
execute unless data storage mgs:temp _btn_data.owner_name run data modify storage mgs:temp _btn_data.owner_name set value "?"

# Add buttons to dialog
function mgs:v5.0.0/multiplayer/marketplace/add_btn with storage mgs:temp _btn_data

