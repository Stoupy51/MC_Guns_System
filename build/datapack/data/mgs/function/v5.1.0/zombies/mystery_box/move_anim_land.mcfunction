
#> mgs:v5.1.0/zombies/mystery_box/move_anim_land
#
# @within	mgs:v5.1.0/zombies/mystery_box/move_anim_tick
#

execute as @n[tag=mgs.mystery_box_active] at @s as @e[tag=mgs.mb_presence,tag=!mgs.mb_temp] run tp @s ~ ~-0.9 ~

scoreboard players set #mb_move_timer mgs.data 0
data remove storage mgs:zombies mystery_box.result

# The old spot is now inactive: rebuild the grayed crates at every inactive spot.
function mgs:v5.1.0/zombies/mystery_box/refresh_disabled

# Unset when the spot has no name.
function mgs:v5.1.0/zombies/mystery_box/read_location_name

execute unless data storage mgs:zombies mystery_box.current_name run tellraw @a[scores={mgs.zb.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.the_mystery_box_has_arrived_at_a_new_location","color":"yellow"}]
execute if data storage mgs:zombies mystery_box.current_name run tellraw @a[scores={mgs.zb.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.the_mystery_box_has_arrived_at","color":"yellow"},{"storage":"mgs:zombies","nbt":"mystery_box.current_name","color":"gold","bold":true},"!"]
execute as @n[tag=mgs.mystery_box_active] at @s run playsound mgs:zombies/mystery_box/land ambient @a[scores={mgs.zb.in_game=1}] ~ ~ ~ 1.0 1.0

