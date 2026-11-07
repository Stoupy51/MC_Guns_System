
#> mgs:leaderboard/zb_map
#
# @within	(public)
#
# @args		map (unknown)
#			players (unknown)
#

# A repeat command block runs this every tick; once a second is enough.
scoreboard players operation #lb_tick mgs.data = #total_tick mgs.data
scoreboard players operation #lb_tick mgs.data %= #20 mgs.data
execute unless score #lb_tick mgs.data matches 0 run return 0
$data modify storage mgs:temp _lb_cb set value {kind:"zb_map",path:'zb_map."$(map)"."$(players)"',title:"Best Rounds: $(map)"}
execute positioned ~ ~0.5 ~ run function mgs:v5.4.0/stats/board/hologram

