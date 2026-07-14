
#> mgs:v5.1.0/zombies/perks/lose_all
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/zombies/revive/on_down
#			mgs:v5.1.0/zombies/revive/full_death
#

# Remove all perk effects and reset scoreboard tracking
execute if score @s mgs.zb.perk.juggernog matches 1 run attribute @s minecraft:max_health base reset
scoreboard players set @s mgs.zb.perk.juggernog 0
execute if score @s mgs.zb.perk.speed_cola matches 1 run scoreboard players set @s mgs.special.quick_reload 0
scoreboard players set @s mgs.zb.perk.speed_cola 0
execute if score @s mgs.zb.perk.double_tap matches 1 run scoreboard players set @s mgs.special.additional_shots 0
scoreboard players set @s mgs.zb.perk.double_tap 0
scoreboard players set @s mgs.zb.perk.mule_kick 0
execute if score @s mgs.zb.perk.stamin_up matches 1 run attribute @s minecraft:movement_speed modifier remove mgs:stamin_up
execute if score @s mgs.zb.perk.stamin_up matches 1 run scoreboard players set @s mgs.stam_bonus 0
scoreboard players set @s mgs.zb.perk.stamin_up 0
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.all_perks_lost","color":"red"}]

# Remove the perk display items from the inventory right away
function mgs:v5.1.0/zombies/inventory/refresh_perk_items

