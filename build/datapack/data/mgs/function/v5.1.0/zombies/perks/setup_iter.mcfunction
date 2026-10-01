
#> mgs:v5.1.0/zombies/perks/setup_iter
#
# @within	mgs:v5.1.0/zombies/perks/setup
#			mgs:v5.1.0/zombies/perks/setup_iter
#

scoreboard players add #pk_counter mgs.data 1

execute store result score #pkx mgs.data run data get storage mgs:temp _pk_iter[0].pos[0]
execute store result score #pky mgs.data run data get storage mgs:temp _pk_iter[0].pos[1]
execute store result score #pkz mgs.data run data get storage mgs:temp _pk_iter[0].pos[2]
scoreboard players operation #pkx mgs.data += #gm_base_x mgs.data
scoreboard players operation #pky mgs.data += #gm_base_y mgs.data
scoreboard players operation #pkz mgs.data += #gm_base_z mgs.data

execute store result storage mgs:temp _pk.x int 1 run scoreboard players get #pkx mgs.data
execute store result storage mgs:temp _pk.y int 1 run scoreboard players get #pky mgs.data
execute store result storage mgs:temp _pk.z int 1 run scoreboard players get #pkz mgs.data
data modify storage mgs:temp _pk.rotation set from storage mgs:temp _pk_iter[0].rotation

function mgs:v5.1.0/zombies/perks/place_at with storage mgs:temp _pk

scoreboard players operation @n[tag=mgs.pk_new] mgs.zb.perk.id = #pk_counter mgs.data
execute store result score @n[tag=mgs.pk_new] mgs.zb.perk.price run data get storage mgs:temp _pk_iter[0].price
# Copied to a flat key first: `[0]{...}` after an index is invalid NBT path syntax.
data modify storage mgs:temp _pk_price.perk_id set from storage mgs:temp _pk_iter[0].perk_id
execute if score @n[tag=mgs.pk_new] mgs.zb.perk.price matches -1 if data storage mgs:temp _pk_price{perk_id:"juggernog"} run scoreboard players set @n[tag=mgs.pk_new] mgs.zb.perk.price 2500
execute if score @n[tag=mgs.pk_new] mgs.zb.perk.price matches -1 if data storage mgs:temp _pk_price{perk_id:"speed_cola"} run scoreboard players set @n[tag=mgs.pk_new] mgs.zb.perk.price 3000
execute if score @n[tag=mgs.pk_new] mgs.zb.perk.price matches -1 if data storage mgs:temp _pk_price{perk_id:"double_tap"} run scoreboard players set @n[tag=mgs.pk_new] mgs.zb.perk.price 2000
execute if score @n[tag=mgs.pk_new] mgs.zb.perk.price matches -1 if data storage mgs:temp _pk_price{perk_id:"quick_revive"} run scoreboard players set @n[tag=mgs.pk_new] mgs.zb.perk.price 1500
execute if score @n[tag=mgs.pk_new] mgs.zb.perk.price matches -1 if data storage mgs:temp _pk_price{perk_id:"mule_kick"} run scoreboard players set @n[tag=mgs.pk_new] mgs.zb.perk.price 4000
execute if score @n[tag=mgs.pk_new] mgs.zb.perk.price matches -1 if data storage mgs:temp _pk_price{perk_id:"stamin_up"} run scoreboard players set @n[tag=mgs.pk_new] mgs.zb.perk.price 2000
execute if score @n[tag=mgs.pk_new] mgs.zb.perk.price matches -1 if data storage mgs:temp _pk_price{perk_id:"phd_flopper"} run scoreboard players set @n[tag=mgs.pk_new] mgs.zb.perk.price 2000
execute if score @n[tag=mgs.pk_new] mgs.zb.perk.price matches -1 if data storage mgs:temp _pk_price{perk_id:"deadshot"} run scoreboard players set @n[tag=mgs.pk_new] mgs.zb.perk.price 1500
execute if score @n[tag=mgs.pk_new] mgs.zb.perk.price matches -1 if data storage mgs:temp _pk_price{perk_id:"timeslip"} run scoreboard players set @n[tag=mgs.pk_new] mgs.zb.perk.price 1500
execute if score @n[tag=mgs.pk_new] mgs.zb.perk.price matches -1 if data storage mgs:temp _pk_price{perk_id:"electric_cherry"} run scoreboard players set @n[tag=mgs.pk_new] mgs.zb.perk.price 2000
execute if score @n[tag=mgs.pk_new] mgs.zb.perk.price matches -1 if data storage mgs:temp _pk_price{perk_id:"tombstone"} run scoreboard players set @n[tag=mgs.pk_new] mgs.zb.perk.price 2000
execute if score @n[tag=mgs.pk_new] mgs.zb.perk.price matches -1 if data storage mgs:temp _pk_price{perk_id:"whos_who"} run scoreboard players set @n[tag=mgs.pk_new] mgs.zb.perk.price 2000
execute if score @n[tag=mgs.pk_new] mgs.zb.perk.price matches -1 if data storage mgs:temp _pk_price{perk_id:"dying_wish"} run scoreboard players set @n[tag=mgs.pk_new] mgs.zb.perk.price 2000
execute if score @n[tag=mgs.pk_new] mgs.zb.perk.price matches -1 if data storage mgs:temp _pk_price{perk_id:"widows_wine"} run scoreboard players set @n[tag=mgs.pk_new] mgs.zb.perk.price 4000
scoreboard players operation @n[tag=mgs.pk_new] mgs.zb.perk.base_price = @n[tag=mgs.pk_new] mgs.zb.perk.price
# Quick Revive machines get dynamic solo pricing.
data modify storage mgs:temp _pk_qr.perk_id set from storage mgs:temp _pk_iter[0].perk_id
execute if data storage mgs:temp _pk_qr{perk_id:"quick_revive"} run tag @n[tag=mgs.pk_new] add mgs.pk_quick_revive
# true is stored as 1b, so `data get` returns 1.
execute store result score @n[tag=mgs.pk_new] mgs.zb.perk.power run data get storage mgs:temp _pk_iter[0].power
# Maps saved before chip-in existed have no field: the failed read stores 0 (off).
execute store result score @n[tag=mgs.pk_new] mgs.zb.perk.partial run data get storage mgs:temp _pk_iter[0].partial_price

