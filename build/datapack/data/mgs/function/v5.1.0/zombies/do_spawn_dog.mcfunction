
#> mgs:v5.1.0/zombies/do_spawn_dog
#
# @executed	as @n[tag=mgs.zb_near,sort=random] & at @s
#
# @within	mgs:v5.1.0/zombies/spawn_dog [ as @n[tag=mgs.zb_near,sort=random] & at @s ]
#

summon minecraft:marker ~ ~ ~ {Tags:["mgs.dog_portal","mgs.gm_entity"]}

scoreboard players set @n[tag=mgs.dog_portal,tag=!mgs.dog_portal_armed] mgs.zb.rise_tick 30

scoreboard players operation @n[tag=mgs.dog_portal,tag=!mgs.dog_portal_armed] mgs.zb.spawn.sid = @s mgs.zb.spawn.sid
tag @n[tag=mgs.dog_portal,tag=!mgs.dog_portal_armed] add mgs.dog_portal_armed

# A dog still in its portal is not an entity, so count it or the round ends early (see game_tick).
scoreboard players add #zb_dog_pending mgs.data 1

# Volume 2.0 reaches the 32-block selector; minVolume lets players further out hear it.
playsound minecraft:block.beacon.deactivate ambient @a[distance=..32] ~ ~ ~ 2.0 1.9 0.25

