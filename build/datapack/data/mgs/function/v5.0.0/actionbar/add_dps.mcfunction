
#> mgs:v5.0.0/actionbar/add_dps
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/actionbar/show
#

# Get collected DPS (accumulated damage*10 per second, snapshotted every 20 ticks)
execute store result score #dps_raw mgs.data run scoreboard players get @s mgs.previous_dps

# Split into integer and decimal parts (previous_dps is damage*10/sec)
scoreboard players operation #dps_int mgs.data = #dps_raw mgs.data
scoreboard players operation #dps_int mgs.data /= #10 mgs.data
scoreboard players operation #dps_dec mgs.data = #dps_raw mgs.data
scoreboard players operation #dps_dec mgs.data %= #10 mgs.data

# Append DPS to actionbar list
data modify storage mgs:temp actionbar.list append value "    "
data modify storage mgs:temp actionbar.list append value {"text":"⚡","color":"#c77e36"}
data modify storage mgs:temp actionbar.list append value " "
data modify storage mgs:temp actionbar.list append value {"score":{"name":"#dps_int","objective":"mgs.data"}}
data modify storage mgs:temp actionbar.list append value {"text":"."}
data modify storage mgs:temp actionbar.list append value {"score":{"name":"#dps_dec","objective":"mgs.data"}}
data modify storage mgs:temp actionbar.list append value " "
data modify storage mgs:temp actionbar.list append value {"translate":"mgs.dps","color":"#c77e36"}

