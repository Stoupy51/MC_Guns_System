
#> mgs:v5.1.0/multiplayer/my_loadouts/manage_prep
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/multiplayer/my_loadouts/manage_find
#

data modify storage mgs:temp _btn_data set from storage mgs:temp _find_iter[0]
scoreboard players operation #trig mgs.data = #loadout_id mgs.data
scoreboard players add #trig mgs.data 10000
execute store result storage mgs:temp _btn_data.select_trig int 1 run scoreboard players get #trig mgs.data
scoreboard players operation #trig mgs.data = #loadout_id mgs.data
scoreboard players add #trig mgs.data 70000
execute store result storage mgs:temp _btn_data.edit_trig int 1 run scoreboard players get #trig mgs.data
scoreboard players operation #trig mgs.data = #loadout_id mgs.data
scoreboard players add #trig mgs.data 50000
execute store result storage mgs:temp _btn_data.vis_trig int 1 run scoreboard players get #trig mgs.data
scoreboard players operation #trig mgs.data = #loadout_id mgs.data
scoreboard players add #trig mgs.data 40000
execute store result storage mgs:temp _btn_data.delete_trig int 1 run scoreboard players get #trig mgs.data
scoreboard players operation #trig mgs.data = #loadout_id mgs.data
scoreboard players add #trig mgs.data 60000
execute store result storage mgs:temp _btn_data.default_trig int 1 run scoreboard players get #trig mgs.data
execute unless data storage mgs:temp _btn_data.perks run data modify storage mgs:temp _btn_data.perks set value []
execute store result storage mgs:temp _btn_data.perks_count int 1 run data get storage mgs:temp _btn_data.perks
data modify storage mgs:temp _btn_data.perk0 set value ""
data modify storage mgs:temp _btn_data.perk1 set value ""
data modify storage mgs:temp _btn_data.perk2 set value ""
data modify storage mgs:temp _btn_data.perk3 set value ""
data modify storage mgs:temp _btn_data.perk4 set value ""
data modify storage mgs:temp _btn_data.perk5 set value ""
data modify storage mgs:temp _btn_data.perk6 set value ""
data modify storage mgs:temp _btn_data.perk7 set value ""
data modify storage mgs:temp _btn_data.perk8 set value ""
execute if data storage mgs:temp _btn_data{perks:["quick_reload"]} run data modify storage mgs:temp _btn_data.perk0 set value "\\n- Sleight of Hand"
execute if data storage mgs:temp _btn_data{perks:["quick_swap"]} run data modify storage mgs:temp _btn_data.perk1 set value "\\n- Fast Hands"
execute if data storage mgs:temp _btn_data{perks:["juggernaut"]} run data modify storage mgs:temp _btn_data.perk2 set value "\\n- Juggernaut"
execute if data storage mgs:temp _btn_data{perks:["scavenger"]} run data modify storage mgs:temp _btn_data.perk3 set value "\\n- Scavenger"
execute if data storage mgs:temp _btn_data{perks:["flak_jacket"]} run data modify storage mgs:temp _btn_data.perk4 set value "\\n- Flak Jacket"
execute if data storage mgs:temp _btn_data{perks:["tracker"]} run data modify storage mgs:temp _btn_data.perk5 set value "\\n- Tracker"
execute if data storage mgs:temp _btn_data{perks:["tactical_mask"]} run data modify storage mgs:temp _btn_data.perk6 set value "\\n- Tactical Mask"
execute if data storage mgs:temp _btn_data{perks:["overkill"]} run data modify storage mgs:temp _btn_data.perk7 set value "\\n- Overkill"
execute if data storage mgs:temp _btn_data{perks:["quick_fix"]} run data modify storage mgs:temp _btn_data.perk8 set value "\\n- Quick Fix"
execute unless data storage mgs:temp _btn_data.points_used run data modify storage mgs:temp _btn_data.points_used set value 0
execute unless data storage mgs:temp _btn_data.favorites_count run data modify storage mgs:temp _btn_data.favorites_count set value 0
execute unless data storage mgs:temp _btn_data.likes run data modify storage mgs:temp _btn_data.likes set value 0
execute unless data storage mgs:temp _btn_data.primary_mag_count run data modify storage mgs:temp _btn_data.primary_mag_count set value 1
execute unless data storage mgs:temp _btn_data.secondary_mag_count run data modify storage mgs:temp _btn_data.secondary_mag_count set value 0
execute unless data storage mgs:temp _btn_data.equip_slot1_name run data modify storage mgs:temp _btn_data.equip_slot1_name set value "?"
execute unless data storage mgs:temp _btn_data.equip_slot2_name run data modify storage mgs:temp _btn_data.equip_slot2_name set value "?"
execute unless data storage mgs:temp _btn_data.main_gun_display run data modify storage mgs:temp _btn_data.main_gun_display set from storage mgs:temp _btn_data.main_gun
execute unless data storage mgs:temp _btn_data.secondary_gun_display run data modify storage mgs:temp _btn_data.secondary_gun_display set value "None"
execute store result score #pub mgs.data run data get storage mgs:temp _find_iter[0].public
execute if score #pub mgs.data matches 1 run function mgs:v5.1.0/multiplayer/my_loadouts/manage_build_public with storage mgs:temp _btn_data
execute if score #pub mgs.data matches 0 run function mgs:v5.1.0/multiplayer/my_loadouts/manage_build_private with storage mgs:temp _btn_data

