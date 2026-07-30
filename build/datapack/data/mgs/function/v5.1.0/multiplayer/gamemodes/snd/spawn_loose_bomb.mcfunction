
#> mgs:v5.1.0/multiplayer/gamemodes/snd/spawn_loose_bomb
#
# @executed	at @e[tag=mgs.spawn_red,limit=1]
#
# @within	mgs:v5.1.0/multiplayer/gamemodes/snd/start_round [ at @e[tag=mgs.spawn_red,limit=1] ]
#			mgs:v5.1.0/multiplayer/gamemodes/snd/start_round [ at @e[tag=mgs.spawn_blue,limit=1] ]
#			mgs:v5.1.0/multiplayer/gamemodes/snd/start_round [ at @e[tag=mgs.spawn_point,limit=1] ]
#			mgs:v5.1.0/multiplayer/gamemodes/snd/drop_bomb [ at @e[tag=mgs.snd_carrier_label,limit=1] ]
#

summon minecraft:marker ~ ~ ~ {Tags:["mgs.snd_loose","mgs.snd_loose_at","mgs.gm_entity"]}
summon minecraft:block_display ~ ~ ~ {Tags:["mgs.snd_loose","mgs.gm_entity"],block_state:{Name:"minecraft:tnt"},transformation:{translation:[-0.25f,0.0f,-0.25f],left_rotation:[0.0f,0.0f,0.0f,1.0f],scale:[0.5f,0.5f,0.5f],right_rotation:[0.0f,0.0f,0.0f,1.0f]}}
summon minecraft:text_display ~ ~ ~ {Tags:["mgs.snd_loose","mgs.gm_entity"],billboard:"vertical",text:[[{"text":"💣 ","color":"gold","bold":true}, {"translate":"mgs.bomb"}]],transformation:{translation:[0.0f,1.1f,0.0f],left_rotation:[0.0f,0.0f,0.0f,1.0f],scale:[1.5f,1.5f,1.5f],right_rotation:[0.0f,0.0f,0.0f,1.0f]},shadow:true,see_through:true}

