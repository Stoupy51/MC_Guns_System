
#> mgs:v5.1.0/zombies/start
#
# @within	???
#

# Prevent starting if already active or preparing
execute if data storage mgs:zombies game{state:"active"} run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.zombies_game_already_in_progress","color":"red"}]
execute if data storage mgs:zombies game{state:"preparing"} run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.zombies_game_already_preparing","color":"red"}]

# Require at least one opted-in player (players are independent until added via Manage Players / + Join)
execute unless entity @a[scores={mgs.zb.in_game=1}] run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.no_players_have_joined_the_zombies_game_use_manage_players_first","color":"red"}]

# Check that a map is selected
execute if data storage mgs:zombies game{map_id:""} run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.no_map_selected_use_the_setup_menu_to_select_a_map","color":"red"}]

# Load the selected map
function mgs:v5.1.0/zombies/load_map_from_storage with storage mgs:zombies game
execute unless score #map_load_found mgs.data matches 1 run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.map_not_found_select_a_valid_map","color":"red"}]

# Copy loaded map data into game state
data modify storage mgs:zombies game.map set from storage mgs:temp map_load.result

# Set state to preparing
data modify storage mgs:zombies game.state set value "preparing"

# Create zombies team
team add mgs.zombies
team modify mgs.zombies color yellow
team modify mgs.zombies friendlyFire false
team modify mgs.zombies nametagVisibility hideForOtherTeams

# Reset scores (in_game is left untouched: it's the opt-in flag, set via Manage Players / + Join)
scoreboard players set @a mgs.zb.points 500
scoreboard players set @a mgs.zb.kills 0
scoreboard players set @a mgs.zb.downs 0
scoreboard players set @a mgs.zb.passive 0
scoreboard players set @a mgs.zb.ability 0
scoreboard players set @a mgs.zb.ability_cd 0

# Config: points per kill, points per hit
scoreboard players set #zb_points_kill mgs.config 50
scoreboard players set #zb_points_hit mgs.config 5
scoreboard players set #zb_points_knife_kill mgs.config 130
scoreboard players set #zb_mystery_box_price mgs.config 950

# Assign opted-in players to the zombies team
team join mgs.zombies @a[scores={mgs.zb.in_game=1}]

# Initialize kill tracking baseline (so kills before game start don't count)
execute as @a run scoreboard players operation @s mgs.zb.prev_kills = @s mgs.total_kills

# Reset death counters and spectate timers to prevent false triggers
scoreboard players set @a mgs.mp.death_count 0
scoreboard players set @a mgs.mp.spectate_timer 0

# Clear other modes' in-game flags so their ticks/logic don't conflict with zombies
scoreboard players set @a mgs.mp.in_game 0
scoreboard players set @a mgs.mi.in_game 0

# Disable natural regeneration, enable custom regen system
# Disable natural regeneration, enable custom regen system
gamerule natural_health_regeneration false
scoreboard players set #any_game_active mgs.data 1

# Reset per-player regen state (hp_prev seeded from the auto-updated health criterion; a player
# whose criterion score is still unset just misses this seed and syncs on their first health change)
scoreboard players set @a mgs.last_hit 0
scoreboard players set @a mgs.hp_prev 0
execute as @a run scoreboard players operation @s mgs.hp_prev = @s mgs.health

# Reset stamina state so every player re-inits to full on their next stamina tick (also covers late-joiners)
scoreboard players set @a mgs.stam_seen 0

# Set gamerules
gamemode spectator @a[scores={mgs.zb.in_game=1}]
gamerule immediate_respawn true
gamerule keep_inventory true
gamerule max_entity_cramming 96
gamerule advance_time false
time set 18000

# Initialize round to 0 (first round will be 1)
data modify storage mgs:zombies game.round set value 0

# Store base coordinates for offset
function mgs:v5.1.0/shared/load_base_coordinates {mode:"zombies"}

# Check if map has boundaries defined
scoreboard players set #zb_has_bounds mgs.data 0
execute if data storage mgs:zombies game.map.boundaries[0] run scoreboard players set #zb_has_bounds mgs.data 1

# Normalize and store boundaries (only if defined)
execute if score #zb_has_bounds mgs.data matches 1 run function mgs:v5.1.0/shared/load_bounds {mode:"zombies"}

# Forceload the area (only if bounds defined)
execute if score #zb_has_bounds mgs.data matches 1 run function mgs:v5.1.0/shared/forceload_area

# Teleport all players as spectator to base coordinates for chunk preloading
execute store result storage mgs:temp _tp.x int 1 run scoreboard players get #gm_base_x mgs.data
execute store result storage mgs:temp _tp.y int 1 run scoreboard players get #gm_base_y mgs.data
execute store result storage mgs:temp _tp.z int 1 run scoreboard players get #gm_base_z mgs.data
execute as @a[scores={mgs.zb.in_game=1}] run function mgs:v5.1.0/shared/tp_to_position with storage mgs:temp _tp

