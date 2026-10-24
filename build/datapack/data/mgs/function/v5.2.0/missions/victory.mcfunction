
#> mgs:v5.2.0/missions/victory
#
# @within	mgs:v5.2.0/missions/game_tick
#

# Mission kills from the totalKillCount delta.
execute as @a[scores={mgs.mi.in_game=1}] run scoreboard players operation @s mgs.mi.kills = @s mgs.mi.kill_total
execute as @a[scores={mgs.mi.in_game=1}] run scoreboard players operation @s mgs.mi.kills -= @s mgs.mi.kill_base

# Missions have no XP award to ride, so the challenge counters are fed here, where mi.kills is final.
execute as @a[scores={mgs.mi.in_game=1}] run scoreboard players add @s mgs.adv.mi.completed 1
execute as @a[scores={mgs.mi.in_game=1}] run function mgs:v5.2.0/progression/adv/mi/completed/check
execute as @a[scores={mgs.mi.in_game=1}] run scoreboard players operation @s mgs.adv.mi.kills += @s mgs.mi.kills
execute as @a[scores={mgs.mi.in_game=1}] run function mgs:v5.2.0/progression/adv/mi/kills/check
execute as @a[scores={mgs.mi.in_game=1,mgs.mi.deaths=0}] run advancement grant @s only mgs:challenges/mi/flawless

scoreboard players operation #mi_seconds mgs.data = #mi_timer mgs.data
scoreboard players operation #mi_seconds mgs.data /= #20 mgs.data

scoreboard players operation #mi_minutes mgs.data = #mi_seconds mgs.data
scoreboard players operation #mi_minutes mgs.data /= #60 mgs.data
scoreboard players operation #mi_rem_sec mgs.data = #mi_seconds mgs.data
scoreboard players operation #mi_rem_sec mgs.data %= #60 mgs.data

title @a[scores={mgs.mi.in_game=1}] times 10 80 20
title @a[scores={mgs.mi.in_game=1}] title {"translate":"mgs.mission_complete","fallback":"MISSION COMPLETE","color":"gold","bold":true}
title @a[scores={mgs.mi.in_game=1}] subtitle {"translate":"mgs.all_enemies_eliminated","fallback":"All enemies eliminated!","color":"green"}

tellraw @a[scores={mgs.mi.in_game=1}] ["","\n",{"translate":"mgs.mission_complete","fallback":"MISSION COMPLETE","color":"gold","bold":true}]
tellraw @a[scores={mgs.mi.in_game=1}] ["","  ","⏱ ",{"translate":"mgs.time","fallback":"Time: ","color":"gray"},{"score":{"name":"#mi_minutes","objective":"mgs.data"},"color":"yellow"},"m ",{"score":{"name":"#mi_rem_sec","objective":"mgs.data"},"color":"yellow"},"s"]
tellraw @a[scores={mgs.mi.in_game=1}] ["","  ","💀 ",{"translate":"mgs.enemies_killed","fallback":"Enemies killed: ","color":"gray"},{"score":{"name":"#mi_total_enemies","objective":"mgs.data"},"color":"red"}]

# Each line carries the completion XP.
execute as @a[scores={mgs.mi.in_game=1}] run tellraw @a[scores={mgs.mi.in_game=1}] ["","  ","🎖 ",["",{"text":"[","color":"dark_gray"},{"score":{"name":"@s","objective":"mgs.mp.xp_level"},"color":"gold"},{"text":"] ","color":"dark_gray"},{"selector":"@s","color":"yellow"}]," | Kills: ",{"score":{"name":"@s","objective":"mgs.mi.kills"},"color":"green"}," | Deaths: ",{"score":{"name":"@s","objective":"mgs.mi.deaths"},"color":"red"},[" ",{"text":"+50 XP","color":"gold"}]]
execute as @a[scores={mgs.mi.in_game=1}] run function mgs:v5.2.0/progression/mp/award_mission_complete

tellraw @a[scores={mgs.mi.in_game=1}] ""

function mgs:v5.2.0/missions/stop

