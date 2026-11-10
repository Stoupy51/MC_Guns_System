
#> mgs:v5.4.1/multiplayer/stop
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/multiplayer/end
#			mgs:v5.4.1/multiplayer/kill_cam/post_roll
#

execute unless score #in_multiplayer_map mgs.data matches 1 run return run function mgs:v5.4.1/shared/enter_map {mode:"multiplayer",fn:"mgs:v5.4.1/multiplayer/stop"}

function mgs:v5.4.1/multiplayer/kill_cam/cleanup

# Map scripts only run during a match, so the leave script comes before the lobby state.
execute as @a[scores={mgs.mp.in_game=1}] run function mgs:v5.4.1/shared/maps/call_script_at_base {mode:"multiplayer",script:"leave"}

data modify storage mgs:multiplayer game.state set value "lobby"
scoreboard players set #mp_end_tick mgs.data 0
schedule clear mgs:v5.4.1/multiplayer/end_prep

# Mode cleanup before the multiplayer_entity sweep: S&D restores its sites with `execute at @e[tag=snd_obj] run fill`,
# which needs the markers to still exist.
execute if data storage mgs:multiplayer game{gamemode:"ffa"} run function mgs:v5.4.1/multiplayer/gamemodes/ffa/cleanup
execute if data storage mgs:multiplayer game{gamemode:"tdm"} run function mgs:v5.4.1/multiplayer/gamemodes/tdm/cleanup
execute if data storage mgs:multiplayer game{gamemode:"dom"} run function mgs:v5.4.1/multiplayer/gamemodes/dom/cleanup
execute if data storage mgs:multiplayer game{gamemode:"hp"} run function mgs:v5.4.1/multiplayer/gamemodes/hp/cleanup
execute if data storage mgs:multiplayer game{gamemode:"snd"} run function mgs:v5.4.1/multiplayer/gamemodes/snd/cleanup
execute if data storage mgs:multiplayer game{gamemode:"demo"} run function mgs:v5.4.1/multiplayer/gamemodes/demo/cleanup
kill @e[tag=mgs.multiplayer_entity]
function #mgs:multiplayer/on_game_end

scoreboard players set #any_game_active mgs.data 0
execute if data storage mgs:multiplayer game.state unless data storage mgs:multiplayer game{state:"lobby"} run scoreboard players set #any_game_active mgs.data 1
execute if data storage mgs:missions game.state unless data storage mgs:missions game{state:"lobby"} run scoreboard players set #any_game_active mgs.data 1
execute if data storage mgs:zombies game.state unless data storage mgs:zombies game{state:"lobby"} run scoreboard players set #any_game_active mgs.data 1
execute if score #any_game_active mgs.data matches 0 run gamerule natural_health_regeneration true

# Stop any hunger drain and refill the bar, so nobody is left winded.
effect clear @a[scores={mgs.mp.in_game=1}] minecraft:hunger
effect give @a[scores={mgs.mp.in_game=1}] minecraft:saturation 5 20 true
scoreboard players set @a[scores={mgs.mp.in_game=1}] mgs.stam_out 0
scoreboard players set @a[scores={mgs.mp.in_game=1}] mgs.stam_seen 0

# Every shader id off, so nothing survives into the lobby.
execute as @a[scores={mgs.mp.in_game=1}] run function mgs:v5.4.1/player/fx_reset

# Team scores mean nothing in FFA; player_wins announces the winner.
tellraw @a[scores={mgs.mp.in_game=1}] ["","⚔ ",[{"text":"","color":"gold","bold":true},{"translate":"mgs.game_over","fallback":"Game Over"},"! "]]
execute unless data storage mgs:multiplayer game{gamemode:"ffa"} run tellraw @a[scores={mgs.mp.in_game=1}] ["",{"translate":"mgs.red","fallback":"Red","color":"red"},{"text":": "},{"score":{"name":"#red","objective":"mgs.mp.team"}}," | ",{"translate":"mgs.blue","fallback":"Blue","color":"blue"},{"text":": "},{"score":{"name":"#blue","objective":"mgs.mp.team"}}]

# Best first; the bare selector shows the team colour, which still applies until reset_player below.
tag @a[scores={mgs.mp.in_game=1}] add mgs.stat_cand
function mgs:v5.4.1/multiplayer/announce_stats_iter
tag @a remove mgs.stat_cand

scoreboard objectives setdisplay sidebar.team.red
scoreboard objectives setdisplay sidebar.team.blue
scoreboard objectives setdisplay sidebar.team.gold
scoreboard objectives remove mgs.sidebar
scoreboard objectives setdisplay list

execute as @a[scores={mgs.mp.in_game=1}] run function mgs:v5.4.1/multiplayer/reset_player
scoreboard players set #mp_has_boundary mgs.data 0

