
#> mgs:v5.0.0/actionbar/build_fire_mode_indicator
#
# @executed	as @a[sort=random] & at @s
#
# @within	mgs:v5.0.0/actionbar/show
#

# Initialize actionbar list
data modify storage mgs:temp actionbar set value {list:[]}

# Add opening bracket
data modify storage mgs:temp actionbar.list append value {"text":"[ ","color":"#c24a17"}

# Check current fire mode and add indicators
execute store result score #has_burst mgs.data if data storage mgs:gun all.stats.can_burst

# If weapon doesn't support burst, only show [A]
execute if score #has_burst mgs.data matches 0 run data modify storage mgs:temp actionbar.list append value {"text":"A","color":"green"}
execute if score #has_burst mgs.data matches 0 run data modify storage mgs:temp actionbar.list append value {"text":" ]"}
execute if score #has_burst mgs.data matches 0 run return 0

# Weapon supports burst - show full selector
# A = Auto
execute if data storage mgs:gun all.stats{fire_mode:"auto"} run data modify storage mgs:temp actionbar.list append value {"text":"A","color":"green"}
execute unless data storage mgs:gun all.stats{fire_mode:"auto"} if data storage mgs:gun all.stats.fire_mode run data modify storage mgs:temp actionbar.list append value {"text":"A","color":"dark_gray"}
execute unless data storage mgs:gun all.stats.fire_mode run data modify storage mgs:temp actionbar.list append value {"text":"A","color":"green"}

# Separator
data modify storage mgs:temp actionbar.list append value {"text":" | ","color":"gray"}

# S = Semi (not implemented yet, always grayed)
data modify storage mgs:temp actionbar.list append value {"text":"S","color":"dark_gray"}

# Separator
data modify storage mgs:temp actionbar.list append value {"text":" | ","color":"gray"}

# B = Burst
execute if data storage mgs:gun all.stats{fire_mode:"burst"} run data modify storage mgs:temp actionbar.list append value {"text":"B","color":"yellow"}
execute unless data storage mgs:gun all.stats{fire_mode:"burst"} run data modify storage mgs:temp actionbar.list append value {"text":"B","color":"dark_gray"}

# Add closing bracket
data modify storage mgs:temp actionbar.list append value {"text":" ]","color":"green"}

