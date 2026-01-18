
#> mgs:v5.0.0/ammo/show_action_bar
#
# @executed	as @a[sort=random] & at @s
#
# @within	mgs:v5.0.0/player/tick
#

# Get capacity
execute store result score #capacity mgs.data run data get storage mgs:gun all.stats.capacity

# Get remaining
execute store result score #remaining mgs.data run scoreboard players get @s mgs.remaining_bullets

# Initialize actionbar
data modify storage mgs:temp actionbar set value {list:[]}

# Check if capacity > 15
execute if score #capacity mgs.data matches 16.. run data modify storage mgs:temp actionbar.list append value {"score":{"name":"#remaining","objective":"mgs.data"},"color":"#c24a17"}
execute if score #capacity mgs.data matches 16.. run data modify storage mgs:temp actionbar.list append value {"text":"x "}
execute if score #capacity mgs.data matches 16.. run data modify storage mgs:temp actionbar.list append value {"text":"A","font":"mgs:icons","shadow_color":[0,0,0,0],"color":"white"}
execute if score #capacity mgs.data matches 16.. run data modify storage mgs:temp actionbar.list append value {"text":" / ","color":"#c77e36"}
execute if score #capacity mgs.data matches 16.. run data modify storage mgs:temp actionbar.list append value {"score":{"name":"#capacity","objective":"mgs.data"}}
execute if score #capacity mgs.data matches 16.. run data modify storage mgs:temp actionbar.list append value {"text":"x "}
execute if score #capacity mgs.data matches 16.. run data modify storage mgs:temp actionbar.list append value {"text":"A","font":"mgs:icons","shadow_color":[0,0,0,0],"color":"white"}
execute if score #capacity mgs.data matches 16.. run function mgs:v5.0.0/ammo/display_actionbar with storage mgs:temp actionbar
execute if score #capacity mgs.data matches ..15 run function mgs:v5.0.0/ammo/show_action_bar_icons

