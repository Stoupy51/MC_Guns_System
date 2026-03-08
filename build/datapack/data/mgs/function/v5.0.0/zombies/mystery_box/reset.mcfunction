
#> mgs:v5.0.0/zombies/mystery_box/reset
#
# @within	mgs:v5.0.0/zombies/stop
#			mgs:v5.0.0/zombies/mystery_box/tick
#			mgs:v5.0.0/zombies/mystery_box/collect
#

# Kill display entity
kill @e[tag=mgs.mb_display]

# Reset state
data modify storage mgs:zombies mystery_box.spinning set value false
data modify storage mgs:zombies mystery_box.ready set value false
data remove storage mgs:zombies mystery_box.result

