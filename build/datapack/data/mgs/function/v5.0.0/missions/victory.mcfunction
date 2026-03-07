
#> mgs:v5.0.0/missions/victory
#
# @within	mgs:v5.0.0/missions/game_tick
#

# Calculate time in seconds
scoreboard players operation #_mi_seconds mgs.data = #mi_timer mgs.data
scoreboard players operation #_mi_seconds mgs.data /= #20 mgs.data

# Calculate minutes and remaining seconds
scoreboard players operation #_mi_minutes mgs.data = #_mi_seconds mgs.data
scoreboard players operation #_mi_minutes mgs.data /= #60 mgs.data
scoreboard players operation #_mi_rem_sec mgs.data = #_mi_seconds mgs.data
scoreboard players operation #_mi_rem_sec mgs.data %= #60 mgs.data

# Title
title @a[scores={mgs.mi.in_game=1}] times 10 80 20
title @a[scores={mgs.mi.in_game=1}] title {"text":"MISSION COMPLETE","color":"gold","bold":true}
title @a[scores={mgs.mi.in_game=1}] subtitle {"translate": "mgs.all_enemies_eliminated","color":"green"}

# Performance summary
tellraw @a ["","\n",{"translate": "mgs.mission_complete","color":"gold","bold":true}]
tellraw @a ["",{"translate": "mgs.time","color":"gray"},{"score":{"name":"#_mi_minutes","objective":"mgs.data"},"color":"yellow"},"m ",{"score":{"name":"#_mi_rem_sec","objective":"mgs.data"},"color":"yellow"},"s"]
tellraw @a ["",{"translate": "mgs.enemies_killed","color":"gray"},{"score":{"name":"#mi_total_enemies","objective":"mgs.data"},"color":"red"}]
tellraw @a ["",{"text":"═══════════════════════════════","color":"gold","bold":true},"\n"]

# End game
function mgs:v5.0.0/missions/stop

