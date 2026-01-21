
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

# Check weapon capabilities
execute store result score #has_auto mgs.data if data storage mgs:gun all.stats.can_auto
execute store result score #has_burst mgs.data if data storage mgs:gun all.stats.can_burst

# Show appropriate fire mode selector based on capabilities
# Weapons with auto and burst: [A | S | B]
# Weapons with auto only: [A | S]
# Weapons with burst only: [S | B]
# Weapons with neither: [S]

# A = Auto (only show if CAN_AUTO)
execute if score #has_auto mgs.data matches 1 if data storage mgs:gun all.stats{fire_mode:"auto"} run data modify storage mgs:temp actionbar.list append value {"text":"A","color":"green"}
execute if score #has_auto mgs.data matches 1 unless data storage mgs:gun all.stats{fire_mode:"auto"} run data modify storage mgs:temp actionbar.list append value {"text":"A","color":"dark_gray"}
execute if score #has_auto mgs.data matches 1 run data modify storage mgs:temp actionbar.list append value {"text":" | ","color":"gray"}

# S = Semi-auto (always available)
execute if data storage mgs:gun all.stats{fire_mode:"semi"} run data modify storage mgs:temp actionbar.list append value {"text":"S","color":"green"}
execute unless data storage mgs:gun all.stats{fire_mode:"semi"} run data modify storage mgs:temp actionbar.list append value {"text":"S","color":"dark_gray"}

# Show separator and burst only if weapon has burst capability
execute if score #has_burst mgs.data matches 1 run data modify storage mgs:temp actionbar.list append value {"text":" | ","color":"gray"}

# B = Burst (only show if CAN_BURST)
execute if score #has_burst mgs.data matches 1 if data storage mgs:gun all.stats{fire_mode:"burst"} run data modify storage mgs:temp actionbar.list append value {"text":"B","color":"yellow"}
execute if score #has_burst mgs.data matches 1 unless data storage mgs:gun all.stats{fire_mode:"burst"} run data modify storage mgs:temp actionbar.list append value {"text":"B","color":"dark_gray"}

# Add closing bracket
data modify storage mgs:temp actionbar.list append value {"text":" ]","color":"green"}

