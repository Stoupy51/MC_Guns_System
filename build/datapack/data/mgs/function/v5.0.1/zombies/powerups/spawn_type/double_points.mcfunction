
#> mgs:v5.0.1/zombies/powerups/spawn_type/double_points
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

$summon minecraft:item $(x) $(y) $(z) {Tags:["mgs.pu_item","mgs.pu_item_new","mgs.gm_entity"],PickupDelay:32767,Invulnerable:1b,Item:{id:"minecraft:gold_ingot",count:1,components:{"minecraft:custom_data":{mgs:{powerup_uid:$(uid)}}}}}
scoreboard players set @n[tag=mgs.pu_item_new] mgs.zb.pu.type 3
scoreboard players set @n[tag=mgs.pu_item_new] mgs.zb.pu.timer 530
tag @n[tag=mgs.pu_item_new] remove mgs.pu_item_new
$execute positioned $(x) $(y) $(z) run summon minecraft:text_display ~ ~1.0 ~ {Tags:["mgs.pu_text","mgs.gm_entity"],text:{"translate":"mgs.double_points","color":"yellow","bold":true},billboard:"vertical",background:0,shadow:true,view_range:64.0f,transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[1.5f,1.5f,1.5f]}}
tellraw @a[scores={mgs.zb.in_game=1}] [{"translate":"mgs.double_points","color":"yellow","bold":true},[{"text":" ","color":"white"}, {"translate":"mgs.has_dropped"}]]
playsound minecraft:entity.experience_orb.pickup master @a[scores={mgs.zb.in_game=1}] ~ ~ ~ 1.0 0.7

