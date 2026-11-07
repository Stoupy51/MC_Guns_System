
#> mgs:v5.4.0/actionbar/add_dps
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/actionbar/show
#

execute store result score #dps_raw mgs.data run scoreboard players get @s mgs.previous_dps

scoreboard players operation #dps_int mgs.data = #dps_raw mgs.data
scoreboard players operation #dps_int mgs.data /= #10 mgs.data
scoreboard players operation #dps_dec mgs.data = #dps_raw mgs.data
scoreboard players operation #dps_dec mgs.data %= #10 mgs.data

data modify storage mgs:temp actionbar.list append value "    "
data modify storage mgs:temp actionbar.list append value {"text":"⚡","color":"#c77e36"}
data modify storage mgs:temp actionbar.list append value " "
data modify storage mgs:temp actionbar.list append value {"score":{"name":"#dps_int","objective":"mgs.data"}}
data modify storage mgs:temp actionbar.list append value {"text":"."}
data modify storage mgs:temp actionbar.list append value {"score":{"name":"#dps_dec","objective":"mgs.data"}}
data modify storage mgs:temp actionbar.list append value " "
data modify storage mgs:temp actionbar.list append value {"translate":"mgs.dps","fallback":"dps","color":"#c77e36"}

