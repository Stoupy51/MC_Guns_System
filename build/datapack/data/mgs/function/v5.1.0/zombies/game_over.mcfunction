
#> mgs:v5.1.0/zombies/game_over
#
# @within	mgs:v5.1.0/zombies/game_tick
#

# Set state to ended
data modify storage mgs:zombies game.state set value "ended"

# Snapshot the roster so a fast restart still works after the scheduled auto-stop clears
# mgs.zb.in_game 5 seconds from now (see zombies/restart).
tag @a remove mgs.zb_last_roster
tag @a[scores={mgs.zb.in_game=1}] add mgs.zb_last_roster

# Title
title @a[scores={mgs.zb.in_game=1}] times 10 80 20
title @a[scores={mgs.zb.in_game=1}] title {"translate":"mgs.game_over_2","color":"dark_red","bold":true}

# Calculate final round
execute store result score #final_round mgs.data run data get storage mgs:zombies game.round

# Performance summary
tellraw @a ["","\n",[{"text":"═══════ ","color":"dark_red","bold":true}, {"translate":"mgs.game_over_2"}, " ═══════"]]
tellraw @a ["","  ","🧟 ",{"translate":"mgs.final_round","color":"gray"},{"score":{"name":"#final_round","objective":"mgs.data"},"color":"red","bold":true}]

# Per-player stats, best first. The bare selector component renders the player's team colour.
tag @a[scores={mgs.zb.in_game=1}] add mgs.stat_cand
function mgs:v5.1.0/zombies/announce_stats_iter
tag @a remove mgs.stat_cand

tellraw @a ["",{"text":"═════════════════════════","color":"dark_red","bold":true},"\n"]

# Signal game end
function #mgs:zombies/on_game_end

# Stop all sounds and play gameover sound
stopsound @a
execute as @a[scores={mgs.zb.in_game=1}] at @s run playsound mgs:zombies/game_over ambient @s ~ ~ ~ 0.25 1.0

# Offer a one-click fast restart. suggest_command only runs at permission level 2, so it is a
# no-op for non-operators — exactly the operator-gated restart the design calls for.
tellraw @a ["",[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "]," ",[{"text": "[", "color": "green", "click_event": {"action": "suggest_command", "command": "/function mgs:v5.1.0/zombies/restart"}, "hover_event": {"action": "show_text", "value": "Restart with the same map, variant and players (operators only)"}}, "\u27f2 Fast Restart", "]"]]

# End game after 5 seconds
schedule function mgs:v5.1.0/zombies/stop 100t

