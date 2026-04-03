
#> mgs:v5.0.0/zombies/mystery_box/move_active_position
#
# @executed	as @n[tag=mgs.mb_new]
#
# @within	mgs:v5.0.0/zombies/mystery_box/maybe_move_after_pull
#

# Need at least 2 positions to move.
execute store result score #mb_pos_count mgs.data run data get storage mgs:zombies game.map.mystery_box.positions
execute if score #mb_pos_count mgs.data matches ..1 run return 0

tag @e[tag=mgs.mystery_box_active] add mgs.mb_prev_active
tag @e[tag=mgs.mystery_box_active] remove mgs.mystery_box_active
execute as @n[tag=mgs.mystery_box_pos,tag=!mgs.mb_prev_active,sort=random] run tag @s add mgs.mystery_box_active
tag @e[tag=mgs.mb_prev_active] remove mgs.mb_prev_active

function mgs:v5.0.0/zombies/mystery_box/sync_presence_display

tellraw @a[scores={mgs.zb.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.mystery_box_moved","color":"yellow"}]
function mgs:v5.0.0/zombies/feedback/sound_announce

