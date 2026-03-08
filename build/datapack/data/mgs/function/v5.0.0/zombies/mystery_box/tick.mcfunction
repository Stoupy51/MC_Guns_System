
#> mgs:v5.0.0/zombies/mystery_box/tick
#
# @within	mgs:v5.0.0/zombies/game_tick
#

# Only tick if spinning
execute unless data storage mgs:zombies mystery_box{spinning:true} run return 0

# Decrement timer
scoreboard players remove #mb_anim_timer mgs.data 1

# Cycling phase (timer > 0): show random items
execute if score #mb_anim_timer mgs.data matches 1.. run function mgs:v5.0.0/zombies/mystery_box/cycle_display

# Landing phase (timer = 0): show the result
execute if score #mb_anim_timer mgs.data matches 0 run function mgs:v5.0.0/zombies/mystery_box/show_result

# Pickup window expired (timer = -60): remove display and reset
execute if score #mb_anim_timer mgs.data matches ..-60 run function mgs:v5.0.0/zombies/mystery_box/reset

