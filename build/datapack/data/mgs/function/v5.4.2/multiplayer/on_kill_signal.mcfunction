
#> mgs:v5.4.2/multiplayer/on_kill_signal
#
# @within	#mgs:signals/on_kill
#			mgs:v5.4.2/dialog/close_then
#

execute unless data storage mgs:multiplayer game{state:"active"} run return fail
execute unless score @s mgs.mp.in_game matches 1 run return fail

# The match is decided: a later kill of the same tick scores nothing and reaches no win path.
execute if score #mp_end_tick mgs.data matches 1.. run return fail

execute if data storage mgs:multiplayer game{gamemode:"ffa"} run return run function mgs:v5.4.2/multiplayer/gamemodes/ffa/on_kill
execute if data storage mgs:multiplayer game{gamemode:"tdm"} run return run function mgs:v5.4.2/multiplayer/gamemodes/tdm/on_kill
execute if data storage mgs:multiplayer game{gamemode:"dom"} run return run function mgs:v5.4.2/multiplayer/gamemodes/dom/on_kill
execute if data storage mgs:multiplayer game{gamemode:"hp"} run return run function mgs:v5.4.2/multiplayer/gamemodes/hp/on_kill
execute if data storage mgs:multiplayer game{gamemode:"snd"} run return run function mgs:v5.4.2/multiplayer/gamemodes/snd/on_kill
execute if data storage mgs:multiplayer game{gamemode:"demo"} run return run function mgs:v5.4.2/multiplayer/gamemodes/demo/on_kill

