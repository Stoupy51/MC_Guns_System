
#> mgs:v5.0.1/zombies/powerups/spawn_type/cash_drop
#
# @executed	at @s
#
# @within	mgs:v5.0.1/zombies/powerups/do_spawn_random {x:$(x),y:$(y),z:$(z)}
#			mgs:v5.0.1/zombies/powerups/spawn_display {{x:$(x),y:$(y),z:$(z)}}
#
# @args		x (int)
#			y (int)
#			z (int)
#

$summon minecraft:item_display $(x) $(y) $(z) {Tags:["mgs.pu_item","mgs.pu_item_new","mgs.gm_entity"],item:{id:"minecraft:emerald",count:1},billboard:"vertical",item_display:"ground",brightness:{block:15,sky:15},transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0.25f,0f],scale:[1.5f,1.5f,1.5f]}}
scoreboard players set @n[tag=mgs.pu_item_new] mgs.zb.pu.type 9
scoreboard players set @n[tag=mgs.pu_item_new] mgs.zb.pu.timer 530
tag @n[tag=mgs.pu_item_new] remove mgs.pu_item_new
$execute positioned $(x) $(y) $(z) run summon minecraft:text_display ~ ~1.0 ~ {Tags:["mgs.pu_text","mgs.gm_entity"],text:{"translate":"mgs.cash_drop_2","color":"green","bold":true},billboard:"vertical",background:0,shadow:true,view_range:64.0f,transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[1.5f,1.5f,1.5f]}}
tellraw @a[scores={mgs.zb.in_game=1}] [{"translate":"mgs.cash_drop_2","color":"green","bold":true},[{"text":" ","color":"white"}, {"translate":"mgs.has_dropped"}]]
playsound minecraft:entity.experience_orb.pickup master @a[scores={mgs.zb.in_game=1}] ~ ~ ~ 1.0 0.7

