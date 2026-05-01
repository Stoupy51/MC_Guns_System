
#> mgs:v5.0.0/zombies/powerups/spawn_type/unlimited_ammo
#
# @executed	at @s
#
# @within	mgs:v5.0.0/zombies/powerups/do_spawn_random {x:$(x),y:$(y),z:$(z)}
#			mgs:v5.0.0/zombies/powerups/spawn_display {{x:$(x),y:$(y),z:$(z)}}
#
# @args		x (int)
#			y (int)
#			z (int)
#

$summon minecraft:item_display $(x) $(y) $(z) {Tags:["mgs.pu_item","mgs.pu_item_new","mgs.gm_entity"],item:{id:"minecraft:blaze_rod",count:1,components:{"minecraft:item_model":"mgs:zombies/powerup/unlimited_ammo"}},item_display:"ground",billboard:"center",transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0.25f,0f],scale:[0.7f,0.7f,0.7f]}}
scoreboard players set @n[tag=mgs.pu_item_new] mgs.zb.pu.type 5
scoreboard players set @n[tag=mgs.pu_item_new] mgs.zb.pu.timer 530
tag @n[tag=mgs.pu_item_new] remove mgs.pu_item_new
$execute positioned $(x) $(y) $(z) run summon minecraft:text_display ~ ~1.0 ~ {Tags:["mgs.pu_text","mgs.gm_entity"],text:{"translate":"mgs.unlimited_ammo_2","color":"yellow","bold":true},billboard:"center",background:0,shadow:true,transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[1.5f,1.5f,1.5f]}}
tellraw @a[scores={mgs.zb.in_game=1}] [{"translate":"mgs.unlimited_ammo_2","color":"yellow","bold":true},[{"text":" ","color":"white"}, {"translate":"mgs.has_dropped"}]]
playsound minecraft:entity.experience_orb.pickup master @a[scores={mgs.zb.in_game=1}] ~ ~ ~ 1.0 0.7

