
#> mgs:v5.3.0/zombies/knife_camo/pick
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.3.0/player/config/process
#

execute if score @s mgs.player.config matches 1621 if score @s mgs.zb.xp_level matches 1.. run scoreboard players set @s mgs.zb.knife_camo 0
execute if score @s mgs.player.config matches 1622 if score @s mgs.zb.xp_level matches 25.. run scoreboard players set @s mgs.zb.knife_camo 1
execute if score @s mgs.player.config matches 1623 if score @s mgs.zb.xp_level matches 50.. run scoreboard players set @s mgs.zb.knife_camo 2
execute if score @s mgs.player.config matches 1624 if score @s mgs.zb.xp_level matches 100.. run scoreboard players set @s mgs.zb.knife_camo 3
execute if score @s mgs.player.config matches 1625 if score @s mgs.zb.xp_level matches 75.. run scoreboard players set @s mgs.zb.knife_camo 4
function mgs:v5.3.0/zombies/knife_camo/menu

