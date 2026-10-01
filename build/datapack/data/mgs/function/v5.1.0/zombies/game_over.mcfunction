
#> mgs:v5.1.0/zombies/game_over
#
# @within	mgs:v5.1.0/zombies/game_tick
#

data modify storage mgs:zombies game.state set value "ended"

# The roster snapshot lets a fast restart work after the auto-stop clears in_game 5 s later (see zombies/restart).
tag @a remove mgs.zb_last_roster
tag @a[scores={mgs.zb.in_game=1}] add mgs.zb_last_roster

title @a[scores={mgs.zb.in_game=1}] times 10 80 20
title @a[scores={mgs.zb.in_game=1}] title {"translate":"mgs.game_over_2","color":"dark_red","bold":true}

execute store result score #final_round mgs.data run data get storage mgs:zombies game.round

# Paid here so the Final Round line can show the amount.
function mgs:v5.1.0/zombies/xp/on_game_over

# The Final Round line is split because only the roster earned the bonus.
tellraw @a ["","\n",{"translate":"mgs.game_over_2","color":"dark_red","bold":true}]
tellraw @a[scores={mgs.zb.in_game=1}] ["","  ","🧟 ",{"translate":"mgs.final_round","color":"gray"},{"score":{"name":"#final_round","objective":"mgs.data"},"color":"red","bold":true},[" ",{"text":"+","color":"gold"},{"score":{"name":"#xp_gain","objective":"mgs.data"},"color":"gold"},{"text":" XP","color":"gold"}]]
tellraw @a[scores={mgs.zb.in_game=0}] ["","  ","🧟 ",{"translate":"mgs.final_round","color":"gray"},{"score":{"name":"#final_round","objective":"mgs.data"},"color":"red","bold":true}]

# Best first; the bare selector component renders the team colour.
tag @a[scores={mgs.zb.in_game=1}] add mgs.stat_cand
function mgs:v5.1.0/zombies/announce_stats_iter
tag @a remove mgs.stat_cand

tellraw @a ""

function #mgs:zombies/on_game_end

stopsound @a
execute as @a[scores={mgs.zb.in_game=1}] at @s run playsound mgs:zombies/game_over ambient @s ~ ~ ~ 0.3 1.0

# suggest_command only runs at permission level 2, so the restart is operator-only.
tellraw @a ["",[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "]," ",[{"text": "[", "color": "green", "click_event": {"action": "suggest_command", "command": "/function mgs:v5.1.0/zombies/restart"}, "hover_event": {"action": "show_text", "value": "Restart with the same map, variant and players (operators only)"}}, "\u27f2 Fast Restart", "]"]]

schedule function mgs:v5.1.0/zombies/stop 100t

