
#> mgs:v5.1.0/zombies/wunderfizz/setup_iter
#
# @within	mgs:v5.1.0/zombies/wunderfizz/setup
#			mgs:v5.1.0/zombies/wunderfizz/setup_iter
#

scoreboard players add #wf_counter mgs.data 1

# Relative -> absolute position
execute store result score #wfx mgs.data run data get storage mgs:temp _wf_iter[0].pos[0]
execute store result score #wfy mgs.data run data get storage mgs:temp _wf_iter[0].pos[1]
execute store result score #wfz mgs.data run data get storage mgs:temp _wf_iter[0].pos[2]
scoreboard players operation #wfx mgs.data += #gm_base_x mgs.data
scoreboard players operation #wfy mgs.data += #gm_base_y mgs.data
scoreboard players operation #wfz mgs.data += #gm_base_z mgs.data
execute store result storage mgs:temp _wf.x int 1 run scoreboard players get #wfx mgs.data
execute store result storage mgs:temp _wf.y int 1 run scoreboard players get #wfy mgs.data
execute store result storage mgs:temp _wf.z int 1 run scoreboard players get #wfz mgs.data
data modify storage mgs:temp _wf.rotation set from storage mgs:temp _wf_iter[0].rotation

# Summon interaction entity
function mgs:v5.1.0/zombies/wunderfizz/place_at with storage mgs:temp _wf

# Metadata on the interaction entity
scoreboard players operation @n[tag=mgs.wf_new] mgs.zb.wf.id = #wf_counter mgs.data
execute store result score @n[tag=mgs.wf_new] mgs.zb.wf.price run data get storage mgs:temp _wf_iter[0].price
execute store result score @n[tag=mgs.wf_new] mgs.zb.wf.power run data get storage mgs:temp _wf_iter[0].power
execute store result score @n[tag=mgs.wf_new] mgs.zb.wf.allperks run data get storage mgs:temp _wf_iter[0].all_perks

# Roam start-eligibility (default eligible when the field is absent, like the Mystery Box)
execute unless data storage mgs:temp _wf_iter[0].can_start_on run tag @n[tag=mgs.wf_new] add mgs.wf_can_start
data modify storage mgs:temp _wf_cso set value 0b
execute if data storage mgs:temp _wf_iter[0].can_start_on run data modify storage mgs:temp _wf_cso set from storage mgs:temp _wf_iter[0].can_start_on
execute if data storage mgs:temp {_wf_cso:1b} run tag @n[tag=mgs.wf_new] add mgs.wf_can_start

# Bookshelf events
execute as @n[tag=mgs.wf_new] run function #bs.interaction:on_right_click {run:"function mgs:v5.1.0/zombies/wunderfizz/on_right_click",executor:"source"}
execute as @n[tag=mgs.wf_new] run function #bs.interaction:on_hover {run:"function mgs:v5.1.0/zombies/wunderfizz/on_hover",executor:"source"}

# Machine display (perk-machine pipeline, custom Wunderfizz model unless the map overrode it).
# Summoned as the DEFAULT (disabled) model; sync_displays lights up the active one afterwards.
data modify storage mgs:temp _wf_disp.tag set value "mgs.wf_display"
data modify storage mgs:temp _wf_disp.item_id set value ""
data modify storage mgs:temp _wf_disp.item_model set value ""
data modify storage mgs:temp _wf_disp.yaw set value 0.0
execute if data storage mgs:temp _wf_iter[0].display_item run data modify storage mgs:temp _wf_disp.item_id set from storage mgs:temp _wf_iter[0].display_item
execute if data storage mgs:temp _wf_iter[0].item_model run data modify storage mgs:temp _wf_disp.item_model set from storage mgs:temp _wf_iter[0].item_model
execute if data storage mgs:temp _wf_disp{item_id:""} run data modify storage mgs:temp _wf_disp.item_id set value "minecraft:potion"
execute if data storage mgs:temp _wf_disp{item_model:""} run data modify storage mgs:temp _wf_disp.item_model set value "mgs:der_wunderfizz"
execute if data storage mgs:temp _wf_iter[0].rotation[0] run data modify storage mgs:temp _wf_disp.yaw set from storage mgs:temp _wf_iter[0].rotation[0]
execute as @n[tag=mgs.wf_new] at @s align xyz positioned ~.5 ~-.37 ~.5 positioned ^ ^ ^-0.49 run function mgs:v5.1.0/zombies/display/summon_machine_display with storage mgs:temp _wf_disp

# Link the freshly summoned display to this position id (there is exactly one unlinked display now)
scoreboard players operation @e[tag=mgs.wf_display,tag=!mgs.wf_linked] mgs.zb.wf.id = @n[tag=mgs.wf_new] mgs.zb.wf.id
tag @e[tag=mgs.wf_display,tag=!mgs.wf_linked] add mgs.wf_linked

execute as @n[tag=mgs.wf_new] at @s run tp @s ~ ~2 ~
tag @n[tag=mgs.wf_new] add mgs.wunderfizz_machine
tag @n[tag=mgs.wf_new] remove mgs.wf_new

data remove storage mgs:temp _wf_iter[0]
execute if data storage mgs:temp _wf_iter[0] run function mgs:v5.1.0/zombies/wunderfizz/setup_iter

