
#> mgs:v5.3.0/zombies/apply_zombie_hp
#
# @executed	as @n[tag=mgs.zb_new]
#
# @within	mgs:v5.3.0/zombies/mob/setup
#			mgs:v5.3.0/zombies/types/fast
#			mgs:v5.3.0/zombies/types/tank
#			mgs:v5.3.0/zombies/types/armed
#			mgs:v5.3.0/zombies/types/aura
#

scoreboard players operation @s mgs.zb.max_hp = #zb_hp mgs.data

# A modifier over the type's default base: any NBT write on a wolf (a rise ending, an escort freezing it) puts its base back to 8.
attribute @s minecraft:max_health base reset
attribute @s minecraft:max_health modifier remove mgs:round_hp
execute store result score #zb_hp_base mgs.data run attribute @s minecraft:max_health base get
scoreboard players operation #zb_hp_add mgs.data = #zb_hp mgs.data
scoreboard players operation #zb_hp_add mgs.data -= #zb_hp_base mgs.data
execute store result storage mgs:temp _zb_hp.val int 1 run scoreboard players get #zb_hp_add mgs.data
function mgs:v5.3.0/zombies/add_hp_modifier with storage mgs:temp _zb_hp
execute store result entity @s Health float 1 run attribute @s minecraft:max_health get
function mgs:v5.3.0/zombies/absorb_above_cap

