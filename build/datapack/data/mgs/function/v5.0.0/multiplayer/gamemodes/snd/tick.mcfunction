
#> mgs:v5.0.0/multiplayer/gamemodes/snd/tick
#
# @within	mgs:v5.0.0/multiplayer/game_tick
#

# Round timer
scoreboard players remove #snd_round_timer mgs.data 1

# If timer runs out, defenders win
execute if score #snd_round_timer mgs.data matches ..0 if score #snd_bomb_state mgs.data matches ..1 run function mgs:v5.0.0/multiplayer/gamemodes/snd/defenders_win

# If bomb planted, tick bomb timer (45 seconds = 900 ticks)
execute if score #snd_bomb_state mgs.data matches 2 run scoreboard players remove #snd_bomb_timer mgs.data 1
execute if score #snd_bomb_state mgs.data matches 2 if score #snd_bomb_timer mgs.data matches ..0 run function mgs:v5.0.0/multiplayer/gamemodes/snd/bomb_explodes

# Check if all attackers are dead (defenders win)
execute store result score #_snd_atk_alive mgs.data if entity @a[tag=mgs.snd_alive,scores={mgs.mp.team=1}]
execute if score #snd_attackers mgs.data matches 2 store result score #_snd_atk_alive mgs.data if entity @a[tag=mgs.snd_alive,scores={mgs.mp.team=2}]
execute if score #_snd_atk_alive mgs.data matches 0 if score #snd_bomb_state mgs.data matches ..1 run function mgs:v5.0.0/multiplayer/gamemodes/snd/defenders_win

# Check if all defenders are dead and bomb not planted (attackers win)
execute store result score #_snd_def_alive mgs.data if entity @a[tag=mgs.snd_alive,scores={mgs.mp.team=2}]
execute if score #snd_attackers mgs.data matches 2 store result score #_snd_def_alive mgs.data if entity @a[tag=mgs.snd_alive,scores={mgs.mp.team=1}]
execute if score #_snd_def_alive mgs.data matches 0 run function mgs:v5.0.0/multiplayer/gamemodes/snd/attackers_win

# Particles at objectives
execute at @e[tag=mgs.snd_obj] run particle dust{color:[1.0,0.6,0.0],scale:1.0} ~ ~1 ~ 1.0 0.5 1.0 0 5

# Check planting (attacker near objective and sneaking)
execute if score #snd_bomb_state mgs.data matches 0 as @a[tag=mgs.snd_alive,predicate=mgs:v5.0.0/is_sneaking] at @s if entity @e[tag=mgs.snd_obj,distance=..3] run function mgs:v5.0.0/multiplayer/gamemodes/snd/try_plant

# Check defusing (defender near bomb and sneaking)
execute if score #snd_bomb_state mgs.data matches 2 as @a[tag=mgs.snd_alive,predicate=mgs:v5.0.0/is_sneaking] at @s if entity @e[tag=mgs.snd_bomb,distance=..3] run function mgs:v5.0.0/multiplayer/gamemodes/snd/try_defuse

