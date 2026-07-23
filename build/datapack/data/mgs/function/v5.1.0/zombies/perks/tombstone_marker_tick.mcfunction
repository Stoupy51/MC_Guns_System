
#> mgs:v5.1.0/zombies/perks/tombstone_marker_tick
#
# @executed	as @e[tag=mgs.tombstone,scores={mgs.zb.ts.state=1}] & at @s
#
# @within	mgs:v5.1.0/zombies/game_tick [ as @e[tag=mgs.tombstone,scores={mgs.zb.ts.state=1}] & at @s ]
#

particle minecraft:soul ~ ~0.5 ~ 0.25 0.4 0.25 0.01 3 force @a[distance=..48]
particle minecraft:soul_fire_flame ~ ~0.6 ~ 0.15 0.2 0.15 0.005 1 force @a[distance=..48]

# Count down; expire (despawn + drop the inventory snapshot) when the timer runs out
scoreboard players operation @s mgs.zb.ts.timer -= #tick_delta mgs.data
execute if score @s mgs.zb.ts.timer matches ..0 run return run function mgs:v5.1.0/zombies/perks/tombstone_expire

# Owner standing within 2 blocks (alive, in-game, not downed) → recover
scoreboard players operation #ts_mid mgs.data = @s mgs.zb.downed_id
execute as @a[distance=..2,gamemode=!spectator,scores={mgs.zb.in_game=1,mgs.zb.downed=0}] if score @s mgs.zb.downed_id = #ts_mid mgs.data run function mgs:v5.1.0/zombies/perks/tombstone_collect

