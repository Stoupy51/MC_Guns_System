
#> mgs:v5.0.0/zombies/mystery_box/tick
#
# @within	mgs:v5.0.0/zombies/game_tick
#

# Spin animation tick
execute if data storage mgs:zombies mystery_box{spinning:true} run function mgs:v5.0.0/zombies/mystery_box/spin_tick

# Move animation tick (independent of spin)
execute if score #mb_move_timer mgs.data matches 1.. run function mgs:v5.0.0/zombies/mystery_box/move_anim_tick

