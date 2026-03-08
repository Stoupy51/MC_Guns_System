
#> mgs:v5.0.0/zombies/mystery_box/try_use
#
# @within	mgs:v5.0.0/zombies/mystery_box/on_right_click
#

# Check if player has enough points
execute unless score @s mgs.zb.points >= #zb_mystery_box_price mgs.config run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.not_enough_points_950_required","color":"red"}]

# Deduct points
scoreboard players operation @s mgs.zb.points -= #zb_mystery_box_price mgs.config

# Start spinning
data modify storage mgs:zombies mystery_box.spinning set value true

# Pick a random weapon from the pool
execute store result score #mb_pool_size mgs.data run data get storage mgs:zombies mystery_box_pool
execute if score #mb_pool_size mgs.data matches ..0 run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.mystery_box_pool_is_empty","color":"red"}]
execute store result score #mb_pick mgs.data run random value 0..100
scoreboard players operation #mb_pick mgs.data %= #mb_pool_size mgs.data

# Copy pool and iterate to the picked index
data modify storage mgs:temp _mb_pool_iter set from storage mgs:zombies mystery_box_pool
function mgs:v5.0.0/zombies/mystery_box/pick_item

# Store the result
data modify storage mgs:zombies mystery_box.result set from storage mgs:temp _mb_pool_iter[0]

# Start animation timer (40 ticks cycling + 60 ticks display = 100 total)
scoreboard players set #mb_anim_timer mgs.data 40

# Spawn display entity at box position
execute at @n[tag=mgs.mystery_box_active] run function mgs:v5.0.0/zombies/mystery_box/spawn_display

# Announce
tellraw @a[scores={mgs.zb.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.mystery_box_spinning","color":"light_purple"}]

