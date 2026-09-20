
#> mgs:v5.1.0/multiplayer/gamemodes/demo/site_hud
#
# @executed	as @e[tag=mgs.demo_obj,scores={mgs.demo_state=1}] & at @s
#
# @within	mgs:v5.1.0/multiplayer/gamemodes/demo/tick [ as @e[tag=mgs.demo_obj,scores={mgs.demo_state=1}] & at @s ]
#

scoreboard players operation #demo_sec mgs.data = @s mgs.demo_fuse
scoreboard players operation #demo_sec mgs.data /= #20 mgs.data
execute store result storage mgs:temp _demo_hud.sec int 1 run scoreboard players get #demo_sec mgs.data
function mgs:v5.1.0/multiplayer/gamemodes/demo/set_site_hud with storage mgs:temp _demo_hud

