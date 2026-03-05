
#> mgs:v5.0.0/multiplayer/on_kill_signal
#
# @within	#mgs:signals/on_kill
#

# Only process if multiplayer game is active
execute unless data storage mgs:multiplayer game{state:"active"} run return fail

# Dispatch to gamemode-specific kill handler
execute if data storage mgs:multiplayer game{gamemode:"ffa"} run return run function mgs:v5.0.0/multiplayer/gamemodes/ffa/on_kill
execute if data storage mgs:multiplayer game{gamemode:"tdm"} run return run function mgs:v5.0.0/multiplayer/gamemodes/tdm/on_kill
execute if data storage mgs:multiplayer game{gamemode:"dom"} run return run function mgs:v5.0.0/multiplayer/gamemodes/dom/on_kill
execute if data storage mgs:multiplayer game{gamemode:"hp"} run return run function mgs:v5.0.0/multiplayer/gamemodes/hp/on_kill
execute if data storage mgs:multiplayer game{gamemode:"snd"} run return run function mgs:v5.0.0/multiplayer/gamemodes/snd/on_kill

