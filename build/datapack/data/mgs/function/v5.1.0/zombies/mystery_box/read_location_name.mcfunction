
#> mgs:v5.1.0/zombies/mystery_box/read_location_name
#
# @within	mgs:v5.1.0/zombies/mystery_box/move_anim_land
#

# names[] is 0-based, box ids are 1-based
data remove storage mgs:zombies mystery_box.current_name
execute as @n[tag=mgs.mystery_box_active] run scoreboard players operation #mb_name_idx mgs.data = @s mgs.mb.box
scoreboard players remove #mb_name_idx mgs.data 1
execute store result storage mgs:temp _mb_name_idx.idx int 1 run scoreboard players get #mb_name_idx mgs.data
function mgs:v5.1.0/zombies/mystery_box/read_location_name_at with storage mgs:temp _mb_name_idx

# An unnamed spot stores "", which must read the same as having no name at all
execute if data storage mgs:zombies mystery_box{current_name:""} run data remove storage mgs:zombies mystery_box.current_name

