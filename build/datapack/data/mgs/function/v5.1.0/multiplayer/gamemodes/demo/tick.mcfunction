
#> mgs:v5.1.0/multiplayer/gamemodes/demo/tick
#
# @within	mgs:v5.1.0/multiplayer/game_tick
#

# Rebuilt once a second: the attacking side and each site's state are text. Above the round gate, so the gap shows the new round.
execute store result score #demo_sb_tick mgs.data run scoreboard players get #total_tick mgs.data
scoreboard players operation #demo_sb_tick mgs.data %= #20 mgs.data
execute if score #demo_sb_tick mgs.data matches 0 run function mgs:v5.1.0/multiplayer/refresh_sidebar_demo

execute unless score #demo_round_active mgs.data matches 1 run return 0

# Before the site channels, so a plant in progress overwrites it with its progress.
title @a[tag=mgs.demo_atk,gamemode=!spectator] actionbar [{"text":"💣 ","color":"white"},{"translate":"mgs.you_are_carrying_a_bomb_sneak_at_a_site_to_plant","color":"gold"}]

# Channels, then fuses, then the clock: a plant completing this tick must stop the clock before it can reach 0,
# or the defenders would win a round off a bomb that is already down.
execute as @e[tag=mgs.demo_obj,scores={mgs.demo_state=0}] at @s run function mgs:v5.1.0/multiplayer/gamemodes/demo/site_plant_tick
execute as @e[tag=mgs.demo_obj,scores={mgs.demo_state=1}] at @s run function mgs:v5.1.0/multiplayer/gamemodes/demo/site_defuse_tick
execute as @e[tag=mgs.demo_obj,scores={mgs.demo_state=1}] at @s run function mgs:v5.1.0/multiplayer/gamemodes/demo/site_fuse_tick

# One NBT write per planted site per second, on whole-second boundaries, with no extra per-entity objective.
execute store result score #demo_sec_tick mgs.data run scoreboard players get #total_tick mgs.data
scoreboard players operation #demo_sec_tick mgs.data %= #20 mgs.data
execute if score #demo_sec_tick mgs.data matches 0 as @e[tag=mgs.demo_obj,scores={mgs.demo_state=1}] at @s run function mgs:v5.1.0/multiplayer/gamemodes/demo/site_hud

# Ambient marker on the sites still standing.
execute at @e[tag=mgs.demo_obj,scores={mgs.demo_state=0}] run particle dust{color:[1.0,0.6,0.0],scale:1.0} ~ ~1 ~ 1.0 0.5 1.0 0 5

# The clock stops while a site is planted: the attackers get room to defend their plant, and expiry never fires on a bomb already down.
execute unless entity @e[tag=mgs.demo_obj,scores={mgs.demo_state=1}] run scoreboard players operation #demo_timer mgs.data -= #tick_delta mgs.data

# Expiry with anything standing is a defensive hold, decider included, so every round awards a point.
execute if score #demo_timer mgs.data matches ..0 run function mgs:v5.1.0/multiplayer/gamemodes/demo/defenders_win

# The HUD score this mode claimed.
scoreboard players operation #mp_timer mgs.data = #demo_timer mgs.data
execute if score #mp_timer mgs.data matches ..0 run scoreboard players set #mp_timer mgs.data 0

