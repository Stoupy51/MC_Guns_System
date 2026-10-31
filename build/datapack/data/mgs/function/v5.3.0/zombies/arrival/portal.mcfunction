
#> mgs:v5.3.0/zombies/arrival/portal
#
# @executed	at @s
#
# @within	mgs:v5.3.0/zombies/do_spawn
#

summon minecraft:marker ~ ~ ~ {Tags:["mgs.zb_portal","mgs.zombies_entity","mgs.zb_portal_new"],CustomName:"Spawn Portal"}
data modify entity @n[tag=mgs.zb_portal_new] data.mob set from storage mgs:temp _mob
execute if data entity @s data.walk_to run data modify entity @n[tag=mgs.zb_portal_new] data.walk_to set from entity @s data.walk_to
scoreboard players set @n[tag=mgs.zb_portal_new] mgs.zb.rise_tick 30
scoreboard players operation @n[tag=mgs.zb_portal_new] mgs.zb.spawn.sid = @s mgs.zb.spawn.sid
tag @n[tag=mgs.zb_portal_new] remove mgs.zb_portal_new

# An enemy still in its portal is not an entity, so count it or the round ends early (see game_tick).
scoreboard players add #zb_portal_pending mgs.data 1

# Volume 2.0 reaches the 32-block selector; minVolume lets players further out hear it.
playsound minecraft:block.beacon.deactivate ambient @a[distance=..32] ~ ~ ~ 2.0 1.9 0.25

