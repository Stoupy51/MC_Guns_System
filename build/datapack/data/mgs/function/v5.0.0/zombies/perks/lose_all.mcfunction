
#> mgs:v5.0.0/zombies/perks/lose_all
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/zombies/revive/on_down
#

# Remove all perk effects and reset scoreboard tracking
execute if score @s mgs.zb.perk.juggernog matches 1 run attribute @s minecraft:max_health base reset
scoreboard players set @s mgs.zb.perk.juggernog 0
execute if score @s mgs.zb.perk.speed_cola matches 1 run scoreboard players set @s mgs.special.quick_reload 0
scoreboard players set @s mgs.zb.perk.speed_cola 0
execute if score @s mgs.zb.perk.double_tap matches 1 run scoreboard players set @s mgs.special.additional_shots 0
scoreboard players set @s mgs.zb.perk.double_tap 0
scoreboard players set @s mgs.zb.perk.mule_kick 0
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.all_perks_lost","color":"red"}]

