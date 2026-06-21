
#> mgs:v5.0.1/zombies/powerups/spawn_type/nuke
#
# @executed	at @s
#
# @within	mgs:v5.0.1/zombies/powerups/do_spawn_random {x:$(x),y:$(y),z:$(z),uid:$(uid)}
#			mgs:v5.0.1/zombies/powerups/spawn_display {x:$(x),y:$(y),z:$(z),uid:$(uid)}
#
# @args		x (int)
#			y (int)
#			z (int)
#			uid (int)
#

$summon minecraft:item $(x) $(y) $(z) {Tags:["mgs.pu_item","mgs.pu_item_new","mgs.gm_entity"],PickupDelay:32767,Invulnerable:1b,Item:{id:"minecraft:tnt",count:1,components:{"minecraft:custom_data":{mgs:{powerup_uid:$(uid)}}}}}
scoreboard players set @n[tag=mgs.pu_item_new] mgs.zb.pu.type 5
scoreboard players set @n[tag=mgs.pu_item_new] mgs.zb.pu.timer 530
tag @n[tag=mgs.pu_item_new] remove mgs.pu_item_new

# Track live power-up count so game_tick can gate the per-item scans (decremented on expire/pickup,
# reset to 0 by the bulk cleanup, resynced periodically). pu_item is Invulnerable, so it can only die
# through those tracked paths — the count can never under-count and freeze a live power-up.
scoreboard players add #pu_active mgs.data 1
$execute positioned $(x) $(y) $(z) run summon minecraft:text_display ~ ~1.0 ~ {Tags:["mgs.pu_text","mgs.gm_entity"],text:{"translate":"mgs.nuke","color":"red","bold":true},billboard:"vertical",background:0,shadow:true,view_range:64.0f,transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[1.5f,1.5f,1.5f]}}

# Drop spawn cue
execute as @a[scores={mgs.zb.in_game=1}] at @s run playsound mgs:zombies/powerups/item/spawn ambient @s ~ ~ ~ 0.7 1.0

