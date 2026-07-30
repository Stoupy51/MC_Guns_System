
#> mgs:v5.1.0/multiplayer/gamemodes/snd/try_pickup
#
# @executed	as @a[tag=mgs.snd_alive,gamemode=!spectator] & at @s
#
# @within	mgs:v5.1.0/multiplayer/gamemodes/snd/tick [ as @a[tag=mgs.snd_alive,gamemode=!spectator] & at @s ]
#

# Defenders cannot touch the bomb
execute if score #snd_attackers mgs.data matches 1 unless score @s mgs.mp.team matches 1 run return fail
execute if score #snd_attackers mgs.data matches 2 unless score @s mgs.mp.team matches 2 run return fail

tag @s add mgs.snd_carrier
kill @e[tag=mgs.snd_loose]

# The label rides along by teleport (an entity cannot be made to ride a player), and doubles as the record
# of where the carrier is: if they die, the bomb drops at this label's position.
summon minecraft:text_display ~ ~ ~ {Tags:["mgs.snd_carrier_label","mgs.gm_entity"],billboard:"vertical",teleport_duration:1,text:[{"text":"💣","color":"gold","bold":true}],transformation:{translation:[0.0f,0.0f,0.0f],left_rotation:[0.0f,0.0f,0.0f,1.0f],scale:[1.5f,1.5f,1.5f],right_rotation:[0.0f,0.0f,0.0f,1.0f]},shadow:true,see_through:false}

tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],"💣 ",{"selector":"@s"},[{"text":" ","color":"gold"}, {"translate":"mgs.picked_up_the_bomb"}]]
playsound minecraft:item.armor.equip_chain player @a ~ ~ ~ 1 1.2

