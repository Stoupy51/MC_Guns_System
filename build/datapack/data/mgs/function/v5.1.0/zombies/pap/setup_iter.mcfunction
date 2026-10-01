
#> mgs:v5.1.0/zombies/pap/setup_iter
#
# @within	mgs:v5.1.0/zombies/pap/setup
#			mgs:v5.1.0/zombies/pap/setup_iter
#

scoreboard players add #pap_counter mgs.data 1

execute store result score #papx mgs.data run data get storage mgs:temp _pap_iter[0].pos[0]
execute store result score #papy mgs.data run data get storage mgs:temp _pap_iter[0].pos[1]
execute store result score #papz mgs.data run data get storage mgs:temp _pap_iter[0].pos[2]
scoreboard players operation #papx mgs.data += #gm_base_x mgs.data
scoreboard players operation #papy mgs.data += #gm_base_y mgs.data
scoreboard players operation #papz mgs.data += #gm_base_z mgs.data

execute store result storage mgs:temp _pap_place.x int 1 run scoreboard players get #papx mgs.data
execute store result storage mgs:temp _pap_place.y int 1 run scoreboard players get #papy mgs.data
execute store result storage mgs:temp _pap_place.z int 1 run scoreboard players get #papz mgs.data
data modify storage mgs:temp _pap_place.rotation set from storage mgs:temp _pap_iter[0].rotation

function mgs:v5.1.0/zombies/pap/place_at with storage mgs:temp _pap_place

scoreboard players operation @n[tag=mgs.pap_new] mgs.zb.pap.id = #pap_counter mgs.data
execute store result score @n[tag=mgs.pap_new] mgs.zb.pap.price run data get storage mgs:temp _pap_iter[0].price
execute store result score @n[tag=mgs.pap_new] mgs.zb.pap.power run data get storage mgs:temp _pap_iter[0].power

execute as @n[tag=mgs.pap_new] run function #bs.interaction:on_right_click {run:"function mgs:v5.1.0/zombies/pap/on_right_click",executor:"source"}
execute as @n[tag=mgs.pap_new] run function #bs.interaction:on_hover {run:"function mgs:v5.1.0/zombies/pap/on_hover",executor:"source"}

# -1 is idle.
scoreboard players set @n[tag=mgs.pap_new] mgs.pap_anim -1

# netherite_block by default; maps can override display_item and item_model.
data modify storage mgs:temp _pap_disp.tag set value "mgs.pap_display"
data modify storage mgs:temp _pap_disp.item_id set value ""
data modify storage mgs:temp _pap_disp.item_model set value ""
data modify storage mgs:temp _pap_disp.yaw set value 0.0
execute if data storage mgs:temp _pap_iter[0].display_item run data modify storage mgs:temp _pap_disp.item_id set from storage mgs:temp _pap_iter[0].display_item
execute if data storage mgs:temp _pap_iter[0].item_model run data modify storage mgs:temp _pap_disp.item_model set from storage mgs:temp _pap_iter[0].item_model
execute if data storage mgs:temp _pap_disp{item_id:""} run data modify storage mgs:temp _pap_disp.item_id set value "minecraft:netherite_block"
execute if data storage mgs:temp _pap_disp{item_model:""} run data modify storage mgs:temp _pap_disp.item_model set value "mgs:pack_a_punch"
execute if data storage mgs:temp _pap_iter[0].rotation[0] run data modify storage mgs:temp _pap_disp.yaw set from storage mgs:temp _pap_iter[0].rotation[0]
execute as @n[tag=mgs.pap_new] at @s positioned ^ ^ ^-0.49 positioned ~ ~-0.4 ~ run function mgs:v5.1.0/zombies/display/summon_machine_display with storage mgs:temp _pap_disp
execute as @n[tag=mgs.pap_new] at @s run tp @s ~ ~2 ~

execute store result storage mgs:temp _pap_store.id int 1 run scoreboard players get #pap_counter mgs.data
data modify storage mgs:temp _pap_store.name set value "Pack-a-Punch"
execute if data storage mgs:temp _pap_iter[0].name run data modify storage mgs:temp _pap_store.name set from storage mgs:temp _pap_iter[0].name
data modify storage mgs:temp _pap_store.display_tag set from storage mgs:temp _pap_disp.tag
data modify storage mgs:temp _pap_store.display_item_id set from storage mgs:temp _pap_disp.item_id
data modify storage mgs:temp _pap_store.display_item_model set from storage mgs:temp _pap_disp.item_model
data modify storage mgs:temp _pap_store.display_yaw set from storage mgs:temp _pap_disp.yaw
function mgs:v5.1.0/zombies/pap/store_data with storage mgs:temp _pap_store

tag @n[tag=mgs.pap_new] remove mgs.pap_new

data remove storage mgs:temp _pap_iter[0]
execute if data storage mgs:temp _pap_iter[0] run function mgs:v5.1.0/zombies/pap/setup_iter

