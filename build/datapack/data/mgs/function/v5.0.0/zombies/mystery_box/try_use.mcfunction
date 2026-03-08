
#> mgs:v5.0.0/zombies/mystery_box/try_use
#
# @executed	as @p[distance=..3,scores={mgs.zb.in_game=1}]
#
# @within	mgs:v5.0.0/zombies/mystery_box/on_interact [ as @p[distance=..3,scores={mgs.zb.in_game=1}] ]
#

# Check game is active
execute unless data storage mgs:zombies game{state:"active"} run return fail

# Check if box is already spinning
execute if data storage mgs:zombies mystery_box{spinning:true} run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.mystery_box_is_already_in_use","color":"red"}]

# Check if player has enough points
execute unless score @s mgs.zb.points >= #zb_mystery_box_price mgs.config run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.not_enough_points_950_required","color":"red"}]

# Deduct points
scoreboard players operation @s mgs.zb.points -= #zb_mystery_box_price mgs.config

# Store buyer UUID
data modify storage mgs:zombies mystery_box.buyer set from entity @s UUID

# Start spinning
data modify storage mgs:zombies mystery_box.spinning set value true

# Pick a random weapon from the pool
execute store result score #_mb_pool_size mgs.data run data get storage mgs:zombies mystery_box_pool
execute if score #_mb_pool_size mgs.data matches ..0 run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.mystery_box_pool_is_empty","color":"red"}]
execute store result score #_mb_pick mgs.data run random value 0..100
scoreboard players operation #_mb_pick mgs.data %= #_mb_pool_size mgs.data

# Copy pool and iterate to the picked index
data modify storage mgs:temp _mb_pool_iter set from storage mgs:zombies mystery_box_pool
function mgs:v5.0.0/zombies/mystery_box/pick_item

# Store the result
data modify storage mgs:zombies mystery_box.result set from storage mgs:temp _mb_pool_iter[0]

# Start animation timer (2 seconds = 40 ticks cycling + 3 seconds = 60 ticks display = 100 total)
scoreboard players set #mb_anim_timer mgs.data 40

# Spawn display entity at box position
execute at @e[tag=mgs.mystery_box_active,limit=1] run function mgs:v5.0.0/zombies/mystery_box/spawn_display

# Announce
tellraw @a[scores={mgs.zb.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.mystery_box_spinning","color":"light_purple"}]

