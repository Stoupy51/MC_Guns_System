
#> mgs:v5.0.0/actionbar/build_fire_mode_indicator
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/actionbar/show
#

# Initialize actionbar list
data modify storage mgs:temp actionbar set value {list:[]}

# Add opening bracket
data modify storage mgs:temp actionbar.list append value {"text":"","color":"#c24a17"}
data modify storage mgs:temp actionbar.list append value {"text":"[ ","color":"#c77e36"}

# Check weapon capabilities
execute store result score #has_auto mgs.data if data storage mgs:gun all.stats.can_auto
execute store result score #has_burst mgs.data if data storage mgs:gun all.stats.can_burst

# Show appropriate fire mode selector based on capabilities
# Weapons with auto and burst: [S | B | A]
# Weapons with auto only: [S | A]
# Weapons with burst only: [S | B]
# Weapons with neither: [S]

# S = Semi-auto (always available)
execute if data storage mgs:gun all.stats{fire_mode:"semi"} run data modify storage mgs:temp actionbar.list append value {"text":"S","color":"yellow","bold":true}
execute unless data storage mgs:gun all.stats{fire_mode:"semi"} run data modify storage mgs:temp actionbar.list append value {"text":"S"}

# Show separator and burst only if weapon has burst capability
execute if score #has_burst mgs.data matches 1 run data modify storage mgs:temp actionbar.list append value {"text":" | "}

# B = Burst (only show if CAN_BURST)
execute if score #has_burst mgs.data matches 1 if data storage mgs:gun all.stats{fire_mode:"burst"} run data modify storage mgs:temp actionbar.list append value {"text":"B","color":"yellow"}
execute if score #has_burst mgs.data matches 1 unless data storage mgs:gun all.stats{fire_mode:"burst"} run data modify storage mgs:temp actionbar.list append value {"text":"B"}

# Show separator and auto only if weapon has auto capability
execute if score #has_auto mgs.data matches 1 run data modify storage mgs:temp actionbar.list append value {"text":" | "}

# A = Auto (only show if CAN_AUTO)
execute if score #has_auto mgs.data matches 1 if data storage mgs:gun all.stats{fire_mode:"auto"} run data modify storage mgs:temp actionbar.list append value {"text":"A","color":"yellow","bold":true}
execute if score #has_auto mgs.data matches 1 unless data storage mgs:gun all.stats{fire_mode:"auto"} run data modify storage mgs:temp actionbar.list append value {"text":"A"}

# Add closing bracket
data modify storage mgs:temp actionbar.list append value {"text":" ]    ","color":"#c77e36"}

