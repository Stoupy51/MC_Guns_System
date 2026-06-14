
#> mgs:v5.0.1/zombies/mystery_box/reset_one
#
# @executed	as @e[tag=...] & at @s
#
# @within	mgs:v5.0.1/zombies/mystery_box/spin_tick_one
#			mgs:v5.0.1/zombies/mystery_box/show_result_one
#

# Close this box's lid
function mgs:v5.0.1/zombies/mystery_box/close_lid

# Clear any buyer still pointing at this box
scoreboard players operation #this_box mgs.data = @s mgs.mb.box
execute as @a[scores={mgs.zb.in_game=1}] if score @s mgs.mb.buying = #this_box mgs.data run scoreboard players set @s mgs.mb.buying 0

# Remove the display
kill @s

# If a Fire Sale ended while pulls were in progress, finish temp-box cleanup once none remain
execute if score #mb_fs_cleanup_pending mgs.data matches 1 unless entity @e[tag=mgs.mb_display] run function mgs:v5.0.1/zombies/mystery_box/fire_sale_cleanup

