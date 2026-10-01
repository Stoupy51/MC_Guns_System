
#> mgs:v5.1.0/multiplayer/stop
#
# @within	mgs:v5.1.0/multiplayer/team_wins
#			mgs:v5.1.0/multiplayer/game_draw
#			mgs:v5.1.0/multiplayer/gamemodes/ffa/player_wins
#			dialog mgs:v5.1.0/multiplayer/setup
#

data modify storage mgs:multiplayer game.state set value "lobby"
schedule clear mgs:v5.1.0/multiplayer/end_prep
execute as @a[scores={mgs.mp.in_game=1}] run attribute @s minecraft:movement_speed base reset
execute as @a[scores={mgs.mp.in_game=1}] run attribute @s minecraft:jump_strength base reset
execute as @a[scores={mgs.mp.in_game=1}] run attribute @s minecraft:waypoint_receive_range base reset
effect clear @a[scores={mgs.mp.in_game=1}] darkness
effect clear @a[scores={mgs.mp.in_game=1}] blindness
effect clear @a[scores={mgs.mp.in_game=1}] night_vision
gamemode adventure @a[scores={mgs.mp.in_game=1},gamemode=spectator]

# Mode cleanup before the gm_entity sweep: S&D restores its sites with `execute at @e[tag=snd_obj] run fill`,
# which needs the markers to still exist.
execute if data storage mgs:multiplayer game{gamemode:"ffa"} run function mgs:v5.1.0/multiplayer/gamemodes/ffa/cleanup
execute if data storage mgs:multiplayer game{gamemode:"tdm"} run function mgs:v5.1.0/multiplayer/gamemodes/tdm/cleanup
execute if data storage mgs:multiplayer game{gamemode:"dom"} run function mgs:v5.1.0/multiplayer/gamemodes/dom/cleanup
execute if data storage mgs:multiplayer game{gamemode:"hp"} run function mgs:v5.1.0/multiplayer/gamemodes/hp/cleanup
execute if data storage mgs:multiplayer game{gamemode:"snd"} run function mgs:v5.1.0/multiplayer/gamemodes/snd/cleanup
execute if data storage mgs:multiplayer game{gamemode:"demo"} run function mgs:v5.1.0/multiplayer/gamemodes/demo/cleanup
kill @e[tag=mgs.gm_entity]
function #mgs:multiplayer/on_game_end

# Re-enable natural regeneration, disable custom regen system
gamerule natural_health_regeneration true
scoreboard players set #any_game_active mgs.data 0

# Tear down stamina state: stop any hunger drain and refill the bar so nobody is left winded
effect clear @a minecraft:hunger
effect give @a minecraft:saturation 5 20 true
scoreboard players set @a mgs.stam_out 0
scoreboard players set @a mgs.stam_seen 0

# Take every shader id back off, so nothing survives into the lobby
execute as @a run function mgs:v5.1.0/player/fx_reset

# Team scores mean nothing in FFA; player_wins announces the winner.
tellraw @a ["","⚔ ",[{"text":"","color":"gold","bold":true},{"translate":"mgs.game_over"},"! "]]
execute unless data storage mgs:multiplayer game{gamemode:"ffa"} run tellraw @a ["",{"translate":"mgs.red","color":"red"},{"text":": "},{"score":{"name":"#red","objective":"mgs.mp.team"}}," | ",{"translate":"mgs.blue","color":"blue"},{"text":": "},{"score":{"name":"#blue","objective":"mgs.mp.team"}}]

# Best first; the bare selector shows the team colour, which still applies before the team leave below.
tag @a[scores={mgs.mp.in_game=1}] add mgs.stat_cand
function mgs:v5.1.0/multiplayer/announce_stats_iter
tag @a remove mgs.stat_cand

scoreboard objectives setdisplay sidebar
scoreboard objectives remove mgs.sidebar
scoreboard objectives setdisplay list
team leave @a[team=mgs.red]
team leave @a[team=mgs.blue]
team leave @a[team=mgs.ffa]

# The state is still active or preparing here.
execute as @a[scores={mgs.mp.in_game=1}] run function mgs:v5.1.0/shared/maps/call_script_at_base {script:"leave"}

scoreboard players set @a mgs.mp.in_game 0
scoreboard players set @a mgs.mp.team 0
scoreboard players set @a mgs.mp.spectate_timer 0
scoreboard players set #mp_has_boundary mgs.data 0
tag @a[tag=mgs.give_class_menu] remove mgs.give_class_menu

