
#> mgs:leaderboard/level_mp
#
# @within	(public)
#

# A repeat command block runs this every tick; once a second is enough.
scoreboard players operation #lb_tick mgs.data = #total_tick mgs.data
scoreboard players operation #lb_tick mgs.data %= #20 mgs.data
execute unless score #lb_tick mgs.data matches 0 run return 0
data modify storage mgs:temp _lb_cb set value {kind:"level_mp",path:'level_mp',title:"Multiplayer Level"}
execute positioned ~ ~0.5 ~ run function mgs:v5.4.1/stats/board/hologram

