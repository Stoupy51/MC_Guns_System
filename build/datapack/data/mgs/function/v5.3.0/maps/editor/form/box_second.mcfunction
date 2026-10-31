
#> mgs:v5.3.0/maps/editor/form/box_second
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.3.0/maps/editor/form/box_corner
#

tag @a[tag=mgs.coord_stick_user] remove mgs.cs_abox
execute unless entity @n[type=minecraft:marker,tag=mgs.ed_form_target] run return run tellraw @a[tag=mgs.coord_stick_user] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.the_spawn_being_edited_is_gone","fallback":"The spawn being edited is gone.","color":"red"}]

data modify storage mgs:temp _form_box set value [0,0,0,0,0,0]
execute store result score #cs_x1 mgs.data run data get storage mgs:temp coord_stick.abox[0]
scoreboard players operation #cs_x2 mgs.data = #cs_x1 mgs.data
scoreboard players operation #cs_x1 mgs.data < #cs_pos_x mgs.data
scoreboard players operation #cs_x2 mgs.data > #cs_pos_x mgs.data
scoreboard players operation #cs_x2 mgs.data -= #cs_x1 mgs.data
execute store result score #cs_tx mgs.data run data get entity @n[type=minecraft:marker,tag=mgs.ed_form_target] Pos[0]
scoreboard players operation #cs_x1 mgs.data -= #cs_tx mgs.data
execute store result storage mgs:temp _form_box[0] int 1 run scoreboard players get #cs_x1 mgs.data
execute store result storage mgs:temp _form_box[3] int 1 run scoreboard players get #cs_x2 mgs.data
execute store result score #cs_y1 mgs.data run data get storage mgs:temp coord_stick.abox[1]
scoreboard players operation #cs_y2 mgs.data = #cs_y1 mgs.data
scoreboard players operation #cs_y1 mgs.data < #cs_pos_y mgs.data
scoreboard players operation #cs_y2 mgs.data > #cs_pos_y mgs.data
scoreboard players operation #cs_y2 mgs.data -= #cs_y1 mgs.data
execute store result score #cs_ty mgs.data run data get entity @n[type=minecraft:marker,tag=mgs.ed_form_target] Pos[1]
scoreboard players operation #cs_y1 mgs.data -= #cs_ty mgs.data
execute store result storage mgs:temp _form_box[1] int 1 run scoreboard players get #cs_y1 mgs.data
execute store result storage mgs:temp _form_box[4] int 1 run scoreboard players get #cs_y2 mgs.data
execute store result score #cs_z1 mgs.data run data get storage mgs:temp coord_stick.abox[2]
scoreboard players operation #cs_z2 mgs.data = #cs_z1 mgs.data
scoreboard players operation #cs_z1 mgs.data < #cs_pos_z mgs.data
scoreboard players operation #cs_z2 mgs.data > #cs_pos_z mgs.data
scoreboard players operation #cs_z2 mgs.data -= #cs_z1 mgs.data
execute store result score #cs_tz mgs.data run data get entity @n[type=minecraft:marker,tag=mgs.ed_form_target] Pos[2]
scoreboard players operation #cs_z1 mgs.data -= #cs_tz mgs.data
execute store result storage mgs:temp _form_box[2] int 1 run scoreboard players get #cs_z1 mgs.data
execute store result storage mgs:temp _form_box[5] int 1 run scoreboard players get #cs_z2 mgs.data
data remove storage mgs:temp coord_stick.abox
data modify entity @n[type=minecraft:marker,tag=mgs.ed_form_target] data.activation_box set from storage mgs:temp _form_box
tellraw @a[tag=mgs.coord_stick_user] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.activation_box_set","fallback":"Activation box set: ","color":"green"},{"storage":"mgs:temp","nbt":"_form_box","color":"white"}]

# Back to the form, which now shows the box.
tag @a[tag=mgs.coord_stick_user] add mgs.ed_form_user
execute as @n[type=minecraft:marker,tag=mgs.ed_form_target] run function mgs:v5.3.0/maps/editor/form/reopen
tag @a remove mgs.ed_form_user

