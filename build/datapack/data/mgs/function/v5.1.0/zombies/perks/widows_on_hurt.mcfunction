
#> mgs:v5.1.0/zombies/perks/widows_on_hurt
#
# @executed	as the player & at current position
#
# @within	mgs:v5.1.0/zombies/hurt_player/on_hurt
#

# Need at least one web grenade in the lethal slot (grenade_type lives under the item's stats compound)
execute unless items entity @s hotbar.7 *[custom_data~{mgs:{stats:{grenade_type:"web"}}}] run return fail

# 2s (40t) internal cooldown
execute store result score #ww_now mgs.data run time query gametime
scoreboard players operation #ww_since mgs.data = #ww_now mgs.data
scoreboard players operation #ww_since mgs.data -= @s mgs.zb.ww_last
execute if score #ww_since mgs.data matches ..39 run return fail
scoreboard players operation @s mgs.zb.ww_last = #ww_now mgs.data

# Consume one web grenade + burst webbing around the player
item modify entity @s hotbar.7 mgs:v5.1.0/grenade/consume_one
particle minecraft:item{item:"minecraft:cobweb"} ~ ~1 ~ 0.8 0.8 0.8 0.1 40 force @a[distance=..48]
playsound minecraft:block.wool.place player @a[distance=..32] ~ ~ ~ 1 0.7
execute store result storage mgs:temp _web.radius float 1 run scoreboard players get #4 mgs.data
execute at @s run function mgs:v5.1.0/zombies/perks/widows_web_burst with storage mgs:temp _web

