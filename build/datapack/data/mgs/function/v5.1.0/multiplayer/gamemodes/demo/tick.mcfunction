
#> mgs:v5.1.0/multiplayer/gamemodes/demo/tick
#
# @within	mgs:v5.1.0/multiplayer/game_tick
#

# Sidebar: rebuilt once a second because the attacking side and each site's state are text, which no score
# component can express. Above the round gate so the new round and the swapped sides show during the gap.
execute store result score #demo_sb_tick mgs.data run scoreboard players get #total_tick mgs.data
scoreboard players operation #demo_sb_tick mgs.data %= #20 mgs.data
execute if score #demo_sb_tick mgs.data matches 0 run function mgs:v5.1.0/multiplayer/refresh_sidebar_demo

# Nothing to tick, and nothing to judge, between rounds
execute unless score #demo_round_active mgs.data matches 1 run return 0

# Channels first, fuses second, and the clock LAST (see the clock block below): a plant that completes on
# this tick has to have stopped the clock before the clock is allowed to reach 0, otherwise the defenders
# steal a round off a bomb that is already down.
execute as @e[tag=mgs.demo_obj,scores={mgs.demo_state=0}] at @s run function mgs:v5.1.0/multiplayer/gamemodes/demo/site_plant_tick
execute as @e[tag=mgs.demo_obj,scores={mgs.demo_state=1}] at @s run function mgs:v5.1.0/multiplayer/gamemodes/demo/site_defuse_tick
execute as @e[tag=mgs.demo_obj,scores={mgs.demo_state=1}] at @s run function mgs:v5.1.0/multiplayer/gamemodes/demo/site_fuse_tick

# One NBT write per planted site per second. Rewriting on a whole-second boundary rather than tracking a
# "last shown" value per site keeps the same cost without a fifth per-entity objective.
execute store result score #demo_sec_tick mgs.data run scoreboard players get #total_tick mgs.data
scoreboard players operation #demo_sec_tick mgs.data %= #20 mgs.data
execute if score #demo_sec_tick mgs.data matches 0 as @e[tag=mgs.demo_obj,scores={mgs.demo_state=1}] at @s run function mgs:v5.1.0/multiplayer/gamemodes/demo/site_hud

# Ambient marker on whatever is still standing
execute at @e[tag=mgs.demo_obj,scores={mgs.demo_state=0}] run particle dust{color:[1.0,0.6,0.0],scale:1.0} ~ ~1 ~ 1.0 0.5 1.0 0 5

# The clock stops dead while any site is planted — that is the rule that gives the attackers room to
# defend their own plant, and it also means the expiry below can never fire on a bomb already down.
execute unless entity @e[tag=mgs.demo_obj,scores={mgs.demo_state=1}] run scoreboard players operation #demo_timer mgs.data -= #tick_delta mgs.data

# Expiry means a defensive hold in regulation — but overtime has no defenders, so there is nobody to award
# it to: #demo_attackers still names whoever attacked in the second half, and crediting that side would
# have put a phantom round win in the final score of what is really a draw.
execute if score #demo_timer mgs.data matches ..0 if score #demo_round mgs.data matches ..2 run function mgs:v5.1.0/multiplayer/gamemodes/demo/defenders_win
execute if score #demo_timer mgs.data matches ..0 if score #demo_round mgs.data matches 3.. run function mgs:v5.1.0/multiplayer/gamemodes/demo/overtime_expired

# Mirror the round clock onto the HUD score this mode claimed
scoreboard players operation #mp_timer mgs.data = #demo_timer mgs.data
execute if score #mp_timer mgs.data matches ..0 run scoreboard players set #mp_timer mgs.data 0

# Remind the armed side what they are holding
title @a[tag=mgs.demo_atk,gamemode=!spectator] actionbar [{"translate":"mgs.you_are_carrying_a_bomb_plant_at_a_site","color":"gold"}]

