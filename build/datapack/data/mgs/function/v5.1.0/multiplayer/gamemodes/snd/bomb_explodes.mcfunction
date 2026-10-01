
#> mgs:v5.1.0/multiplayer/gamemodes/snd/bomb_explodes
#
# @within	mgs:v5.1.0/multiplayer/gamemodes/snd/tick
#

execute at @e[tag=mgs.snd_bomb] run particle minecraft:explosion_emitter ~ ~1 ~ 2 2 2 0 5
execute at @e[tag=mgs.snd_bomb] run playsound minecraft:entity.generic.explode player @a ~ ~ ~ 2 0.8

# Players within 10 blocks die.
execute at @e[tag=mgs.snd_bomb] as @a[distance=..10,gamemode=!creative,gamemode=!spectator,scores={mgs.mp.in_game=1..}] run data modify storage mgs:input with set value {}
execute at @e[tag=mgs.snd_bomb] as @a[distance=..10,gamemode=!creative,gamemode=!spectator,scores={mgs.mp.in_game=1..}] run function mgs:v5.1.0/multiplayer/simulate_death

tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"text":"💥 ","color":"white"},{"translate":"mgs.bomb_exploded","color":"red","bold":true}]
kill @e[tag=mgs.snd_bomb]
function mgs:v5.1.0/multiplayer/gamemodes/snd/attackers_win

