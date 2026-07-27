
#> mgs:v5.1.0/zombies/mystery_box/move_anim_land
#
# @within	mgs:v5.1.0/zombies/mystery_box/move_anim_tick
#

# Snap the descending chest (base + lid) to exact final position smoothly
execute as @n[tag=mgs.mystery_box_active] at @s as @e[tag=mgs.mb_presence,tag=!mgs.mb_temp] run tp @s ~ ~-0.9 ~

# Reset move state
scoreboard players set #mb_move_timer mgs.data 0
data remove storage mgs:zombies mystery_box.result

# The old active spot is now inactive: (re)build the grayed disabled crates at every inactive spot
function mgs:v5.1.0/zombies/mystery_box/refresh_disabled

# Resolve the new spot's editor-given name into mystery_box.current_name, unset when it has none
function mgs:v5.1.0/zombies/mystery_box/read_location_name

# Announce arrival, naming the place when the map maker gave this spot one
execute unless data storage mgs:zombies mystery_box.current_name run tellraw @a[scores={mgs.zb.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.the_mystery_box_has_arrived_at_a_new_location","color":"yellow"}]
execute if data storage mgs:zombies mystery_box.current_name run tellraw @a[scores={mgs.zb.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.the_mystery_box_has_arrived_at","color":"yellow"},{"storage":"mgs:zombies","nbt":"mystery_box.current_name","color":"gold","bold":true},"!"]
execute as @n[tag=mgs.mystery_box_active] at @s run playsound mgs:zombies/mystery_box/land ambient @a[scores={mgs.zb.in_game=1}] ~ ~ ~ 1.0 1.0

