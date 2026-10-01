
#> mgs:v5.1.0/multiplayer/gamemodes/snd/tick
#
# @within	mgs:v5.1.0/multiplayer/game_tick
#

# Rebuilt once a second: the attacking side and the bomb state are text, which no score component can show.
# Above the round gate, so the new round and swapped sides show during the 3 s gap.
execute store result score #snd_sb_tick mgs.data run scoreboard players get #total_tick mgs.data
scoreboard players operation #snd_sb_tick mgs.data %= #20 mgs.data
execute if score #snd_sb_tick mgs.data matches 0 run function mgs:v5.1.0/multiplayer/refresh_sidebar_snd

# Nothing to judge between rounds: next_round clears snd_alive, so every side would read as wiped.
execute unless score #snd_round_active mgs.data matches 1 run return 0

scoreboard players operation #snd_round_timer mgs.data -= #tick_delta mgs.data

# Time out before a plant: defenders win.
execute if score #snd_round_timer mgs.data matches ..0 if score #snd_bomb_state mgs.data matches 0 run function mgs:v5.1.0/multiplayer/gamemodes/snd/defenders_win

execute if score #snd_bomb_state mgs.data matches 2 run scoreboard players operation #snd_bomb_timer mgs.data -= #tick_delta mgs.data
execute if score #snd_bomb_state mgs.data matches 2 if score #snd_bomb_timer mgs.data matches ..0 run function mgs:v5.1.0/multiplayer/gamemodes/snd/bomb_explodes

# The HUD shows the round clock, then the fuse once the bomb is down (the round timer stops mattering then).
# A plant with 20 s left therefore raises the displayed time to the 45 s fuse.
scoreboard players operation #mp_timer mgs.data = #snd_round_timer mgs.data
execute if score #snd_bomb_state mgs.data matches 2 run scoreboard players operation #mp_timer mgs.data = #snd_bomb_timer mgs.data
execute if score #mp_timer mgs.data matches ..0 run scoreboard players set #mp_timer mgs.data 0

# A text_display resolves score components when its data is sent, so it would freeze at the planted value;
# rewriting on each whole second costs one NBT write a second.
execute if score #snd_bomb_state mgs.data matches 2 run scoreboard players operation #snd_bomb_sec mgs.data = #snd_bomb_timer mgs.data
execute if score #snd_bomb_state mgs.data matches 2 run scoreboard players operation #snd_bomb_sec mgs.data /= #20 mgs.data
execute if score #snd_bomb_state mgs.data matches 2 unless score #snd_bomb_sec mgs.data = #snd_bomb_sec_shown mgs.data run function mgs:v5.1.0/multiplayer/gamemodes/snd/update_bomb_hud

# Attackers wiped before the plant: defenders win. After the plant someone still has to defuse.
execute store result score #snd_atk_alive mgs.data if entity @a[tag=mgs.snd_alive,scores={mgs.mp.team=1}]
execute if score #snd_attackers mgs.data matches 2 store result score #snd_atk_alive mgs.data if entity @a[tag=mgs.snd_alive,scores={mgs.mp.team=2}]
execute if score #snd_atk_alive mgs.data matches 0 if score #snd_bomb_state mgs.data matches 0 run function mgs:v5.1.0/multiplayer/gamemodes/snd/defenders_win

# Defenders wiped: attackers win, planted or not, since nobody is left to defuse.
execute store result score #snd_def_alive mgs.data if entity @a[tag=mgs.snd_alive,scores={mgs.mp.team=2}]
execute if score #snd_attackers mgs.data matches 2 store result score #snd_def_alive mgs.data if entity @a[tag=mgs.snd_alive,scores={mgs.mp.team=1}]
execute if score #snd_def_alive mgs.data matches 0 run function mgs:v5.1.0/multiplayer/gamemodes/snd/attackers_win

execute at @e[tag=mgs.snd_obj] run particle dust{color:[1.0,0.6,0.0],scale:1.0} ~ ~1 ~ 1.0 0.5 1.0 0 5

# The carrier's label follows them; see_through is off, so it does not reveal the carrier through walls (as in CoD).
execute as @a[tag=mgs.snd_carrier] at @s run tp @e[tag=mgs.snd_carrier_label,limit=1] ~ ~2.2 ~
title @a[tag=mgs.snd_carrier] actionbar [{"text":"💣 ","color":"white"},{"translate":"mgs.you_have_the_bomb_plant_at_a_site","color":"gold"}]

# A carrier who disconnects leaves no bomb and no carrier, which would end the attack for the round; their label stays, so the bomb drops there.
execute if score #snd_bomb_state mgs.data matches 0 unless entity @a[tag=mgs.snd_carrier] if entity @e[tag=mgs.snd_carrier_label] run function mgs:v5.1.0/multiplayer/gamemodes/snd/recover_bomb

# Any living attacker walking over a loose bomb collects it.
execute if score #snd_bomb_state mgs.data matches 0 unless entity @a[tag=mgs.snd_carrier] as @a[tag=mgs.snd_alive,gamemode=!spectator] at @s if entity @e[tag=mgs.snd_loose_at,distance=..2.0] run function mgs:v5.1.0/multiplayer/gamemodes/snd/try_pickup

# Only the carrier, sneaking at a site. The channeler only raises a flag; progress advances once here (see defuse).
scoreboard players set #snd_channeling mgs.data 0
execute if score #snd_bomb_state mgs.data matches 0 as @a[tag=mgs.snd_carrier,tag=mgs.snd_alive,predicate=mgs:v5.1.0/is_sneaking,gamemode=!spectator] at @s if entity @e[tag=mgs.snd_obj,distance=..3.0] run function mgs:v5.1.0/multiplayer/gamemodes/snd/try_plant
execute if score #snd_bomb_state mgs.data matches 0 if score #snd_channeling mgs.data matches 0 run scoreboard players set #snd_plant_progress mgs.data 0
execute if score #snd_bomb_state mgs.data matches 0 if score #snd_channeling mgs.data matches 1 run scoreboard players operation #snd_plant_progress mgs.data += #tick_delta mgs.data
execute if score #snd_bomb_state mgs.data matches 0 if score #snd_plant_progress mgs.data matches 100.. as @a[tag=mgs.snd_carrier,limit=1] at @s run function mgs:v5.1.0/multiplayer/gamemodes/snd/bomb_planted

# Defender sneaking at the bomb; progress resets when nobody channels. The += lives here, not in try_defuse:
# per player, two defenders halved the defuse time. try_defuse marks the channelers, so bomb_defused knows who to pay.
scoreboard players set #snd_channeling mgs.data 0
tag @a remove mgs.xp_earner
execute if score #snd_bomb_state mgs.data matches 2 as @a[tag=mgs.snd_alive,predicate=mgs:v5.1.0/is_sneaking,gamemode=!spectator] at @s if entity @e[tag=mgs.snd_bomb,distance=..3.0] run function mgs:v5.1.0/multiplayer/gamemodes/snd/try_defuse
execute if score #snd_bomb_state mgs.data matches 2 if score #snd_channeling mgs.data matches 0 run scoreboard players set #snd_defuse_progress mgs.data 0
execute if score #snd_bomb_state mgs.data matches 2 if score #snd_channeling mgs.data matches 1 run scoreboard players operation #snd_defuse_progress mgs.data += #tick_delta mgs.data
execute if score #snd_bomb_state mgs.data matches 2 if score #snd_defuse_progress mgs.data matches 150.. run function mgs:v5.1.0/multiplayer/gamemodes/snd/bomb_defused

