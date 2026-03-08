
#> mgs:v5.0.0/zombies/game_over
#
# @within	mgs:v5.0.0/zombies/game_tick
#

# Set state to ended
data modify storage mgs:zombies game.state set value "ended"

# Title
title @a[scores={mgs.zb.in_game=1}] times 10 80 20
title @a[scores={mgs.zb.in_game=1}] title {"text":"GAME OVER","color":"dark_red","bold":true}

# Calculate final round
execute store result score #_final_round mgs.data run data get storage mgs:zombies game.round

# Performance summary
tellraw @a ["","\n",{"text":"═══════ GAME OVER ═══════","color":"dark_red","bold":true}]
tellraw @a ["",{"translate": "mgs.final_round","color":"gray"},{"score":{"name":"#_final_round","objective":"mgs.data"},"color":"red","bold":true}]

# Per-player stats
execute as @a[scores={mgs.zb.in_game=1}] run tellraw @a ["",{"text":"  🎖 ","color":"gray"},{"selector":"@s","color":"yellow"}," — Kills: ",{"score":{"name":"@s","objective":"mgs.zb.kills"},"color":"green"}," | Downs: ",{"score":{"name":"@s","objective":"mgs.zb.downs"},"color":"red"}," | Points: ",{"score":{"name":"@s","objective":"mgs.zb.points"},"color":"gold"}]

tellraw @a ["",{"text":"═════════════════════════","color":"dark_red","bold":true},"\n"]

# Signal game end
function #mgs:zombies/on_game_end

# End game after 5 seconds
schedule function mgs:v5.0.0/zombies/stop 100t

