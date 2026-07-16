
#> mgs:v5.1.0/zombies/game_over
#
# @within	mgs:v5.1.0/zombies/game_tick
#

# Set state to ended
data modify storage mgs:zombies game.state set value "ended"

# Title
title @a[scores={mgs.zb.in_game=1}] times 10 80 20
title @a[scores={mgs.zb.in_game=1}] title {"translate":"mgs.game_over_2","color":"dark_red","bold":true}

# Calculate final round
execute store result score #final_round mgs.data run data get storage mgs:zombies game.round

# Performance summary
tellraw @a ["","\n",[{"text":"═══════ ","color":"dark_red","bold":true}, {"translate":"mgs.game_over_2"}, " ═══════"]]
tellraw @a ["","  ","🧟 ",{"translate":"mgs.final_round","color":"gray"},{"score":{"name":"#final_round","objective":"mgs.data"},"color":"red","bold":true}]

# Per-player stats
execute as @a[scores={mgs.zb.in_game=1}] run tellraw @a ["","  ","🎖 ",{"selector":"@s","color":"yellow"}," — Kills: ",{"score":{"name":"@s","objective":"mgs.zb.kills"},"color":"green"}," | Downs: ",{"score":{"name":"@s","objective":"mgs.zb.downs"},"color":"red"}," | Points: ",{"score":{"name":"@s","objective":"mgs.zb.points"},"color":"gold"}]

tellraw @a ["",{"text":"═════════════════════════","color":"dark_red","bold":true},"\n"]

# Signal game end
function #mgs:zombies/on_game_end

# Stop all sounds and play gameover sound
stopsound @a
execute as @a[scores={mgs.zb.in_game=1}] at @s run playsound mgs:zombies/game_over ambient @s ~ ~ ~ 0.6 1.0

# End game after 5 seconds
schedule function mgs:v5.1.0/zombies/stop 100t

