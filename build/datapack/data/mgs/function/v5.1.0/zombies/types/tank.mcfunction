
#> mgs:v5.1.0/zombies/types/tank
#
# @executed	as @n[tag=mgs.zb_near,sort=random] & at @s
#
# @within	mgs:v5.1.0/zombies/summon_zombie_at {level:"$(level)"}
#
# @args		level (string)
#

scoreboard players set #zb_no_walker mgs.data 1
$function mgs:v5.1.0/zombies/types/normal {level:"$(level)"}
scoreboard players set #zb_no_walker mgs.data 0
tag @s add mgs.zb_tank

# 75% of the round's speed; the escort taxi reads this base value.
execute store result storage mgs:temp _zb_speed.value double 0.00075 run attribute @s minecraft:movement_speed base get 1000
function mgs:v5.1.0/zombies/set_speed with storage mgs:temp _zb_speed
execute store result score #zb_speed mgs.data run attribute @s minecraft:movement_speed base get 1000
execute if score #zb_speed mgs.data matches 290.. run tag @s add mgs.zb_sprint
execute if score #zb_speed mgs.data matches ..289 run tag @s remove mgs.zb_sprint

# 300% of the health normal just applied (#zb_hp).
scoreboard players operation #zb_hp mgs.data *= #300 mgs.data
scoreboard players operation #zb_hp mgs.data /= #100 mgs.data
execute if score #zb_hp mgs.data matches 3073.. run scoreboard players set #zb_hp mgs.data 3072
execute store result storage mgs:temp _zb_hp.val int 1 run scoreboard players get #zb_hp mgs.data
function mgs:v5.1.0/zombies/apply_zombie_hp with storage mgs:temp _zb_hp

attribute @s minecraft:scale base set 1.25

