
#> mgs:v5.3.0/zombies/knife_camo/on_level_up
#
# @within	#mgs:progression/on_level_up
#

execute unless data storage mgs:signals on_level_up{side:"zb"} run return fail
execute if score #xp_lvl_before mgs.data matches ..24 if score @s mgs.zb.xp_level matches 25.. run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.zombies_knife_camo_unlocked","fallback":"Zombies knife camo unlocked: ","color":"green"},{"translate":"mgs.autumn","fallback":"Autumn","color":"gold"}]
execute if score #xp_lvl_before mgs.data matches ..49 if score @s mgs.zb.xp_level matches 50.. run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.zombies_knife_camo_unlocked","fallback":"Zombies knife camo unlocked: ","color":"green"},{"translate":"mgs.galaxy","fallback":"Galaxy","color":"gold"}]
execute if score #xp_lvl_before mgs.data matches ..99 if score @s mgs.zb.xp_level matches 100.. run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.zombies_knife_camo_unlocked","fallback":"Zombies knife camo unlocked: ","color":"green"},{"translate":"mgs.gold","fallback":"Gold","color":"gold"}]
execute if score #xp_lvl_before mgs.data matches ..74 if score @s mgs.zb.xp_level matches 75.. run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.zombies_knife_camo_unlocked","fallback":"Zombies knife camo unlocked: ","color":"green"},{"translate":"mgs.red_polymer","fallback":"Red Polymer","color":"gold"}]

