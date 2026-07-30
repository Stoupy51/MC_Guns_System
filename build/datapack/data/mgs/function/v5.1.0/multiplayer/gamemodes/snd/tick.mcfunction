
#> mgs:v5.1.0/multiplayer/gamemodes/snd/tick
#
# @within	mgs:v5.1.0/multiplayer/game_tick
#

# Nothing to tick between rounds, and critically nothing to JUDGE: next_round clears snd_alive, so every
# check below would read one side as wiped during the 60-tick gap before start_round.
execute unless score #snd_round_active mgs.data matches 1 run return 0

# Round timer
scoreboard players operation #snd_round_timer mgs.data -= #tick_delta mgs.data

# If timer runs out before the bomb is planted, defenders win
execute if score #snd_round_timer mgs.data matches ..0 if score #snd_bomb_state mgs.data matches 0 run function mgs:v5.1.0/multiplayer/gamemodes/snd/defenders_win

# If bomb planted, tick bomb timer
execute if score #snd_bomb_state mgs.data matches 2 run scoreboard players operation #snd_bomb_timer mgs.data -= #tick_delta mgs.data
execute if score #snd_bomb_state mgs.data matches 2 if score #snd_bomb_timer mgs.data matches ..0 run function mgs:v5.1.0/multiplayer/gamemodes/snd/bomb_explodes

# Live countdown on the planted bomb. A score component would be wrong here: a text_display resolves its
# components when the entity data is sent, not continuously, so it would freeze at the planted value.
# Rewriting only when the whole second changes keeps that to one NBT write a second.
execute if score #snd_bomb_state mgs.data matches 2 run scoreboard players operation #snd_bomb_sec mgs.data = #snd_bomb_timer mgs.data
execute if score #snd_bomb_state mgs.data matches 2 run scoreboard players operation #snd_bomb_sec mgs.data /= #20 mgs.data
execute if score #snd_bomb_state mgs.data matches 2 unless score #snd_bomb_sec mgs.data = #snd_bomb_sec_shown mgs.data run function mgs:v5.1.0/multiplayer/gamemodes/snd/update_bomb_hud

# Check if all attackers are dead (defenders win). Only BEFORE the plant: once the bomb is down, wiping
# the attackers is not enough on its own — someone still has to walk up and defuse it.
execute store result score #snd_atk_alive mgs.data if entity @a[tag=mgs.snd_alive,scores={mgs.mp.team=1}]
execute if score #snd_attackers mgs.data matches 2 store result score #snd_atk_alive mgs.data if entity @a[tag=mgs.snd_alive,scores={mgs.mp.team=2}]
execute if score #snd_atk_alive mgs.data matches 0 if score #snd_bomb_state mgs.data matches 0 run function mgs:v5.1.0/multiplayer/gamemodes/snd/defenders_win

# Check if all defenders are dead (attackers win). Deliberately NOT gated on the bomb state: wiping the
# defenders wins the round outright, planted or not, because nobody is left who could ever defuse.
execute store result score #snd_def_alive mgs.data if entity @a[tag=mgs.snd_alive,scores={mgs.mp.team=2}]
execute if score #snd_attackers mgs.data matches 2 store result score #snd_def_alive mgs.data if entity @a[tag=mgs.snd_alive,scores={mgs.mp.team=1}]
execute if score #snd_def_alive mgs.data matches 0 run function mgs:v5.1.0/multiplayer/gamemodes/snd/attackers_win

# Particles at objectives
execute at @e[tag=mgs.snd_obj] run particle dust{color:[1.0,0.6,0.0],scale:1.0} ~ ~1 ~ 1.0 0.5 1.0 0 5

# Keep the carrier's bomb marker on their back, and remind them they are the one holding it.
# see_through is false on that label so it does NOT wallhack the carrier to the defenders: in CoD you spot
# the bomb on their model when you can already see them, you are not handed their position.
execute as @a[tag=mgs.snd_carrier] at @s run tp @e[tag=mgs.snd_carrier_label,limit=1] ~ ~2.2 ~
title @a[tag=mgs.snd_carrier] actionbar [{"translate":"mgs.you_have_the_bomb_plant_at_a_site","color":"gold"}]

# Loose bomb: any living attacker who walks over it collects it. No channel, no keypress.
execute if score #snd_bomb_state mgs.data matches 0 unless entity @a[tag=mgs.snd_carrier] as @a[tag=mgs.snd_alive,gamemode=!spectator] at @s if entity @e[tag=mgs.snd_loose_at,distance=..2.0] run function mgs:v5.1.0/multiplayer/gamemodes/snd/try_pickup

# Check planting (the CARRIER only, sneaking at a site); progress resets if nobody is channeling
scoreboard players set #snd_channeling mgs.data 0
execute if score #snd_bomb_state mgs.data matches 0 as @a[tag=mgs.snd_carrier,tag=mgs.snd_alive,predicate=mgs:v5.1.0/is_sneaking,gamemode=!spectator] at @s if entity @e[tag=mgs.snd_obj,distance=..3.0] run function mgs:v5.1.0/multiplayer/gamemodes/snd/try_plant
execute if score #snd_bomb_state mgs.data matches 0 if score #snd_channeling mgs.data matches 0 run scoreboard players set #snd_plant_progress mgs.data 0

# Check defusing (defender near bomb and sneaking); progress resets if nobody is channeling
scoreboard players set #snd_channeling mgs.data 0
execute if score #snd_bomb_state mgs.data matches 2 as @a[tag=mgs.snd_alive,predicate=mgs:v5.1.0/is_sneaking,gamemode=!spectator] at @s if entity @e[tag=mgs.snd_bomb,distance=..3.0] run function mgs:v5.1.0/multiplayer/gamemodes/snd/try_defuse
execute if score #snd_bomb_state mgs.data matches 2 if score #snd_channeling mgs.data matches 0 run scoreboard players set #snd_defuse_progress mgs.data 0

