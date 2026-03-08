
#> mgs:v5.0.0/zombies/mystery_box/on_right_click
#
# @within	???
#

# Only respond if this is the active mystery box
execute unless entity @e[tag=bs.interaction.target,tag=mgs.mystery_box_active] run return fail

# Check game is active
execute unless data storage mgs:zombies game{state:"active"} run return fail

# If result is ready: collect
execute if data storage mgs:zombies mystery_box{ready:true} run return run function mgs:v5.0.0/zombies/mystery_box/collect

# If already spinning: inform player
execute if data storage mgs:zombies mystery_box{spinning:true} run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.mystery_box_is_already_in_use","color":"red"}]

# Otherwise: try to use (buy)
function mgs:v5.0.0/zombies/mystery_box/try_use