execute store result storage mgs:temp _pk_store.id int 1 run scoreboard players get #pk_counter mgs.data
data modify storage mgs:temp _pk_store.perk_id set from storage mgs:temp _pk_iter[0].perk_id
# A custom label is kept only when non-empty; otherwise the perk's display_name is used.
data remove storage mgs:temp _pk_store.name
data modify storage mgs:temp _pk_store.name set from storage mgs:temp _pk_iter[0].name
execute if data storage mgs:temp _pk_store{name:""} run data remove storage mgs:temp _pk_store.name
function mgs:v5.1.0/zombies/perks/store_data with storage mgs:temp _pk_store
execute if data storage mgs:temp _pk_store.name run function mgs:v5.1.0/zombies/perks/store_data_name with storage mgs:temp _pk_store

# Shared random-perk pool (power-up and Der Wunderfizz).
function mgs:v5.1.0/zombies/perks/pool/mark with storage mgs:temp _pk_store

execute as @n[tag=mgs.pk_new] run function #bs.interaction:on_right_click {run:"function mgs:v5.1.0/zombies/perks/on_right_click",executor:"source"}
execute as @n[tag=mgs.pk_new] run function #bs.interaction:on_hover {run:"function mgs:v5.1.0/zombies/perks/on_hover",executor:"source"}

# Potion by default; maps can override display_item and item_model.
data modify storage mgs:temp _pk_disp.tag set value "mgs.pk_display"
data modify storage mgs:temp _pk_disp.item_id set value ""
data modify storage mgs:temp _pk_disp.item_model set value ""
data modify storage mgs:temp _pk_disp.yaw set value 0.0
execute if data storage mgs:temp _pk_iter[0].display_item run data modify storage mgs:temp _pk_disp.item_id set from storage mgs:temp _pk_iter[0].display_item
execute if data storage mgs:temp _pk_iter[0].item_model run data modify storage mgs:temp _pk_disp.item_model set from storage mgs:temp _pk_iter[0].item_model
execute if data storage mgs:temp _pk_disp{item_id:""} run data modify storage mgs:temp _pk_disp.item_id set value "minecraft:potion"
execute if data storage mgs:temp _pk_disp{item_model:""} run data modify storage mgs:temp _pk_disp.item_model set value "minecraft:potion"

# Per-perk default machine models when the map set none. Other perks need a child model overriding accent and accent2
# (see perk_machine_juggernog.json) and a line here.
data modify storage mgs:temp _pk_disp.perk_id set from storage mgs:temp _pk_iter[0].perk_id
execute if data storage mgs:temp _pk_disp{item_model:"minecraft:potion"} run function mgs:v5.1.0/zombies/perks/override_perk_model with storage mgs:temp _pk_disp
execute if data storage mgs:temp _pk_iter[0].rotation[0] run data modify storage mgs:temp _pk_disp.yaw set from storage mgs:temp _pk_iter[0].rotation[0]
execute as @n[tag=mgs.pk_new] at @s align xyz positioned ~.5 ~-.37 ~.5 positioned ^ ^ ^-0.49 run function mgs:v5.1.0/zombies/display/summon_machine_display with storage mgs:temp _pk_disp
execute as @n[tag=mgs.pk_new] at @s run tp @s ~ ~2 ~
tag @n[tag=mgs.pk_new] add mgs.perk_machine
tag @n[tag=mgs.pk_new] remove mgs.pk_new

data remove storage mgs:temp _pk_iter[0]
execute if data storage mgs:temp _pk_iter[0] run function mgs:v5.1.0/zombies/perks/setup_iter

