
#> mgs:v5.1.0/zombies/powerups/spawn_type
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/powerups/spawn_display {x:$(x),y:$(y),z:$(z),uid:$(uid),item:"minecraft:amethyst_shard",type_num:1,label:'{"translate":"mgs.max_ammo","color":"aqua","bold":true}'}
#			mgs:v5.1.0/zombies/powerups/spawn_display {x:$(x),y:$(y),z:$(z),uid:$(uid),item:"minecraft:fermented_spider_eye",type_num:2,label:'{"translate":"mgs.insta_kill","color":"red","bold":true}'}
#			mgs:v5.1.0/zombies/powerups/spawn_display {x:$(x),y:$(y),z:$(z),uid:$(uid),item:"minecraft:gold_ingot",type_num:3,label:'{"translate":"mgs.double_points","color":"yellow","bold":true}'}
#			mgs:v5.1.0/zombies/powerups/spawn_display {x:$(x),y:$(y),z:$(z),uid:$(uid),item:"minecraft:oak_log",type_num:4,label:'{"translate":"mgs.carpenter","color":"gold","bold":true}'}
#			mgs:v5.1.0/zombies/powerups/spawn_display {x:$(x),y:$(y),z:$(z),uid:$(uid),item:"minecraft:tnt",type_num:5,label:'{"translate":"mgs.nuke","color":"red","bold":true}'}
#			mgs:v5.1.0/zombies/powerups/spawn_display {x:$(x),y:$(y),z:$(z),uid:$(uid),item:"minecraft:blaze_rod",type_num:6,label:'{"translate":"mgs.unlimited_ammo","color":"green","bold":true}'}
#			mgs:v5.1.0/zombies/powerups/spawn_display {x:$(x),y:$(y),z:$(z),uid:$(uid),item:"minecraft:glass_bottle",type_num:7,label:'{"translate":"mgs.random_perk","color":"light_purple","bold":true}'}
#			mgs:v5.1.0/zombies/powerups/spawn_display {x:$(x),y:$(y),z:$(z),uid:$(uid),item:"minecraft:diamond",type_num:8,label:'{"translate":"mgs.free_pap","color":"aqua","bold":true}'}
#			mgs:v5.1.0/zombies/powerups/spawn_display {x:$(x),y:$(y),z:$(z),uid:$(uid),item:"minecraft:emerald",type_num:9,label:'{"translate":"mgs.cash_drop","color":"green","bold":true}'}
#			mgs:v5.1.0/zombies/powerups/spawn_display {x:$(x),y:$(y),z:$(z),uid:$(uid),item:"minecraft:firework_star",type_num:10,label:'{"translate":"mgs.fire_sale","color":"light_purple","bold":true}'}
#			mgs:v5.1.0/zombies/powerups/spawn_display {x:$(x),y:$(y),z:$(z),uid:$(uid),item:"minecraft:campfire",type_num:11,label:'{"translate":"mgs.bonfire_sale","color":"gold","bold":true}'}
#
# @args		x (int)
#			y (int)
#			z (int)
#			item (string)
#			uid (int)
#			type_num (int)
#			label (string)
#

$summon minecraft:item $(x) $(y) $(z) {Tags:["mgs.pu_item","mgs.pu_item_new","mgs.gm_entity"],PickupDelay:32767,Invulnerable:1b,Item:{id:"$(item)",count:1,components:{"minecraft:custom_data":{mgs:{powerup_uid:$(uid)}}}}}
$scoreboard players set @n[type=minecraft:item,tag=mgs.pu_item_new] mgs.zb.pu.type $(type_num)
scoreboard players set @n[type=minecraft:item,tag=mgs.pu_item_new] mgs.zb.pu.timer 530
tag @n[type=minecraft:item,tag=mgs.pu_item_new] remove mgs.pu_item_new

# Track live power-up count so game_tick can gate the per-item scans (decremented on expire/pickup,
# reset to 0 by the bulk cleanup, resynced periodically). pu_item is Invulnerable, so it can only die
# through those tracked paths — the count can never under-count and freeze a live power-up.
scoreboard players add #pu_active mgs.data 1
$execute positioned $(x) $(y) $(z) run summon minecraft:text_display ~ ~1.0 ~ {Tags:["mgs.pu_text","mgs.gm_entity"],text:$(label),billboard:"vertical",background:0,shadow:true,view_range:64.0f,transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[1.5f,1.5f,1.5f]}}

# Drop spawn cue
execute as @a[scores={mgs.zb.in_game=1}] at @s run playsound mgs:zombies/powerups/item/spawn ambient @s ~ ~ ~ 0.7 1.0

