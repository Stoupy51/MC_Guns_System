
#> mgs:v5.3.0/zombies/do_spawn_zombie
#
# @executed	as @n[tag=mgs.zb_near,sort=random] & at @s
#
# @within	mgs:v5.3.0/zombies/spawn_zombie [ as @n[tag=mgs.zb_near,sort=random] & at @s ]
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

# 2 blocks over the spawn's rise duration, up through the floor or down from the ceiling.
scoreboard players set #zb_rise_step mgs.data 2000
execute if entity @s[tag=mgs.spawn_from_ceiling] run scoreboard players set #zb_rise_step mgs.data -2000
scoreboard players operation #zb_rise_step mgs.data /= @s mgs.zb.rise_tick

execute unless entity @s[tag=mgs.spawn_from_ceiling] run function mgs:v5.3.0/zombies/summon_zombie_at with storage mgs:temp _zpos
execute if entity @s[tag=mgs.spawn_from_ceiling] positioned ~ ~4 ~ run function mgs:v5.3.0/zombies/summon_zombie_at with storage mgs:temp _zpos
scoreboard players operation @n[tag=mgs.zb_new] mgs.zb.rise_tick = @s mgs.zb.rise_tick
scoreboard players operation @n[tag=mgs.zb_new] mgs.zb.rise_step = #zb_rise_step mgs.data

# The block broken through is the floor below the spawn or the ceiling 2 blocks above it.
execute unless entity @s[tag=mgs.spawn_from_ceiling] run function mgs:v5.3.0/zombies/summon_rise_dust {block_y:"-1"}
execute if entity @s[tag=mgs.spawn_from_ceiling] positioned ~ ~2 ~ run function mgs:v5.3.0/zombies/summon_rise_dust {block_y:"0"}

# Remembered so a stuck-rescue never reuses this spawn.
scoreboard players operation @n[tag=mgs.zb_new] mgs.zb.spawn.sid = @s mgs.zb.spawn.sid

# Walk-to spawn (map editor `walk_to`): zombie_finish_rise walks the zombie there instead of letting it wander.
execute if data entity @s data.walk_to run data modify entity @n[tag=mgs.zb_new] data.walk_to set from entity @s data.walk_to

tag @n[tag=mgs.zb_new] remove mgs.zb_new

