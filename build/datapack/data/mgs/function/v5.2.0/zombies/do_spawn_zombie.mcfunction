
#> mgs:v5.2.0/zombies/do_spawn_zombie
#
# @executed	as @n[tag=mgs.zb_near,sort=random] & at @s
#
# @within	mgs:v5.2.0/zombies/spawn_zombie [ as @n[tag=mgs.zb_near,sort=random] & at @s ]
#

# Level: rounds 1-5 give 1, 6-10 give 2, 11-15 give 3, 16+ give 4.
execute if score #zb_round mgs.data matches ..5 run data modify storage mgs:temp _zpos.level set value "1"
execute if score #zb_round mgs.data matches 6..10 run data modify storage mgs:temp _zpos.level set value "2"
execute if score #zb_round mgs.data matches 11..15 run data modify storage mgs:temp _zpos.level set value "3"
execute if score #zb_round mgs.data matches 16.. run data modify storage mgs:temp _zpos.level set value "4"

# Special types replace a normal zombie in Zonweeb only, never on a dog round; Vanilla always spawns "normal".
data modify storage mgs:temp _zpos.type set value "normal"
scoreboard players set #zb_type_roll mgs.data 0
execute if data storage mgs:zombies game{variant:"zonweeb"} unless score #zb_dog_round mgs.data matches 1 store result score #zb_type_roll mgs.data run random value 1..100
execute if score #zb_type_roll mgs.data matches 1..15 if score #zb_round mgs.data matches 5.. run data modify storage mgs:temp _zpos.type set value "fast"
execute if score #zb_type_roll mgs.data matches 16..23 if score #zb_round mgs.data matches 10.. run data modify storage mgs:temp _zpos.type set value "tank"
execute if score #zb_type_roll mgs.data matches 24..28 if score #zb_round mgs.data matches 15.. run data modify storage mgs:temp _zpos.type set value "armed"
execute if score #zb_type_roll mgs.data matches 29..31 if score #zb_round mgs.data matches 20.. unless entity @e[type=minecraft:zombie,tag=mgs.zb_aura,limit=1] run data modify storage mgs:temp _zpos.type set value "aura"

function mgs:v5.2.0/zombies/summon_zombie_at with storage mgs:temp _zpos

# Remembered so a stuck-rescue never reuses this spawn.
scoreboard players operation @n[tag=mgs.zb_new] mgs.zb.spawn.sid = @s mgs.zb.spawn.sid

# Walk-to spawn (map editor `walk_to`): zombie_finish_rise walks the zombie there instead of letting it wander.
execute if data entity @s data.walk_to run data modify entity @n[tag=mgs.zb_new] data.walk_to set from entity @s data.walk_to

tag @n[tag=mgs.zb_new] remove mgs.zb_new

