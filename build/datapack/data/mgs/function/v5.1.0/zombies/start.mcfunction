
#> mgs:v5.1.0/zombies/start
#
# @executed	as the player & at current position
#
# @within	mgs:v5.1.0/zombies/restart
#			dialog mgs:v5.1.0/zombies/setup
#

execute if data storage mgs:zombies game{state:"active"} run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.zombies_game_already_in_progress","color":"red"}]
execute if data storage mgs:zombies game{state:"preparing"} run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.zombies_game_already_preparing","color":"red"}]

# Players join through Manage Players or + Join.
execute unless entity @a[scores={mgs.zb.in_game=1}] run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.no_players_have_joined_the_zombies_game_use_manage_players_first","color":"red"}]

execute if data storage mgs:zombies game{map_id:""} run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.no_map_selected_use_the_setup_menu_to_select_a_map","color":"red"}]

function mgs:v5.1.0/zombies/load_map_from_storage with storage mgs:zombies game
execute unless score #map_load_found mgs.data matches 1 run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.map_not_found_select_a_valid_map","color":"red"}]

data modify storage mgs:zombies game.map set from storage mgs:temp map_load.result

# Set state to preparing
data modify storage mgs:zombies game.state set value "preparing"

# in_game is the opt-in flag, so it stays. The XP spend tracker is reset too, or the reset reads as points spent (see xp).
scoreboard players set @a mgs.zb.points 500
scoreboard players set @a mgs.zb.xp_pts_prev 500
scoreboard players set @a mgs.zb.xp_spent_acc 0
scoreboard players set @a mgs.zb.kills 0
scoreboard players set @a mgs.zb.downs 0
scoreboard players set @a mgs.zb.passive 0
scoreboard players set @a mgs.zb.ability 0
scoreboard players set @a mgs.zb.ability_cd 0
scoreboard players set @a mgs.zb.horde_cd 0

scoreboard players set #zb_points_kill mgs.config 50
scoreboard players set #zb_points_hit mgs.config 10
scoreboard players set #zb_points_knife_kill mgs.config 130
scoreboard players set #zb_mystery_box_price mgs.config 950

team join mgs.zombies @a[scores={mgs.zb.in_game=1}]

# Kills from before the game do not count.
execute as @a run scoreboard players operation @s mgs.zb.prev_kills = @s mgs.total_kills

# Prevents false triggers.
scoreboard players set @a mgs.mp.death_count 0
scoreboard players set @a mgs.mp.spectate_timer 0

# A stale flag would pause the first round.
scoreboard players set #zb_freeze mgs.data 0
tag @e[tag=mgs.zb_frozen_ai] remove mgs.zb_frozen_ai

scoreboard players set @a mgs.mp.in_game 0
scoreboard players set @a mgs.mi.in_game 0

gamerule natural_health_regeneration false
scoreboard players set #any_game_active mgs.data 1

# hp_prev comes from the `health` criterion; a player whose score is unset syncs on their first health change.
scoreboard players set @a mgs.last_hit 0
scoreboard players set @a mgs.hp_prev 0
execute as @a run scoreboard players operation @s mgs.hp_prev = @s mgs.health

# Everyone, late joiners included, re-inits at full stamina on their next tick.
scoreboard players set @a mgs.stam_seen 0

# Post effects live in player NBT, so a round that ended badly could still apply them.
execute as @a run function mgs:v5.1.0/player/fx_reset

gamemode spectator @a[scores={mgs.zb.in_game=1}]
gamerule immediate_respawn true
gamerule keep_inventory true
gamerule max_entity_cramming 96
gamerule advance_time false
time set 18000

# The first round is 1.
data modify storage mgs:zombies game.round set value 0

function mgs:v5.1.0/shared/load_base_coordinates {mode:"zombies"}

# At least 2 corners: a lone corner would collapse to a point that eliminates everyone.
scoreboard players set #zb_has_bounds mgs.data 0
execute if data storage mgs:zombies game.map.boundaries[0] if data storage mgs:zombies game.map.boundaries[1] run scoreboard players set #zb_has_bounds mgs.data 1

execute if score #zb_has_bounds mgs.data matches 1 run function mgs:v5.1.0/shared/load_bounds {mode:"zombies"}

execute if score #zb_has_bounds mgs.data matches 1 run function mgs:v5.1.0/shared/forceload_area