# Register custom maps and mystery box items (extension points)
function #mgs:zombies/register_maps
function #mgs:zombies/register_mystery_box_item

# Schedule preload completion after 1 second
schedule function mgs:v5.1.0/zombies/preload_complete 20t

# Announce
tellraw @a ["",{"text":"","color":"dark_green","bold":true},"🧟 ",{"translate":"mgs.loading_zombies_map","color":"yellow"}]

# Escort system (escort.py)
scoreboard players set #zb_escort_count mgs.data 0
scoreboard players set #zb_escort_mode mgs.data 0
scoreboard players set #zb_lure mgs.data 0
gamerule spawn_wandering_traders false
gamerule spawn_mobs false

# Initialize power state
scoreboard players set #zb_power mgs.data 0

# Initialize unlocked groups (group 0 = starting area, compound keys for quick lookup)
data modify storage mgs:zombies game.unlocked_groups set value {"0": 1b}

# Reset perk scoreboards for all known score holders (including offline players).
scoreboard players reset * mgs.zb.perk.juggernog
scoreboard players reset * mgs.zb.perk.speed_cola
scoreboard players reset * mgs.zb.perk.double_tap
scoreboard players reset * mgs.zb.perk.quick_revive
scoreboard players reset * mgs.zb.perk.mule_kick
scoreboard players reset * mgs.zb.perk.stamin_up

# Chip-in progress never carries between games
scoreboard players reset * mgs.zb.perkpaid.juggernog
scoreboard players reset * mgs.zb.perkpaid.speed_cola
scoreboard players reset * mgs.zb.perkpaid.double_tap
scoreboard players reset * mgs.zb.perkpaid.quick_revive
scoreboard players reset * mgs.zb.perkpaid.mule_kick
scoreboard players reset * mgs.zb.perkpaid.stamin_up

# Clean slate for the joining players: perk effects survive a game that ended without a proper stop,
# and the special.* scores can just as well have come from a multiplayer class or the debug menu.
execute as @a[scores={mgs.zb.in_game=1}] run attribute @s minecraft:max_health base reset
execute as @a[scores={mgs.zb.in_game=1}] run attribute @s minecraft:movement_speed modifier remove mgs:stamin_up
scoreboard players set @a[scores={mgs.zb.in_game=1}] mgs.stam_bonus 0
tag @a[scores={mgs.zb.in_game=1}] remove mgs.perk.speed_cola
tag @a[scores={mgs.zb.in_game=1}] remove mgs.perk.double_tap
tag @a[scores={mgs.zb.in_game=1}] remove mgs.perk.quick_revive
scoreboard players set @a[scores={mgs.zb.in_game=1}] mgs.special.instant_kill 0
scoreboard players set @a[scores={mgs.zb.in_game=1}] mgs.special.infinite_ammo 0
scoreboard players set @a[scores={mgs.zb.in_game=1}] mgs.special.double_points 0
scoreboard players set @a[scores={mgs.zb.in_game=1}] mgs.special.quick_reload 0
scoreboard players set @a[scores={mgs.zb.in_game=1}] mgs.special.quick_swap 0
scoreboard players set @a[scores={mgs.zb.in_game=1}] mgs.special.additional_shots 0
scoreboard players set @a[scores={mgs.zb.in_game=1}] mgs.special.juggernaut 0
scoreboard players set @a[scores={mgs.zb.in_game=1}] mgs.special.scavenger 0
scoreboard players set @a[scores={mgs.zb.in_game=1}] mgs.special.flak_jacket 0
scoreboard players set @a[scores={mgs.zb.in_game=1}] mgs.special.tracker 0
scoreboard players set @a[scores={mgs.zb.in_game=1}] mgs.special.tactical_mask 0
scoreboard players set @a[scores={mgs.zb.in_game=1}] mgs.special.overkill 0
scoreboard players set @a[scores={mgs.zb.in_game=1}] mgs.special.quick_fix 0

# Reset revive state
scoreboard players set @a mgs.zb.downed 0
scoreboard players set @a mgs.zb.bleed 0
scoreboard players set @a mgs.zb.revive_p 0
scoreboard players set @a mgs.zb.qr_uses 0
scoreboard players set @a mgs.zb.downed_id 0
scoreboard players set #downed_id_next mgs.data 0
tag @a remove mgs.downed_spectator
kill @e[tag=mgs.downed_mannequin]
kill @e[tag=mgs.downed_hud]
kill @e[tag=mgs.downed_cam]

