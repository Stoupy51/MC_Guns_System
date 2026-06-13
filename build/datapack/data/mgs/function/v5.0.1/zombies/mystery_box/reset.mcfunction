
#> mgs:v5.0.1/zombies/mystery_box/reset
#
# @within	mgs:v5.0.1/zombies/stop
#			mgs:v5.0.1/zombies/mystery_box/spin_tick
#			mgs:v5.0.1/zombies/mystery_box/collect
#

# Close the lid
function mgs:v5.0.1/zombies/mystery_box/close_lid

# Kill display entity
kill @e[tag=mgs.mb_display]

# Reset state
data modify storage mgs:zombies mystery_box.spinning set value false
data modify storage mgs:zombies mystery_box.ready set value false
data remove storage mgs:zombies mystery_box.result

