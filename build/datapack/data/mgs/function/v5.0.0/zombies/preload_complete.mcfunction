
#> mgs:v5.0.0/zombies/preload_complete
#
# @within	mgs:v5.0.0/zombies/start 20t [ scheduled ]
#

# Guard: only if still preparing
execute unless data storage mgs:zombies game{state:"preparing"} run return fail

# Switch to adventure mode
gamemode adventure @a[scores={mgs.zb.in_game=1}]

# Summon OOB markers (only if map has out_of_bounds data)
execute if data storage mgs:zombies game.map.out_of_bounds run function mgs:v5.0.0/zombies/summon_oob

# Summon spawn point markers for players
function mgs:v5.0.0/zombies/summon_spawns

# Signal zombies game start
function #mgs:zombies/on_game_start

# Teleport all players to player spawns
function mgs:v5.0.0/zombies/tp_all_to_spawns

# Freeze players during prep
effect give @a[scores={mgs.zb.in_game=1}] darkness 25 255 true
effect give @a[scores={mgs.zb.in_game=1}] blindness 25 255 true
effect give @a[scores={mgs.zb.in_game=1}] night_vision 25 255 true
effect give @a[scores={mgs.zb.in_game=1}] saturation infinite 255 true
execute as @a[scores={mgs.zb.in_game=1}] run attribute @s minecraft:max_health base reset
execute as @a[scores={mgs.zb.in_game=1}] run attribute @s minecraft:movement_speed base set 0
execute as @a[scores={mgs.zb.in_game=1}] run attribute @s minecraft:jump_strength base set 0

# Give starting loadout to all players
execute as @a[scores={mgs.zb.in_game=1}] at @s run function mgs:v5.0.0/zombies/inventory/give_starting_loadout

# Show zombies perk selection menu
execute as @a[scores={mgs.zb.in_game=1}] run function mgs:v5.0.0/zombies/passive_ability_menu

# Schedule end of prep (9 seconds remaining)
schedule function mgs:v5.0.0/zombies/end_prep 180t

# Initialize sidebar
function mgs:v5.0.0/zombies/create_sidebar

# Announce
tellraw @a ["",{"text":"","color":"dark_green","bold":true},"🧟 ",{"translate":"mgs.preparing_choose_your_perk_round_1_starts_in_9_seconds","color":"yellow"}]

# Setup mystery box positions
execute if data storage mgs:zombies game.map.mystery_box.positions[0] run function mgs:v5.0.0/zombies/mystery_box/setup_positions

# Setup power switches
execute if data storage mgs:zombies game.map.power_switch[0] run function mgs:v5.0.0/zombies/power/setup

# Setup doors
execute if data storage mgs:zombies game.map.doors[0] run function mgs:v5.0.0/zombies/doors/setup

# Setup wallbuys
execute if data storage mgs:zombies game.map.wallbuys[0] run function mgs:v5.0.0/zombies/wallbuys/setup

# Setup perk machines
execute if data storage mgs:zombies game.map.perks[0] run function mgs:v5.0.0/zombies/perks/setup

# Setup traps
execute if data storage mgs:zombies game.map.traps[0] run function mgs:v5.0.0/zombies/traps/setup

