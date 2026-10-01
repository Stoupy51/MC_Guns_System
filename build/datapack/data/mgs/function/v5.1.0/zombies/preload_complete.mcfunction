
#> mgs:v5.1.0/zombies/preload_complete
#
# @within	mgs:v5.1.0/zombies/start 20t [ scheduled ]
#

execute unless data storage mgs:zombies game{state:"preparing"} run return fail

gamemode adventure @a[scores={mgs.zb.in_game=1}]

execute if data storage mgs:zombies game.map.out_of_bounds run function mgs:v5.1.0/shared/summon_oob {mode:"zombies"}

function mgs:v5.1.0/zombies/summon_spawns

function #mgs:zombies/on_game_start

# After the entity and setup summons.
execute if data storage mgs:zombies game.map.start_commands[0] run function mgs:v5.1.0/shared/run_start_commands {mode:"zombies"}

function mgs:v5.1.0/zombies/tp_all_to_spawns

effect give @a[scores={mgs.zb.in_game=1}] darkness 25 255 true
effect give @a[scores={mgs.zb.in_game=1}] blindness 25 255 true
effect give @a[scores={mgs.zb.in_game=1}] night_vision 25 255 true
execute as @a[scores={mgs.zb.in_game=1}] run attribute @s minecraft:movement_speed base set 0
execute as @a[scores={mgs.zb.in_game=1}] run attribute @s minecraft:jump_strength base set 0
execute as @a[scores={mgs.zb.in_game=1}] run attribute @s minecraft:max_health base reset
execute as @a[scores={mgs.zb.in_game=1}] run attribute @s minecraft:entity_interaction_range base set 5

execute as @a[scores={mgs.zb.in_game=1}] at @s run function mgs:v5.1.0/zombies/inventory/give_starting_loadout

# Zonweeb only.
execute if data storage mgs:zombies game{variant:"zonweeb"} as @a[scores={mgs.zb.in_game=1}] run function mgs:v5.1.0/zombies/passive_ability_menu

# Prep lasts 10 s.
schedule function mgs:v5.1.0/zombies/end_prep 200t

function mgs:v5.1.0/zombies/create_sidebar

# Perk wording only for Zonweeb.
execute if data storage mgs:zombies game{variant:"zonweeb"} run tellraw @a ["",{"text":"","color":"dark_green","bold":true},"🧟 ",{"translate":"mgs.preparing_choose_your_perk_round_1_starts_in_10_seconds","color":"yellow"}]
execute unless data storage mgs:zombies game{variant:"zonweeb"} run tellraw @a ["",{"text":"","color":"dark_green","bold":true},"🧟 ",{"translate":"mgs.preparing_round_1_starts_in_10_seconds","color":"yellow"}]

function mgs:v5.1.0/zombies/escort/setup_lure_center

execute if data storage mgs:zombies game.map.mystery_box.positions[0] run function mgs:v5.1.0/zombies/mystery_box/setup_positions

execute if data storage mgs:zombies game.map.pap_machines[0] run function mgs:v5.1.0/zombies/pap/setup

# Maps saved before the barriers to barricades rename keep the old key, and maps are only appended when missing.
# game.map is a per-game copy, so renaming the key here never touches the stored map.
execute unless data storage mgs:zombies game.map.barricades if data storage mgs:zombies game.map.barriers run data modify storage mgs:zombies game.map.barricades set from storage mgs:zombies game.map.barriers

execute if data storage mgs:zombies game.map.barricades[0] run function mgs:v5.1.0/zombies/barricades/setup

execute if data storage mgs:zombies game.map.power_switch[0] run function mgs:v5.1.0/zombies/power/setup

execute if data storage mgs:zombies game.map.doors[0] run function mgs:v5.1.0/zombies/doors/setup

execute if data storage mgs:zombies game.map.wallbuys[0] run function mgs:v5.1.0/zombies/wallbuys/setup

execute if data storage mgs:zombies game.map.perks[0] run function mgs:v5.1.0/zombies/perks/setup

execute if data storage mgs:zombies game.map.perks[0] run function mgs:v5.1.0/zombies/perks/update_quick_revive_price

execute if data storage mgs:zombies game.map.wunderfizz[0] run function mgs:v5.1.0/zombies/wunderfizz/setup

execute if data storage mgs:zombies game.map.traps[0] run function mgs:v5.1.0/zombies/traps/setup

