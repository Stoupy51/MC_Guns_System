
#> mgs:v5.1.0/multiplayer/refresh_sidebar_snd
#
# @executed	as the player & at current position
#
# @within	mgs:v5.1.0/multiplayer/create_sidebar_snd
#			mgs:v5.1.0/multiplayer/gamemodes/snd/tick
#

# Which side is attacking
execute if score #snd_attackers mgs.data matches 1 run data modify storage mgs:temp snd_sb.atk set value '[[" ⚔ ",{"translate":"mgs.attack","color":"gray"}],{"translate":"mgs.red","color":"red"}]'
execute if score #snd_attackers mgs.data matches 2 run data modify storage mgs:temp snd_sb.atk set value '[[" ⚔ ",{"translate":"mgs.attack","color":"gray"}],{"translate":"mgs.blue","color":"blue"}]'

# Bomb state: on the ground, on someone's back, or ticking
execute if score #snd_bomb_state mgs.data matches 0 run data modify storage mgs:temp snd_sb.bomb set value '[[" 💣 ",{"translate":"mgs.bomb_2","color":"gray"}],{"translate":"mgs.loose","color":"gray"}]'
execute if score #snd_bomb_state mgs.data matches 0 if entity @a[tag=mgs.snd_carrier] run data modify storage mgs:temp snd_sb.bomb set value '[[" 💣 ",{"translate":"mgs.bomb_2","color":"gray"}],{"translate":"mgs.carried","color":"gold"}]'
execute if score #snd_bomb_state mgs.data matches 2 run data modify storage mgs:temp snd_sb.bomb set value '[[" 💣 ",{"translate":"mgs.bomb_2","color":"gray"}],{"translate":"mgs.planted","color":"red","bold":true}]'

function mgs:v5.1.0/multiplayer/build_sidebar_snd with storage mgs:temp snd_sb

