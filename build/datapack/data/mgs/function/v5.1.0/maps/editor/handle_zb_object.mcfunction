
#> mgs:v5.1.0/maps/editor/handle_zb_object
#
# @executed	as @n[tag=mgs.new_element] & at @s
#
# @within	mgs:v5.1.0/maps/editor/process_element
#

execute store result storage mgs:temp _zbpos.x double 1 run data get entity @s Pos[0]
execute store result storage mgs:temp _zbpos.y double 1 run data get entity @s Pos[1]
execute store result storage mgs:temp _zbpos.z double 1 run data get entity @s Pos[2]

execute if entity @s[tag=mgs.element.zombie_spawn] run data modify storage mgs:temp _zbpos.tag set value "mgs.element.zombie_spawn"
execute if entity @s[tag=mgs.element.zombie_spawn] run data modify storage mgs:temp _zb_new set from storage mgs:temp map_edit.zb_defaults.zombie_spawn
execute if entity @s[tag=mgs.element.player_spawn_zb] run data modify storage mgs:temp _zbpos.tag set value "mgs.element.player_spawn_zb"
execute if entity @s[tag=mgs.element.player_spawn_zb] run data modify storage mgs:temp _zb_new set from storage mgs:temp map_edit.zb_defaults.player_spawn_zb
execute if entity @s[tag=mgs.element.special_spawn] run data modify storage mgs:temp _zbpos.tag set value "mgs.element.special_spawn"
execute if entity @s[tag=mgs.element.special_spawn] run data modify storage mgs:temp _zb_new set from storage mgs:temp map_edit.zb_defaults.special_spawn
execute if entity @s[tag=mgs.element.wallbuy] run data modify storage mgs:temp _zbpos.tag set value "mgs.element.wallbuy"
execute if entity @s[tag=mgs.element.wallbuy] run data modify storage mgs:temp _zb_new set from storage mgs:temp map_edit.zb_defaults.wallbuy
execute if entity @s[tag=mgs.element.door] run data modify storage mgs:temp _zbpos.tag set value "mgs.element.door"
execute if entity @s[tag=mgs.element.door] run data modify storage mgs:temp _zb_new set from storage mgs:temp map_edit.zb_defaults.door
execute if entity @s[tag=mgs.element.trap] run data modify storage mgs:temp _zbpos.tag set value "mgs.element.trap"
execute if entity @s[tag=mgs.element.trap] run data modify storage mgs:temp _zb_new set from storage mgs:temp map_edit.zb_defaults.trap
execute if entity @s[tag=mgs.element.perk_machine] run data modify storage mgs:temp _zbpos.tag set value "mgs.element.perk_machine"
execute if entity @s[tag=mgs.element.perk_machine] run data modify storage mgs:temp _zb_new set from storage mgs:temp map_edit.zb_defaults.perk_machine
execute if entity @s[tag=mgs.element.wunderfizz] run data modify storage mgs:temp _zbpos.tag set value "mgs.element.wunderfizz"
execute if entity @s[tag=mgs.element.wunderfizz] run data modify storage mgs:temp _zb_new set from storage mgs:temp map_edit.zb_defaults.wunderfizz
execute if entity @s[tag=mgs.element.pap_machine] run data modify storage mgs:temp _zbpos.tag set value "mgs.element.pap_machine"
execute if entity @s[tag=mgs.element.pap_machine] run data modify storage mgs:temp _zb_new set from storage mgs:temp map_edit.zb_defaults.pap_machine
execute if entity @s[tag=mgs.element.mystery_box_pos] run data modify storage mgs:temp _zbpos.tag set value "mgs.element.mystery_box_pos"
execute if entity @s[tag=mgs.element.mystery_box_pos] run data modify storage mgs:temp _zb_new set from storage mgs:temp map_edit.zb_defaults.mystery_box_pos
execute if entity @s[tag=mgs.element.power_switch] run data modify storage mgs:temp _zbpos.tag set value "mgs.element.power_switch"
execute if entity @s[tag=mgs.element.power_switch] run data modify storage mgs:temp _zb_new set from storage mgs:temp map_edit.zb_defaults.power_switch
execute if entity @s[tag=mgs.element.barricade] run data modify storage mgs:temp _zbpos.tag set value "mgs.element.barricade"
execute if entity @s[tag=mgs.element.barricade] run data modify storage mgs:temp _zb_new set from storage mgs:temp map_edit.zb_defaults.barricade

