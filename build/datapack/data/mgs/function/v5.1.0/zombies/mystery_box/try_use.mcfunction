
#> mgs:v5.1.0/zombies/mystery_box/try_use
#
# @executed	at @n[tag=bs.interaction.target]
#
# @within	mgs:v5.1.0/zombies/mystery_box/box_click
#

# Check if player has enough points
execute unless score @s mgs.zb.points >= #zb_mystery_box_price mgs.config run return run function mgs:v5.1.0/zombies/mystery_box/deny_not_enough_points

# Ensure at least a default pool exists.
function mgs:v5.1.0/zombies/mystery_box/ensure_default_pool

# Deduct points, then ensure this player has a stable id so the pull display can record them as
# its buyer (set on the display below). Supports several concurrent pulls by the same player.
scoreboard players operation @s mgs.zb.points -= #zb_mystery_box_price mgs.config
execute unless score @s mgs.mb.pid matches 1.. run function mgs:v5.1.0/zombies/mystery_box/assign_pid

# Pre-determine if the box will move (teddy bear) — only the active box, never during a Fire Sale
scoreboard players set #mb_will_move mgs.data 0
scoreboard players add #mb_pulls mgs.data 1
execute if score #mb_pulls mgs.data matches 4.. if entity @n[tag=bs.interaction.target,tag=mgs.mystery_box_active] store result score #mb_move_roll mgs.data run random value 0..2
execute if score #mb_pulls mgs.data matches 4.. if entity @n[tag=bs.interaction.target,tag=mgs.mystery_box_active] if score #mb_move_roll mgs.data matches 0 run scoreboard players set #mb_will_move mgs.data 1
execute if score #zb_fire_sale_timer mgs.data matches 1.. run scoreboard players set #mb_will_move mgs.data 0
execute if score #mb_will_move mgs.data matches 1 run scoreboard players set #mb_pulls mgs.data 0

# Spawn the pull display here and stamp it with the box id, animation timer, and will-move flag
function mgs:v5.1.0/zombies/mystery_box/spawn_display
scoreboard players operation @n[tag=mgs.mb_display_new] mgs.mb.box = #cur_box mgs.data
scoreboard players set @n[tag=mgs.mb_display_new] mgs.mb.anim 105
scoreboard players operation @n[tag=mgs.mb_display_new] mgs.mb.willmove = #mb_will_move mgs.data
scoreboard players operation @n[tag=mgs.mb_display_new] mgs.mb.buyer = @s mgs.mb.pid
tag @n[tag=mgs.mb_display_new] remove mgs.mb_display_new

# Open this box's lid + open/spin sounds + a private announce to the buyer
function mgs:v5.1.0/zombies/mystery_box/open_lid
function mgs:v5.1.0/zombies/feedback/sound_box_open
function mgs:v5.1.0/zombies/feedback/sound_box_spin
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.mystery_box_spinning","color":"light_purple"}]

