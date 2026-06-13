
#> mgs:v5.0.1/zombies/mystery_box/move_anim_land
#
# @within	mgs:v5.0.1/zombies/mystery_box/move_anim_tick
#

# Snap the descending chest (base + lid) to exact final position smoothly
execute as @n[tag=mgs.mystery_box_active] at @s as @e[tag=mgs.mb_presence] run tp @s ~ ~-0.9 ~

# Reset move state
scoreboard players set #mb_move_timer mgs.data 0
data remove storage mgs:zombies mystery_box.result

# Announce arrival
tellraw @a[scores={mgs.zb.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.the_mystery_box_has_arrived_at_a_new_location","color":"yellow"}]
execute as @n[tag=mgs.mystery_box_active] at @s run function mgs:v5.0.1/zombies/feedback/sound_box_land

