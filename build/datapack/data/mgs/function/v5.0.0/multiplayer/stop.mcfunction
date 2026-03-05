
#> mgs:v5.0.0/multiplayer/stop
#
# @within	mgs:v5.0.0/multiplayer/team_wins
#			mgs:v5.0.0/multiplayer/game_draw
#			mgs:v5.0.0/multiplayer/gamemodes/ffa/player_wins
#

# End game
data modify storage mgs:multiplayer game.state set value "lobby"

# Cancel scheduled prep end (in case game stopped during prep)
schedule clear mgs:v5.0.0/multiplayer/end_prep

# Disable instant respawn
gamerule immediate_respawn false

# Restore movement (in case stopped during prep)
execute as @a[scores={mgs.mp.in_game=1}] run attribute @s minecraft:movement_speed base set 0.1
execute as @a[scores={mgs.mp.in_game=1}] run attribute @s minecraft:jump_strength base set 0.42

# Clear prep effects (in case stopped during prep)
effect clear @a[scores={mgs.mp.in_game=1}] darkness
effect clear @a[scores={mgs.mp.in_game=1}] blindness
effect clear @a[scores={mgs.mp.in_game=1}] night_vision

# Gamemode cleanup
execute if data storage mgs:multiplayer game{gamemode:"ffa"} run function mgs:v5.0.0/multiplayer/gamemodes/ffa/cleanup
execute if data storage mgs:multiplayer game{gamemode:"tdm"} run function mgs:v5.0.0/multiplayer/gamemodes/tdm/cleanup
execute if data storage mgs:multiplayer game{gamemode:"dom"} run function mgs:v5.0.0/multiplayer/gamemodes/dom/cleanup
execute if data storage mgs:multiplayer game{gamemode:"hp"} run function mgs:v5.0.0/multiplayer/gamemodes/hp/cleanup
execute if data storage mgs:multiplayer game{gamemode:"snd"} run function mgs:v5.0.0/multiplayer/gamemodes/snd/cleanup

# Kill gamemode entities
kill @e[tag=mgs.gm_entity]

# Signal game end
function #mgs:multiplayer/on_game_end

# Announce scores
tellraw @a ["",[{"text":"","color":"gold","bold":true},"⚔ ",{"translate": "mgs.game_over"},"! "]]
tellraw @a ["",{"translate": "mgs.red","color":"red"},{"text":": "},{"score":{"name":"#red","objective":"mgs.mp.team"}}," | ",{"translate": "mgs.blue","color":"blue"},{"text":": "},{"score":{"name":"#blue","objective":"mgs.mp.team"}}]

# Clear in-game state
scoreboard players set @a mgs.mp.in_game 0
scoreboard players set @a mgs.mp.team 0

