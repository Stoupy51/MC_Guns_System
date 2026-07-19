
#> mgs:v5.1.0/zombies/watchdog_tick
#
# @within	mgs:v5.1.0/zombies/game_tick
#

# Progress fingerprint: any spawn, kill, or portal strike moves it.
scoreboard players operation #zb_wd_fp mgs.data = #zb_alive mgs.data
scoreboard players operation #zb_wd_fp mgs.data += #zb_to_spawn mgs.data
scoreboard players operation #zb_wd_fp mgs.data += #zb_dog_pending mgs.data

# Anything alive counts as progress on its own: kiting a horde is a normal, arbitrarily long state,
# and unreachable zombies are already handled by the stuck escort/glow system.
scoreboard players set #zb_wd_moved mgs.data 0
execute if score #zb_alive mgs.data matches 1.. run scoreboard players set #zb_wd_moved mgs.data 1
execute unless score #zb_wd_fp mgs.data = #zb_wd_last mgs.data run scoreboard players set #zb_wd_moved mgs.data 1
scoreboard players operation #zb_wd_last mgs.data = #zb_wd_fp mgs.data

execute if score #zb_wd_moved mgs.data matches 1 run scoreboard players set #zb_wd_ticks mgs.data 0
execute if score #zb_wd_moved mgs.data matches 0 run scoreboard players add #zb_wd_ticks mgs.data 1

# 400 ticks = 20s, well past the 5s handoff so a healthy round can't trip it.
execute if score #zb_wd_ticks mgs.data matches 400.. run function mgs:zombies/recover

