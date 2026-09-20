
#> mgs:v5.1.0/zombies/do_spawn_dog
#
# @executed	as @n[tag=mgs.zb_near,sort=random] & at @s
#
# @within	mgs:v5.1.0/zombies/spawn_dog [ as @n[tag=mgs.zb_near,sort=random] & at @s ]
#

summon minecraft:marker ~ ~ ~ {Tags:["mgs.dog_portal","mgs.gm_entity"]}

# 30 ticks (1.5s) of telegraph before the strike
scoreboard players set @n[tag=mgs.dog_portal,tag=!mgs.dog_portal_armed] mgs.zb.rise_tick 30

# Carry the spawn point id through, so a stuck-rescue never reuses the spawn the dog came from
scoreboard players operation @n[tag=mgs.dog_portal,tag=!mgs.dog_portal_armed] mgs.zb.spawn.sid = @s mgs.zb.spawn.sid
tag @n[tag=mgs.dog_portal,tag=!mgs.dog_portal_armed] add mgs.dog_portal_armed

# A telegraphing dog isn't an entity yet, so #zb_alive can't see it — count it or the round
# completes early with the last dog still mid-portal (see game_tick).
scoreboard players add #zb_dog_pending mgs.data 1

# Opening cue: a crackle at the strike point. Volume 2.0 = 32 blocks of reach to match the
# selector, with a minVolume floor so the telegraph carries to players further out.
playsound minecraft:block.beacon.deactivate ambient @a[distance=..32] ~ ~ ~ 2.0 1.9 0.25

