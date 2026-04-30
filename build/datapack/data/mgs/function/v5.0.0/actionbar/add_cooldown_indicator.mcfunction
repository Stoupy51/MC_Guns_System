
#> mgs:v5.0.0/actionbar/add_cooldown_indicator
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/actionbar/show
#

# Append cooldown indicator dot: green if ready, dark_red if on cooldown
execute if score @s mgs.cooldown <= #total_tick mgs.data run data modify storage mgs:temp actionbar.list append value {"text":" ● ","color":"green"}
execute if score @s mgs.cooldown > #total_tick mgs.data run data modify storage mgs:temp actionbar.list append value {"text":" ● ","color":"dark_red"}