# Spectators at the base coordinates while chunks preload.
execute store result storage mgs:temp _tp.x int 1 run scoreboard players get #gm_base_x mgs.data
execute store result storage mgs:temp _tp.y int 1 run scoreboard players get #gm_base_y mgs.data
execute store result storage mgs:temp _tp.z int 1 run scoreboard players get #gm_base_z mgs.data
execute as @a[scores={mgs.zb.in_game=1}] run function mgs:v5.1.0/shared/tp_to_position with storage mgs:temp _tp

# Extension points.
function #mgs:zombies/register_maps
function #mgs:zombies/register_mystery_box_item

schedule function mgs:v5.1.0/zombies/preload_complete 20t

tellraw @a ["",{"text":"","color":"dark_green","bold":true},"🧟 ",{"translate":"mgs.loading_zombies_map","color":"yellow"}]

scoreboard players set #zb_escort_count mgs.data 0
scoreboard players set #zb_escort_mode mgs.data 0
scoreboard players set #zb_lure mgs.data 0
gamerule spawn_wandering_traders false
gamerule spawn_mobs false

scoreboard players set #zb_power mgs.data 0

# Group 0 is the starting area; compound keys for quick lookup.
data modify storage mgs:zombies game.unlocked_groups set value {"0": 1b}

# Every known score holder, offline players included.
scoreboard players reset * mgs.zb.perk.juggernog
scoreboard players reset * mgs.zb.perk.speed_cola
scoreboard players reset * mgs.zb.perk.double_tap
scoreboard players reset * mgs.zb.perk.quick_revive
scoreboard players reset * mgs.zb.perk.mule_kick
scoreboard players reset * mgs.zb.perk.stamin_up
scoreboard players reset * mgs.zb.perk.phd_flopper
scoreboard players reset * mgs.zb.perk.deadshot
scoreboard players reset * mgs.zb.perk.timeslip
scoreboard players reset * mgs.zb.perk.electric_cherry
scoreboard players reset * mgs.zb.perk.tombstone
scoreboard players reset * mgs.zb.perk.whos_who
scoreboard players reset * mgs.zb.perk.dying_wish
scoreboard players reset * mgs.zb.perk.widows_wine

# Chip-in progress never carries between games.
scoreboard players reset * mgs.zb.perkpaid.juggernog
scoreboard players reset * mgs.zb.perkpaid.speed_cola
scoreboard players reset * mgs.zb.perkpaid.double_tap
scoreboard players reset * mgs.zb.perkpaid.quick_revive
scoreboard players reset * mgs.zb.perkpaid.mule_kick
scoreboard players reset * mgs.zb.perkpaid.stamin_up
scoreboard players reset * mgs.zb.perkpaid.phd_flopper
scoreboard players reset * mgs.zb.perkpaid.deadshot
scoreboard players reset * mgs.zb.perkpaid.timeslip
scoreboard players reset * mgs.zb.perkpaid.electric_cherry
scoreboard players reset * mgs.zb.perkpaid.tombstone
scoreboard players reset * mgs.zb.perkpaid.whos_who
scoreboard players reset * mgs.zb.perkpaid.dying_wish
scoreboard players reset * mgs.zb.perkpaid.widows_wine

# Repopulated by perks/setup.
scoreboard players set #map_perk_juggernog mgs.data 0
scoreboard players set #map_perk_speed_cola mgs.data 0
scoreboard players set #map_perk_double_tap mgs.data 0
scoreboard players set #map_perk_quick_revive mgs.data 0
scoreboard players set #map_perk_mule_kick mgs.data 0
scoreboard players set #map_perk_stamin_up mgs.data 0
scoreboard players set #map_perk_phd_flopper mgs.data 0
scoreboard players set #map_perk_deadshot mgs.data 0
scoreboard players set #map_perk_timeslip mgs.data 0
scoreboard players set #map_perk_electric_cherry mgs.data 0
scoreboard players set #map_perk_tombstone mgs.data 0
scoreboard players set #map_perk_whos_who mgs.data 0
scoreboard players set #map_perk_dying_wish mgs.data 0
scoreboard players set #map_perk_widows_wine mgs.data 0

