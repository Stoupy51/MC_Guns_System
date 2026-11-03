
#> mgs:v5.3.0/zombies/arrival/rescued
#
# @executed	as @n[tag=mgs.zb_near] & at @s
#
# @within	mgs:v5.3.0/zombies/rescue_tp [ as @n[tag=mgs.zb_near] & at @s ]
#

execute if entity @s[tag=mgs.arrive_portal] run return run function mgs:v5.3.0/zombies/portal_strike_fx
execute if entity @s[tag=mgs.arrive_instant] run return 0

scoreboard players set #zb_rise_step mgs.data 2000
execute if entity @s[tag=mgs.arrive_ceiling] run scoreboard players set #zb_rise_step mgs.data -2000
scoreboard players operation #zb_rise_step mgs.data /= @s mgs.zb.rise_tick

execute if entity @s[tag=mgs.arrive_ceiling] positioned ~ ~2.2 ~ run tp @n[tag=mgs.zb_rescue_new] ~ ~ ~
execute unless entity @s[tag=mgs.arrive_ceiling] positioned ~ ~-1.8 ~ run tp @n[tag=mgs.zb_rescue_new] ~ ~ ~
data modify entity @n[tag=mgs.zb_rescue_new] NoAI set value 1b
scoreboard players operation @n[tag=mgs.zb_rescue_new] mgs.zb.rise_tick = @s mgs.zb.rise_tick
scoreboard players operation @n[tag=mgs.zb_rescue_new] mgs.zb.rise_step = #zb_rise_step mgs.data
tag @n[tag=mgs.zb_rescue_new] add mgs.zb_rising

execute if entity @s[tag=mgs.arrive_ceiling] positioned ~ ~2 ~ run function mgs:v5.3.0/zombies/summon_rise_dust {block_y:"0"}
execute unless entity @s[tag=mgs.arrive_ceiling] run function mgs:v5.3.0/zombies/summon_rise_dust {block_y:"-1"}

