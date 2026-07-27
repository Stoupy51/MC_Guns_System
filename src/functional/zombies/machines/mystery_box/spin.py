""" The per-display spin: item cycling, the landing and the result baked onto the display. """
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_versioned_function

from ....helpers import MGS_TAG
from ...common import ZombiesCommon


# Functions
def write_mystery_box_spin() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	deny_all_owned: str = ZombiesCommon.deny_cmd(ns, version, '{"text":"You already own all available Mystery Box weapons. Points refunded.","color":"yellow"}')

	## Mystery box tick: each pull display advances independently, so multiple boxes can spin at once.
	write_versioned_function("zombies/mystery_box/tick", f"""
# Per-box spin animation (the moving bear display is excluded — the move handles it)
execute as @e[tag={ns}.mb_display,tag=!{ns}.mb_bear] at @s run function {ns}:v{version}/zombies/mystery_box/spin_tick_one

# Move animation tick (active box only; never during a Fire Sale)
execute if score #mb_move_timer {ns}.data matches 1.. run function {ns}:v{version}/zombies/mystery_box/move_anim_tick
""")

	## Per-display spin tick (@s = a pull display, never the moving bear)
	write_versioned_function("zombies/mystery_box/spin_tick_one", f"""
scoreboard players remove @s {ns}.mb.anim 1

# Timeslip: 2x spin speed. The extra -1 only fires inside the cycling phase (1..103), so the 104
# float-up trigger still runs; anim is even every tick after the first, so the doubled step always
# lands exactly on the anim==0 result and never overshoots into the reset window.
execute if score @s {ns}.mb.timeslip matches 1 if score @s {ns}.mb.anim matches 1..103 run scoreboard players remove @s {ns}.mb.anim 1

# Start the float-up one tick after spawn (avoids same-tick interpolation glitches)
execute if score @s {ns}.mb.anim matches 104 run data merge entity @s {{transformation:{{translation:[0f,0.8f,0f]}},start_interpolation:0,interpolation_duration:200}}

# Cycling phase (anim > 0): show random items with staged slowdown cadence
execute if score @s {ns}.mb.anim matches 1.. run function {ns}:v{version}/zombies/mystery_box/cycle_step_one

# Landing (anim == 0): decide + show the result
execute if score @s {ns}.mb.anim matches 0 run function {ns}:v{version}/zombies/mystery_box/show_result_one

# Pickup window expired (anim == -150): remove display and reset this box
execute if score @s {ns}.mb.anim matches ..-150 run function {ns}:v{version}/zombies/mystery_box/reset_one
""")

	## Cadence using the display's own anim timer (@s = display)
	write_versioned_function("zombies/mystery_box/cycle_step_one", f"""
scoreboard players set #mb_elapsed {ns}.data 80
scoreboard players operation #mb_elapsed {ns}.data -= @s {ns}.mb.anim
scoreboard players set #mb_c2 {ns}.data 2
scoreboard players set #mb_c5 {ns}.data 5
scoreboard players set #mb_c8 {ns}.data 8

scoreboard players operation #mb_mod {ns}.data = #mb_elapsed {ns}.data
execute if score #mb_elapsed {ns}.data matches ..29 run scoreboard players operation #mb_mod {ns}.data %= #mb_c2 {ns}.data
execute if score #mb_elapsed {ns}.data matches ..29 if score #mb_mod {ns}.data matches 0 run function {ns}:v{version}/zombies/mystery_box/cycle_display_one

scoreboard players operation #mb_mod {ns}.data = #mb_elapsed {ns}.data
execute if score #mb_elapsed {ns}.data matches 30..49 run scoreboard players operation #mb_mod {ns}.data %= #mb_c5 {ns}.data
execute if score #mb_elapsed {ns}.data matches 30..49 if score #mb_mod {ns}.data matches 0 run function {ns}:v{version}/zombies/mystery_box/cycle_display_one

scoreboard players operation #mb_mod {ns}.data = #mb_elapsed {ns}.data
execute if score #mb_elapsed {ns}.data matches 50.. run scoreboard players operation #mb_mod {ns}.data %= #mb_c8 {ns}.data
execute if score #mb_elapsed {ns}.data matches 50.. if score #mb_mod {ns}.data matches 0 run function {ns}:v{version}/zombies/mystery_box/cycle_display_one
""")

	## Cycle this display's item (@s = display)
	write_versioned_function("zombies/mystery_box/cycle_display_one", f"""
data modify storage bs:in random.weighted_choice.options set from storage {ns}:zombies mystery_box_pool
data modify storage bs:in random.weighted_choice.weights set from storage {ns}:zombies mystery_box_weights
function #bs.random:weighted_choice
data modify storage {ns}:temp _mb_cycle_item set from storage bs:out random.weighted_choice
execute if data storage {ns}:temp _mb_cycle_item.weapon_id run function {ns}:v{version}/zombies/mystery_box/cycle_display_weapon_one with storage {ns}:temp _mb_cycle_item
execute unless data storage {ns}:temp _mb_cycle_item.weapon_id run data modify entity @s item set from storage {ns}:temp _mb_cycle_item.display_item
""")

	write_versioned_function("zombies/mystery_box/cycle_display_weapon_one", f"""
$loot replace entity @s contents loot {ns}:i/$(weapon_id)
""")

	## Landing: decide + show the result for this pull (@s = display, positioned at the box)
	write_versioned_function("zombies/mystery_box/show_result_one", f"""
# Box will move (active box only): teddy bear path
execute if score @s {ns}.mb.willmove matches 1 run return run function {ns}:v{version}/zombies/mystery_box/show_bear_result

# Remember this box's id and buyer, then pick + reroll the result as its buyer
scoreboard players operation #this_box {ns}.data = @s {ns}.mb.box
scoreboard players operation #this_buyer {ns}.data = @s {ns}.mb.buyer
data remove storage {ns}:zombies mystery_box.result
scoreboard players set #mb_owned {ns}.data 0
execute as @a[scores={{{ns}.zb.in_game=1}}] if score @s {ns}.mb.pid = #this_buyer {ns}.data run function {ns}:v{version}/zombies/mystery_box/pick_for_buyer

# All owned / empty pool: refund the buyer and cancel this pull
execute if score #mb_owned {ns}.data matches 1 run function {ns}:v{version}/zombies/mystery_box/result_all_owned
execute if score #mb_owned {ns}.data matches 1 run return run function {ns}:v{version}/zombies/mystery_box/reset_one

# Set this display to the final weapon and bake the result onto it for collect
execute if data storage {ns}:zombies mystery_box.result.weapon_id run function {ns}:v{version}/zombies/mystery_box/show_result_weapon_one with storage {ns}:zombies mystery_box.result
execute unless data storage {ns}:zombies mystery_box.result.weapon_id run data modify entity @s item set from storage {ns}:zombies mystery_box.result.display_item
data modify entity @s item.components."minecraft:custom_data".{ns}.mb_result set from storage {ns}:zombies mystery_box.result

# Descend into place over 7.5s (150 ticks)
data merge entity @s {{transformation:{{translation:[0f,1.5f,0f]}}}}
data merge entity @s {{interpolation_duration:150,transformation:{{translation:[0f,0f,0f]}},start_interpolation:0}}

# Tell only the buyer it is ready
execute as @a[scores={{{ns}.zb.in_game=1}}] if score @s {ns}.mb.pid = #this_buyer {ns}.data run tellraw @s [{MGS_TAG},{{"text":"Mystery Box result ready! ","color":"light_purple"}},{{"text":"Right-click to collect!","color":"green","bold":true}}]
""")

	## Pick + reroll the result against the buyer's owned weapons (@s = the buyer)
	write_versioned_function("zombies/mystery_box/pick_for_buyer", f"""
function {ns}:v{version}/zombies/mystery_box/pick_random_result
scoreboard players set #mb_reroll {ns}.data 0
function {ns}:v{version}/zombies/mystery_box/reroll_owned
# Treat a missing result (empty pool / all owned after rerolls) as "owned" so we refund
execute unless data storage {ns}:zombies mystery_box.result.weapon_id run scoreboard players set #mb_owned {ns}.data 1
""")

	## Refund the buyer of this box (#this_buyer set by show_result_one) and notify them
	write_versioned_function("zombies/mystery_box/result_all_owned", f"""
execute as @a[scores={{{ns}.zb.in_game=1}}] if score @s {ns}.mb.pid = #this_buyer {ns}.data run scoreboard players operation @s {ns}.zb.points += #zb_mystery_box_price {ns}.config
execute as @a[scores={{{ns}.zb.in_game=1}}] if score @s {ns}.mb.pid = #this_buyer {ns}.data run {deny_all_owned}
""")

	write_versioned_function("zombies/mystery_box/show_result_weapon_one", f"""
$loot replace entity @s contents loot {ns}:i/$(weapon_id)
""")