# Perk effects survive a game that ended without a proper stop, and special.* can come from a class or the debug menu.
execute as @a[scores={mgs.zb.in_game=1}] run attribute @s minecraft:max_health base reset
execute as @a[scores={mgs.zb.in_game=1}] run attribute @s minecraft:movement_speed modifier remove mgs:stamin_up
execute as @a[scores={mgs.zb.in_game=1}] run attribute @s minecraft:fall_damage_multiplier base reset
execute as @a[scores={mgs.zb.in_game=1}] run attribute @s minecraft:attack_damage modifier remove mgs:widows_wine
execute as @a[scores={mgs.zb.in_game=1}] run attribute @s minecraft:attack_damage modifier remove mgs:dying_wish
tag @a[scores={mgs.zb.in_game=1}] remove mgs.dying_wish_active
scoreboard players set @a[scores={mgs.zb.in_game=1}] mgs.zb.dw_uses 0
scoreboard players set @a[scores={mgs.zb.in_game=1}] mgs.zb.dw_cd 0
scoreboard players set @a[scores={mgs.zb.in_game=1}] mgs.zb.dw_timer 0
scoreboard players set @a[scores={mgs.zb.in_game=1}] mgs.stam_bonus 0
tag @a[scores={mgs.zb.in_game=1}] remove mgs.perk.speed_cola
tag @a[scores={mgs.zb.in_game=1}] remove mgs.perk.double_tap
tag @a[scores={mgs.zb.in_game=1}] remove mgs.perk.quick_revive
scoreboard players set @a[scores={mgs.zb.in_game=1}] mgs.special.instant_kill 0
scoreboard players set @a[scores={mgs.zb.in_game=1}] mgs.special.infinite_ammo 0
scoreboard players set @a[scores={mgs.zb.in_game=1}] mgs.special.double_points 0
scoreboard players set @a[scores={mgs.zb.in_game=1}] mgs.special.quick_reload 0
scoreboard players set @a[scores={mgs.zb.in_game=1}] mgs.special.quick_swap 0
scoreboard players set @a[scores={mgs.zb.in_game=1}] mgs.special.double_tap 0
scoreboard players set @a[scores={mgs.zb.in_game=1}] mgs.special.phd_flopper 0
scoreboard players set @a[scores={mgs.zb.in_game=1}] mgs.special.deadshot 0
scoreboard players set @a[scores={mgs.zb.in_game=1}] mgs.special.timeslip 0
scoreboard players set @a[scores={mgs.zb.in_game=1}] mgs.special.electric_cherry 0
scoreboard players set @a[scores={mgs.zb.in_game=1}] mgs.special.widows_wine 0
scoreboard players set @a[scores={mgs.zb.in_game=1}] mgs.special.juggernaut 0
scoreboard players set @a[scores={mgs.zb.in_game=1}] mgs.special.scavenger 0
scoreboard players set @a[scores={mgs.zb.in_game=1}] mgs.special.flak_jacket 0
scoreboard players set @a[scores={mgs.zb.in_game=1}] mgs.special.tracker 0
scoreboard players set @a[scores={mgs.zb.in_game=1}] mgs.special.tactical_mask 0
scoreboard players set @a[scores={mgs.zb.in_game=1}] mgs.special.overkill 0
scoreboard players set @a[scores={mgs.zb.in_game=1}] mgs.special.quick_fix 0

kill @e[type=item_display,tag=mgs.wunderfizz_orb]
kill @e[tag=mgs.wf_display]
kill @e[tag=mgs.wf_bear]
scoreboard players set #wf_uses mgs.data 0
scoreboard players set #wf_move_timer mgs.data 0

tag @a remove mgs.ww_active
scoreboard players set @a mgs.zb.ww.id 0
data modify storage mgs:zombies ww_inv set value {}

scoreboard players set @a mgs.zb.downed 0
scoreboard players set @a mgs.zb.bleed 0
scoreboard players set @a mgs.zb.revive_p 0
scoreboard players set @a mgs.zb.qr_uses 0
scoreboard players set @a mgs.zb.downed_id 0
scoreboard players set #downed_id_next mgs.data 0
tag @a remove mgs.downed_spectator
tag @a remove mgs.zb_qr_armed
kill @e[tag=mgs.downed_mannequin]
kill @e[tag=mgs.downed_hud]
kill @e[tag=mgs.downed_cam]
kill @e[tag=mgs.tombstone]
data modify storage mgs:zombies tombstone_inv set value {}

