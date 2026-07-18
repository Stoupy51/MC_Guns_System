
#> mgs:v5.1.0/multiplayer/drop_spawn
#
# @executed	at @s
#
# @within	mgs:v5.1.0/multiplayer/drop_held_weapon
#

scoreboard players set #drop_spawned mgs.data 1

# Static item display lying flat on the ground (left_rotation = 90° around X), with a random yaw
# so a batch of drops doesn't end up all facing the same way
summon minecraft:item_display ~ ~0.05 ~ {Tags:["mgs.mp_dropped_gun","mgs.gm_entity","mgs.mp_drop_new"],item_display:"ground",transformation:{left_rotation:[0.7071068f,0f,0f,0.7071068f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[0.75f,0.75f,0.75f]}}
data modify entity @n[tag=mgs.mp_drop_new] item set from storage mgs:temp _dropw
execute store result storage mgs:temp _drop_yaw float 1 run random value -180..179
data modify entity @n[tag=mgs.mp_drop_new] Rotation[0] set from storage mgs:temp _drop_yaw
scoreboard players set @n[tag=mgs.mp_drop_new] mgs.mp.drop_timer 600
tag @n[tag=mgs.mp_drop_new] remove mgs.mp_drop_new

# Small interaction hitbox for pickup (Bookshelf right-click)
summon minecraft:interaction ~ ~ ~ {width:0.9f,height:0.6f,response:true,Tags:["mgs.mp_drop_int","mgs.gm_entity","bs.entity.interaction","mgs.mp_drop_new"]}
scoreboard players set @n[tag=mgs.mp_drop_new] mgs.mp.drop_timer 600
execute as @n[tag=mgs.mp_drop_new] run function #bs.interaction:on_right_click {run:"function mgs:v5.1.0/multiplayer/pickup_dropped_weapon",executor:"source"}
tag @n[tag=mgs.mp_drop_new] remove mgs.mp_drop_new

