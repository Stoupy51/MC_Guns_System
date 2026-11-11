
#> mgs:v5.4.2/zombies/preload_complete
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/start 20t [ scheduled ]
#

execute unless score #in_zombies_map mgs.data matches 1 run return run function mgs:v5.4.2/shared/enter_map {mode:"zombies",fn:"mgs:v5.4.2/zombies/preload_complete"}

execute unless data storage mgs:zombies game{state:"preparing"} run return fail

execute as @a[scores={mgs.zb.in_game=1}] run gamemode adventure @s

execute if data storage mgs:zombies game.map.out_of_bounds run function mgs:v5.4.2/shared/summon_oob {mode:"zombies"}

function mgs:v5.4.2/zombies/summon_spawns

function #mgs:zombies/on_game_start

# After the entity and setup summons.
execute if data storage mgs:zombies game.map.start_commands[0] run function mgs:v5.4.2/shared/run_start_commands {mode:"zombies"}

function mgs:v5.4.2/zombies/tp_all_to_spawns

effect give @a[scores={mgs.zb.in_game=1}] darkness 25 255 true
effect give @a[scores={mgs.zb.in_game=1}] blindness 25 255 true
effect give @a[scores={mgs.zb.in_game=1}] night_vision 25 255 true
execute as @a[scores={mgs.zb.in_game=1}] run attribute @s minecraft:movement_speed base set 0
execute as @a[scores={mgs.zb.in_game=1}] run attribute @s minecraft:jump_strength base set 0

execute as @a[scores={mgs.zb.in_game=1}] run attribute @s minecraft:max_health base reset
execute as @a[scores={mgs.zb.in_game=1}] run attribute @s minecraft:entity_interaction_range base set 5

execute as @a[scores={mgs.zb.in_game=1}] at @s run function mgs:v5.4.2/zombies/inventory/give_starting_loadout

# Zonweeb only.
execute if data storage mgs:zombies game{variant:"zonweeb"} as @a[scores={mgs.zb.in_game=1}] run function mgs:v5.4.2/zombies/passive_ability_menu

# Prep lasts 10 s.
schedule function mgs:v5.4.2/zombies/end_prep 200t

function mgs:v5.4.2/zombies/create_sidebar

# Perk wording only for Zonweeb.
execute if data storage mgs:zombies game{variant:"zonweeb"} run tellraw @a[scores={mgs.zb.in_game=1}] ["",{"text":"","color":"dark_green","bold":true},"🧟 ",{"translate":"mgs.preparing_choose_your_perk_round_1_starts_in_10_seconds","fallback":"Preparing! Choose your perk! Round 1 starts in 10 seconds!","color":"yellow"}]
execute unless data storage mgs:zombies game{variant:"zonweeb"} run tellraw @a[scores={mgs.zb.in_game=1}] ["",{"text":"","color":"dark_green","bold":true},"🧟 ",{"translate":"mgs.preparing_round_1_starts_in_10_seconds","fallback":"Preparing! Round 1 starts in 10 seconds!","color":"yellow"}]

function mgs:v5.4.2/zombies/escort/setup_lure_center

execute if data storage mgs:zombies game.map.mystery_box.positions[0] run function mgs:v5.4.2/zombies/mystery_box/setup_positions

execute if data storage mgs:zombies game.map.pap_machines[0] run function mgs:v5.4.2/zombies/pap/setup

execute if data storage mgs:zombies game.map.barricades[0] run function mgs:v5.4.2/zombies/barricades/setup

execute if data storage mgs:zombies game.map.power_switch[0] run function mgs:v5.4.2/zombies/power/setup

execute if data storage mgs:zombies game.map.doors[0] run function mgs:v5.4.2/zombies/doors/setup

execute if data storage mgs:zombies game.map.wallbuys[0] run function mgs:v5.4.2/zombies/wallbuys/setup

execute if data storage mgs:zombies game.map.perks[0] run function mgs:v5.4.2/zombies/perks/setup

execute if data storage mgs:zombies game.map.perks[0] run function mgs:v5.4.2/zombies/perks/update_quick_revive_price

execute if data storage mgs:zombies game.map.wunderfizz[0] run function mgs:v5.4.2/zombies/wunderfizz/setup

execute if data storage mgs:zombies game.map.traps[0] run function mgs:v5.4.2/zombies/traps/setup

