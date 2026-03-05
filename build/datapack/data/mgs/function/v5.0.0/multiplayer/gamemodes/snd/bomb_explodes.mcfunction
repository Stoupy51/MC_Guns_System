
#> mgs:v5.0.0/multiplayer/gamemodes/snd/bomb_explodes
#
# @within	mgs:v5.0.0/multiplayer/gamemodes/snd/tick
#

# Explosion effect at bomb
execute at @e[tag=mgs.snd_bomb] run particle minecraft:explosion_emitter ~ ~1 ~ 2 2 2 0 5
execute at @e[tag=mgs.snd_bomb] run playsound minecraft:entity.generic.explode player @a ~ ~ ~ 2 0.8

# Kill any players near the bomb (10 block radius)
execute at @e[tag=mgs.snd_bomb] run kill @a[distance=..10,gamemode=!creative,gamemode=!spectator]

tellraw @a [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.bomb_exploded","color":"red","bold":true}]
kill @e[tag=mgs.snd_bomb]
function mgs:v5.0.0/multiplayer/gamemodes/snd/attackers_win

