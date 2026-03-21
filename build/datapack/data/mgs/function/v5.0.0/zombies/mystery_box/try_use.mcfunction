
#> mgs:v5.0.0/zombies/mystery_box/try_use
#
# @within	mgs:v5.0.0/zombies/mystery_box/on_right_click
#

# Check if player has enough points
execute unless score @s mgs.zb.points >= #zb_mystery_box_price mgs.config run return run function mgs:v5.0.0/zombies/mystery_box/deny_not_enough_points

# Ensure at least a default pool exists.
function mgs:v5.0.0/zombies/mystery_box/ensure_default_pool

# Deduct points
scoreboard players operation @s mgs.zb.points -= #zb_mystery_box_price mgs.config

# Start spinning
data modify storage mgs:zombies mystery_box.spinning set value true

# Pick a random weapon from the pool and reroll if player already owns it.
function mgs:v5.0.0/zombies/mystery_box/pick_random_result
scoreboard players set #mb_reroll mgs.data 0
function mgs:v5.0.0/zombies/mystery_box/reroll_owned

# If still owned after rerolls, refund and fail.
execute if score #mb_owned mgs.data matches 1 run scoreboard players operation @s mgs.zb.points += #zb_mystery_box_price mgs.config
execute if score #mb_owned mgs.data matches 1 run return run function mgs:v5.0.0/zombies/mystery_box/deny_all_owned

# Start animation timer (100 ticks cycling with slowdown + 150 ticks display window)
scoreboard players set #mb_anim_timer mgs.data 105

# Spawn display entity at box position
execute at @n[tag=mgs.mystery_box_active] run function mgs:v5.0.0/zombies/mystery_box/spawn_display

# Announce
tellraw @a[scores={mgs.zb.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.mystery_box_spinning","color":"light_purple"}]
function mgs:v5.0.0/zombies/feedback/sound_box_spin