function mgs:v5.1.0/maps/editor/summon_zb_marker with storage mgs:temp _zbpos

execute as @n[tag=mgs.new_zb_marker] run data modify entity @s data set from storage mgs:temp _zb_new

execute as @n[tag=mgs.new_zb_marker] run data modify entity @s data.group_id set from storage mgs:temp map_edit.zb_defaults.group_id

execute store result score #yaw mgs.data run data get entity @p[tag=mgs.map_editor,distance=..6,sort=nearest] Rotation[0]

# The power switch sits on a block face, so it snaps to 90°; other objects to 45°.
# 742 = 720 + 45/2 and 765 = 720 + 90/2 make the value positive for rounding; the 720 is removed after.
execute unless entity @s[tag=mgs.element.power_switch] run scoreboard players add #yaw mgs.data 742
execute unless entity @s[tag=mgs.element.power_switch] run scoreboard players operation #yaw mgs.data /= #45 mgs.data
execute unless entity @s[tag=mgs.element.power_switch] run scoreboard players operation #yaw mgs.data *= #45 mgs.data
execute if entity @s[tag=mgs.element.power_switch] run scoreboard players add #yaw mgs.data 765
execute if entity @s[tag=mgs.element.power_switch] run scoreboard players operation #yaw mgs.data /= #90 mgs.data
execute if entity @s[tag=mgs.element.power_switch] run scoreboard players operation #yaw mgs.data *= #90 mgs.data
scoreboard players remove #yaw mgs.data 720

# +180°
scoreboard players add #yaw mgs.data 180

# The entity Rotation is synced at once, so the model display below is oriented right away.
execute as @n[tag=mgs.new_zb_marker] store result entity @s data.yaw float 1 run scoreboard players get #yaw mgs.data
execute as @n[tag=mgs.new_zb_marker] run data modify entity @s Rotation[0] set from entity @s data.yaw

# Doors take their block from the player's offhand (required).
execute if entity @s[tag=mgs.element.door] as @p[tag=mgs.map_editor,distance=..6,sort=nearest] run data modify storage mgs:temp _zb_offhand_block set from entity @s equipment.offhand.id
execute if entity @s[tag=mgs.element.door] unless data storage mgs:temp _zb_offhand_block run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"text":"⚠ ","color":"white"},{"translate":"mgs.door_cancelled_hold_a_block_in_offhand","color":"red"}]
execute if entity @s[tag=mgs.element.door] unless data storage mgs:temp _zb_offhand_block run kill @e[tag=mgs.new_zb_marker]
execute if entity @s[tag=mgs.element.door] unless data storage mgs:temp _zb_offhand_block run return fail
execute if entity @s[tag=mgs.element.door] as @n[tag=mgs.new_zb_marker] run data modify entity @s data.block set from storage mgs:temp _zb_offhand_block
data remove storage mgs:temp _zb_offhand_block

tag @e[tag=mgs.new_zb_marker] remove mgs.new_zb_marker

# Wallbuy, perk, PaP, mystery box and power switch displays.
function mgs:v5.1.0/maps/editor/refresh_displays

execute if entity @s[tag=mgs.element.zombie_spawn] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.zombie_spawn_placed","color":"dark_green"}]
execute if entity @s[tag=mgs.element.player_spawn_zb] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.player_spawn_placed","color":"aqua"}]
execute if entity @s[tag=mgs.element.special_spawn] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.special_spawn_placed","color":"dark_red"}]
execute if entity @s[tag=mgs.element.wallbuy] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.wallbuy_placed","color":"yellow"}]
execute if entity @s[tag=mgs.element.door] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.door_placed","color":"gold"}]
execute if entity @s[tag=mgs.element.trap] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.trap_placed","color":"red"}]
execute if entity @s[tag=mgs.element.perk_machine] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.perk_machine_placed","color":"dark_purple"}]
execute if entity @s[tag=mgs.element.wunderfizz] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.der_wunderfizz_placed","color":"gold"}]
execute if entity @s[tag=mgs.element.pap_machine] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.pack_a_punch_placed","color":"dark_red"}]
execute if entity @s[tag=mgs.element.mystery_box_pos] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.mystery_box_pos_placed","color":"light_purple"}]
execute if entity @s[tag=mgs.element.power_switch] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.power_switch_placed","color":"green"}]
execute if entity @s[tag=mgs.element.barricade] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.barricade_placed","color":"aqua"}]

