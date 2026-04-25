
#> mgs:v5.0.0/load/confirm_load
#
# @within	mgs:v5.0.0/load/valid_dependencies
#

# Player config: trigger objective for /trigger command
scoreboard objectives add mgs.player.config trigger

# Per-player toggles (default 0 = disabled)
scoreboard objectives add mgs.player.hitmarker dummy
scoreboard objectives add mgs.player.damage_debug dummy

## Define objectives
# Used to tag players that should be selected by Multiplayer/Mission/Zombies functions (@a)
# We use a scoreboard instead of tag so we can reset offline players
scoreboard objectives add mgs.player dummy

# Tracks the currently selected weapon ID for each player
scoreboard objectives add mgs.previous_selected dummy

# Tracks right clicks to enable continuous right-click detection
scoreboard objectives add mgs.pending_clicks dummy

# Tracks if the player is holding right-click (vs single tap)
scoreboard objectives add mgs.held_click dummy

# Tracks current burst fire count (resets after BURST shots)
scoreboard objectives add mgs.burst_count dummy

# Tracks weapon drops to enable fire mode switching
scoreboard objectives add mgs.dropped minecraft.custom:minecraft.drop

# Cooldown in ticks before being able to shot
scoreboard objectives add mgs.cooldown dummy

# Tracks weapon-switch-only cooldown (not set when shooting) for zoom shader guard
scoreboard objectives add mgs.switch_cooldown dummy

# Indicates if the player was zooming (used to remove slowness)
scoreboard objectives add mgs.zoom dummy

# Tracks continuous zoom duration for delayed scope effect (10-tick delay)
scoreboard objectives add mgs.zoom_timer dummy

# Tracks the most recently selected weapon ID for weapon switching mechanics
scoreboard objectives add mgs.last_selected dummy

# Tracks the current amount of bullets in the selected weapon
scoreboard objectives add mgs.remaining_bullets dummy

# Tracks the total reserve ammo (sum of all magazine bullets in inventory)
# Updated on reload and when player is idle (not shooting for ~60 ticks)
scoreboard objectives add mgs.reserve_ammo dummy

# Tracks the room acoustics level for crack sound effects
scoreboard objectives add mgs.acoustics_level dummy

# Tracks how much time has passed since the player last saw a muzzle flash
scoreboard objectives add mgs.last_muzzle_flash dummy

## Global configuration scoreboards (admin/server-level)
# RPG explosion power (0 = no block destruction, higher = more destruction)
scoreboard objectives add mgs.config dummy

## Per-player special scoreboards (for zombies bonuses, testing, etc.)
# Instant kill: duration in ticks (kills entities in one hit, except mgs.no_instant_kill tagged)
scoreboard objectives add mgs.special.instant_kill dummy
# Infinite ammo: duration in ticks (don't consume ammo, set ammo to max capacity)
scoreboard objectives add mgs.special.infinite_ammo dummy
# Quick reload: percentage faster reload (20 = 20% faster, 50 = 50% faster)
scoreboard objectives add mgs.special.quick_reload dummy
# Quick swap: percentage faster weapon switch (20 = 20% faster, 50 = 50% faster)
scoreboard objectives add mgs.special.quick_swap dummy
# Additional shots: number of extra projectiles per shot (Double Tap perk)
scoreboard objectives add mgs.special.additional_shots dummy
# DPS tracking: accumulates damage dealt per second, snapshot stored for actionbar
scoreboard objectives add mgs.dps dummy
scoreboard objectives add mgs.previous_dps dummy
scoreboard objectives add mgs.dps_timer dummy

# Initialize slow bullet (projectile) counter
scoreboard players add #slow_bullet_count mgs.data 0

# Semtex entity pairing: unique ID objective + global counter
scoreboard objectives add mgs.grenade_launch dummy
scoreboard objectives add mgs.stuck_id dummy
scoreboard players set #semtex_id mgs.data 0

# Initialize global config defaults (only if not already set)
execute unless score #projectile_explosion_power mgs.config matches -2147483648.. run scoreboard players set #projectile_explosion_power mgs.config 0
execute unless score #grenade_explosion_power mgs.config matches -2147483648.. run scoreboard players set #grenade_explosion_power mgs.config 0
execute unless score #max_ammo_reload_weapons mgs.config matches -2147483648.. run scoreboard players set #max_ammo_reload_weapons mgs.config 0
execute unless score #damage_debug mgs.config matches -2147483648.. run scoreboard players set #damage_debug mgs.config 0

# Confirm load
tellraw @a[tag=convention.debug] {"translate":"mgs.loaded_mc_guns_system_v5_0_0","color":"green"}
scoreboard players set #mgs.loaded load.status 1
function mgs:v5.0.0/load/set_items_storage

## Lore label templates for utils/update_all_lore
data modify storage mgs:lore_templates damage set value [{"text": "D", "color": "#c24a17", "italic": false}, {"text": "a", "color": "#c24c18"}, {"text": "m", "color": "#c24f1a"}, {"text": "a", "color": "#c2511b"}, {"text": "g", "color": "#c3541d"}, {"text": "e", "color": "#c3571e"}, {"text": " ", "color": "#c35920"}, {"text": "P", "color": "#c35c21"}, {"text": "e", "color": "#c45e23"}, {"text": "r", "color": "#c46124"}, {"text": " ", "color": "#c46426"}, {"text": "B", "color": "#c46628"}, {"text": "u", "color": "#c56929"}, {"text": "l", "color": "#c56b2b"}, {"text": "l", "color": "#c56e2c"}, {"text": "e", "color": "#c5712e"}, {"text": "t", "color": "#c6732f"}, {"text": " ", "color": "#c67631"}, {"text": " ", "color": "#c67832"}, {"text": "\u27a4", "color": "#c67b34"}, {"text": " ", "color": "#c77e36"}]
data modify storage mgs:lore_templates ammo set value [{"text": "A", "color": "#c24a17", "italic": false}, {"text": "m", "color": "#c24c18"}, {"text": "m", "color": "#c24e19"}, {"text": "o", "color": "#c2511b"}, {"text": " ", "color": "#c2531c"}, {"text": "R", "color": "#c3561e"}, {"text": "e", "color": "#c3581f"}, {"text": "m", "color": "#c35b21"}, {"text": "a", "color": "#c35d22"}, {"text": "i", "color": "#c46024"}, {"text": "n", "color": "#c46225"}, {"text": "i", "color": "#c46527"}, {"text": "n", "color": "#c46728"}, {"text": "g", "color": "#c56a2a"}, {"text": " ", "color": "#c56c2b"}, {"text": " ", "color": "#c56f2d"}, {"text": " ", "color": "#c5712e"}, {"text": " ", "color": "#c67430"}, {"text": " ", "color": "#c67631"}, {"text": " ", "color": "#c67933"}, {"text": "\u27a4", "color": "#c67b34"}, {"text": " ", "color": "#c77e36"}]
data modify storage mgs:lore_templates reload set value [{"text": "R", "color": "#c24a17", "italic": false}, {"text": "e", "color": "#c24c18"}, {"text": "l", "color": "#c24e19"}, {"text": "o", "color": "#c2511b"}, {"text": "a", "color": "#c2531c"}, {"text": "d", "color": "#c3551e"}, {"text": "i", "color": "#c3581f"}, {"text": "n", "color": "#c35a20"}, {"text": "g", "color": "#c35c22"}, {"text": " ", "color": "#c45f23"}, {"text": "T", "color": "#c46125"}, {"text": "i", "color": "#c46426"}, {"text": "m", "color": "#c46627"}, {"text": "e", "color": "#c46829"}, {"text": " ", "color": "#c56b2a"}, {"text": " ", "color": "#c56d2c"}, {"text": " ", "color": "#c56f2d"}, {"text": " ", "color": "#c5722e"}, {"text": " ", "color": "#c67430"}, {"text": " ", "color": "#c67631"}, {"text": " ", "color": "#c67933"}, {"text": "\u27a4", "color": "#c67b34"}, {"text": " ", "color": "#c77e36"}]
data modify storage mgs:lore_templates fire_rate set value [{"text": "F", "color": "#c24a17", "italic": false}, {"text": "i", "color": "#c24c18"}, {"text": "r", "color": "#c24e19"}, {"text": "e", "color": "#c2501b"}, {"text": " ", "color": "#c2531c"}, {"text": "R", "color": "#c3551d"}, {"text": "a", "color": "#c3571f"}, {"text": "t", "color": "#c35920"}, {"text": "e", "color": "#c35c21"}, {"text": " ", "color": "#c35e23"}, {"text": " ", "color": "#c46024"}, {"text": " ", "color": "#c46225"}, {"text": " ", "color": "#c46527"}, {"text": " ", "color": "#c46728"}, {"text": " ", "color": "#c56929"}, {"text": " ", "color": "#c56b2b"}, {"text": " ", "color": "#c56e2c"}, {"text": " ", "color": "#c5702d"}, {"text": " ", "color": "#c5722f"}, {"text": " ", "color": "#c67430"}, {"text": " ", "color": "#c67731"}, {"text": " ", "color": "#c67933"}, {"text": "\u27a4", "color": "#c67b34"}, {"text": " ", "color": "#c77e36"}]
data modify storage mgs:lore_templates pellets set value [{"text": "P", "color": "#c24a17", "italic": false}, {"text": "e", "color": "#c24c18"}, {"text": "l", "color": "#c24e19"}, {"text": "l", "color": "#c2511b"}, {"text": "e", "color": "#c2531c"}, {"text": "t", "color": "#c3561e"}, {"text": "s", "color": "#c3581f"}, {"text": " ", "color": "#c35b21"}, {"text": "P", "color": "#c35d22"}, {"text": "e", "color": "#c46024"}, {"text": "r", "color": "#c46225"}, {"text": " ", "color": "#c46527"}, {"text": "S", "color": "#c46728"}, {"text": "h", "color": "#c56a2a"}, {"text": "o", "color": "#c56c2b"}, {"text": "t", "color": "#c56f2d"}, {"text": " ", "color": "#c5712e"}, {"text": " ", "color": "#c67430"}, {"text": " ", "color": "#c67631"}, {"text": " ", "color": "#c67933"}, {"text": "\u27a4", "color": "#c67b34"}, {"text": " ", "color": "#c77e36"}]
data modify storage mgs:lore_templates decay set value [{"text": "D", "color": "#c24a17", "italic": false}, {"text": "a", "color": "#c24c18"}, {"text": "m", "color": "#c24f1a"}, {"text": "a", "color": "#c2511b"}, {"text": "g", "color": "#c3541d"}, {"text": "e", "color": "#c3571e"}, {"text": " ", "color": "#c35920"}, {"text": "D", "color": "#c35c21"}, {"text": "e", "color": "#c45e23"}, {"text": "c", "color": "#c46124"}, {"text": "a", "color": "#c46426"}, {"text": "y", "color": "#c46628"}, {"text": " ", "color": "#c56929"}, {"text": " ", "color": "#c56b2b"}, {"text": " ", "color": "#c56e2c"}, {"text": " ", "color": "#c5712e"}, {"text": " ", "color": "#c6732f"}, {"text": " ", "color": "#c67631"}, {"text": " ", "color": "#c67832"}, {"text": "\u27a4", "color": "#c67b34"}, {"text": " ", "color": "#c77e36"}]
data modify storage mgs:lore_templates switch_time set value [{"text": "S", "color": "#c24a17", "italic": false}, {"text": "w", "color": "#c24c18"}, {"text": "i", "color": "#c24e19"}, {"text": "t", "color": "#c2501b"}, {"text": "c", "color": "#c2531c"}, {"text": "h", "color": "#c3551d"}, {"text": " ", "color": "#c3571f"}, {"text": "T", "color": "#c35920"}, {"text": "i", "color": "#c35c21"}, {"text": "m", "color": "#c35e23"}, {"text": "e", "color": "#c46024"}, {"text": " ", "color": "#c46225"}, {"text": " ", "color": "#c46527"}, {"text": " ", "color": "#c46728"}, {"text": " ", "color": "#c56929"}, {"text": " ", "color": "#c56b2b"}, {"text": " ", "color": "#c56e2c"}, {"text": " ", "color": "#c5702d"}, {"text": " ", "color": "#c5722f"}, {"text": " ", "color": "#c67430"}, {"text": " ", "color": "#c67731"}, {"text": " ", "color": "#c67933"}, {"text": "\u27a4", "color": "#c67b34"}, {"text": " ", "color": "#c77e36"}]
data modify storage mgs:lore_templates fire_rate_sps set value [{"text": "s", "color": "#c77e36", "italic": false}, {"text": "h", "color": "#c67832"}, {"text": "o", "color": "#c5722f"}, {"text": "t", "color": "#c56c2b"}, {"text": "s", "color": "#c46628"}, {"text": "/", "color": "#c46124"}, {"text": "s", "color": "#c35b21"}]
data modify storage mgs:lore_templates fire_rate_spshot set value [{"text": "s", "color": "#c77e36", "italic": false}, {"text": "/", "color": "#c67832"}, {"text": "s", "color": "#c5722f"}, {"text": "h", "color": "#c56c2b"}, {"text": "o", "color": "#c46628"}, {"text": "t", "color": "#c46124"}]
data modify storage mgs:lore_templates grenade_type set value [{"text": "T", "color": "#c24a17", "italic": false}, {"text": "y", "color": "#c24c18"}, {"text": "p", "color": "#c24e19"}, {"text": "e", "color": "#c2501b"}, {"text": " ", "color": "#c2531c"}, {"text": " ", "color": "#c3551d"}, {"text": " ", "color": "#c3571f"}, {"text": " ", "color": "#c35920"}, {"text": " ", "color": "#c35c21"}, {"text": " ", "color": "#c35e23"}, {"text": " ", "color": "#c46024"}, {"text": " ", "color": "#c46225"}, {"text": " ", "color": "#c46527"}, {"text": " ", "color": "#c46728"}, {"text": " ", "color": "#c56929"}, {"text": " ", "color": "#c56b2b"}, {"text": " ", "color": "#c56e2c"}, {"text": " ", "color": "#c5702d"}, {"text": " ", "color": "#c5722f"}, {"text": " ", "color": "#c67430"}, {"text": " ", "color": "#c67731"}, {"text": " ", "color": "#c67933"}, {"text": "\u27a4", "color": "#c67b34"}, {"text": " ", "color": "#c77e36"}]
data modify storage mgs:lore_templates grenade_fuse set value [{"text": "F", "color": "#c24a17", "italic": false}, {"text": "u", "color": "#c24c18"}, {"text": "s", "color": "#c24e19"}, {"text": "e", "color": "#c2511b"}, {"text": " ", "color": "#c2531c"}, {"text": "T", "color": "#c3551e"}, {"text": "i", "color": "#c3581f"}, {"text": "m", "color": "#c35a20"}, {"text": "e", "color": "#c35c22"}, {"text": " ", "color": "#c45f23"}, {"text": " ", "color": "#c46125"}, {"text": " ", "color": "#c46426"}, {"text": " ", "color": "#c46627"}, {"text": " ", "color": "#c46829"}, {"text": " ", "color": "#c56b2a"}, {"text": " ", "color": "#c56d2c"}, {"text": " ", "color": "#c56f2d"}, {"text": " ", "color": "#c5722e"}, {"text": " ", "color": "#c67430"}, {"text": " ", "color": "#c67631"}, {"text": " ", "color": "#c67933"}, {"text": "\u27a4", "color": "#c67b34"}, {"text": " ", "color": "#c77e36"}]
data modify storage mgs:lore_templates expl_damage set value [{"text": "E", "color": "#c24a17", "italic": false}, {"text": "x", "color": "#c24c18"}, {"text": "p", "color": "#c24f1a"}, {"text": "l", "color": "#c2521b"}, {"text": "o", "color": "#c3541d"}, {"text": "s", "color": "#c3571f"}, {"text": "i", "color": "#c35a20"}, {"text": "o", "color": "#c35d22"}, {"text": "n", "color": "#c45f24"}, {"text": " ", "color": "#c46225"}, {"text": "D", "color": "#c46527"}, {"text": "a", "color": "#c46828"}, {"text": "m", "color": "#c56a2a"}, {"text": "a", "color": "#c56d2c"}, {"text": "g", "color": "#c5702d"}, {"text": "e", "color": "#c5732f"}, {"text": " ", "color": "#c67531"}, {"text": " ", "color": "#c67832"}, {"text": "\u27a4", "color": "#c67b34"}, {"text": " ", "color": "#c77e36"}]
data modify storage mgs:lore_templates expl_radius set value [{"text": "E", "color": "#c24a17", "italic": false}, {"text": "x", "color": "#c24c18"}, {"text": "p", "color": "#c24f1a"}, {"text": "l", "color": "#c2511b"}, {"text": "o", "color": "#c3541d"}, {"text": "s", "color": "#c3571e"}, {"text": "i", "color": "#c35920"}, {"text": "o", "color": "#c35c21"}, {"text": "n", "color": "#c45e23"}, {"text": " ", "color": "#c46124"}, {"text": "R", "color": "#c46426"}, {"text": "a", "color": "#c46628"}, {"text": "d", "color": "#c56929"}, {"text": "i", "color": "#c56b2b"}, {"text": "u", "color": "#c56e2c"}, {"text": "s", "color": "#c5712e"}, {"text": " ", "color": "#c6732f"}, {"text": " ", "color": "#c67631"}, {"text": " ", "color": "#c67832"}, {"text": "\u27a4", "color": "#c67b34"}, {"text": " ", "color": "#c77e36"}]

# Armed mob counter (skip tick loop if 0)
scoreboard players add #armed_mob_count mgs.data 0

# Mob AI phase timer, active time, and sleep time
scoreboard objectives add mgs.mob.timer dummy
scoreboard objectives add mgs.mob.active_time dummy
scoreboard objectives add mgs.mob.sleep_time dummy

## Zombies scoreboards
scoreboard objectives add mgs.zb.in_game dummy
scoreboard objectives add mgs.zb.points dummy
scoreboard objectives add mgs.zb.kills dummy
scoreboard objectives add mgs.zb.downs dummy

# Perk scoreboards
# zb.passive: 0=none, 1=points_x1.2, 2=powerup_x1.5
# zb.ability: 0=none, 1=coward, 2=guardian
# Ability cooldown (0 = ready, 1+ = on cooldown in rounds remaining)
scoreboard objectives add mgs.zb.passive dummy
scoreboard objectives add mgs.zb.ability dummy
scoreboard objectives add mgs.zb.ability_cd dummy

# Spawn point group_id scoreboard
scoreboard objectives add mgs.zb.spawn.gid dummy

# Sidebar rank scoreboard
scoreboard objectives add mgs.zb.sb_rank dummy

# Initialize zombies game state
execute unless data storage mgs:zombies game run data modify storage mgs:zombies game set value {state:"lobby",map_id:"",round:0}

# Initialize mystery box base pool (can be extended via function tag)
execute unless data storage mgs:zombies mystery_box_pool run data modify storage mgs:zombies mystery_box_pool set value []

# Config: points per kill, points per hit
# TODO: ZB points hit not used
execute unless score #zb_points_kill mgs.config matches 1.. run scoreboard players set #zb_points_kill mgs.config 50
execute unless score #zb_points_hit mgs.config matches 1.. run scoreboard players set #zb_points_hit mgs.config 10
execute unless score #zb_mystery_box_price mgs.config matches 1.. run scoreboard players set #zb_mystery_box_price mgs.config 950

# Pack-a-Punch machine scoreboards
scoreboard objectives add mgs.zb.pap.id dummy
scoreboard objectives add mgs.zb.pap.price dummy
scoreboard objectives add mgs.zb.pap.power dummy
scoreboard objectives add mgs.pap_anim dummy

# Per-player PAP tracking (for cleanup when weapon is lost/collected)
scoreboard objectives add mgs.zb.pap_s dummy
scoreboard objectives add mgs.zb.pap_mid dummy

data modify storage mgs:zombies scope_variants."ak47" set value [{id:"ak47",model:"mgs:ak47",zoom:"mgs:ak47_zoom"},{id:"ak47_1",model:"mgs:ak47_1",zoom:"mgs:ak47_1_zoom"},{id:"ak47_2",model:"mgs:ak47_2",zoom:"mgs:ak47_2_zoom"},{id:"ak47_3",model:"mgs:ak47_3",zoom:"mgs:ak47_3_zoom",scope_level:3},{id:"ak47_4",model:"mgs:ak47_4",zoom:"mgs:ak47_4_zoom",scope_level:4}]
data modify storage mgs:zombies scope_variants."m16a4" set value [{id:"m16a4",model:"mgs:m16a4",zoom:"mgs:m16a4_zoom"},{id:"m16a4_1",model:"mgs:m16a4_1",zoom:"mgs:m16a4_1_zoom"},{id:"m16a4_2",model:"mgs:m16a4_2",zoom:"mgs:m16a4_2_zoom"},{id:"m16a4_3",model:"mgs:m16a4_3",zoom:"mgs:m16a4_3_zoom",scope_level:3},{id:"m16a4_4",model:"mgs:m16a4_4",zoom:"mgs:m16a4_4_zoom",scope_level:4}]
data modify storage mgs:zombies scope_variants."famas" set value [{id:"famas",model:"mgs:famas",zoom:"mgs:famas_zoom"},{id:"famas_1",model:"mgs:famas_1",zoom:"mgs:famas_1_zoom"},{id:"famas_2",model:"mgs:famas_2",zoom:"mgs:famas_2_zoom"},{id:"famas_3",model:"mgs:famas_3",zoom:"mgs:famas_3_zoom",scope_level:3},{id:"famas_4",model:"mgs:famas_4",zoom:"mgs:famas_4_zoom",scope_level:4}]
data modify storage mgs:zombies scope_variants."aug" set value [{id:"aug",model:"mgs:aug",zoom:"mgs:aug_zoom"},{id:"aug_1",model:"mgs:aug_1",zoom:"mgs:aug_1_zoom"},{id:"aug_2",model:"mgs:aug_2",zoom:"mgs:aug_2_zoom"},{id:"aug_3",model:"mgs:aug_3",zoom:"mgs:aug_3_zoom",scope_level:3},{id:"aug_4",model:"mgs:aug_4",zoom:"mgs:aug_4_zoom",scope_level:4}]
data modify storage mgs:zombies scope_variants."m4a1" set value [{id:"m4a1",model:"mgs:m4a1",zoom:"mgs:m4a1_zoom"},{id:"m4a1_1",model:"mgs:m4a1_1",zoom:"mgs:m4a1_1_zoom"},{id:"m4a1_2",model:"mgs:m4a1_2",zoom:"mgs:m4a1_2_zoom"},{id:"m4a1_3",model:"mgs:m4a1_3",zoom:"mgs:m4a1_3_zoom",scope_level:3},{id:"m4a1_4",model:"mgs:m4a1_4",zoom:"mgs:m4a1_4_zoom",scope_level:4}]
data modify storage mgs:zombies scope_variants."fnfal" set value [{id:"fnfal",model:"mgs:fnfal",zoom:"mgs:fnfal_zoom"},{id:"fnfal_1",model:"mgs:fnfal_1",zoom:"mgs:fnfal_1_zoom"},{id:"fnfal_2",model:"mgs:fnfal_2",zoom:"mgs:fnfal_2_zoom"},{id:"fnfal_3",model:"mgs:fnfal_3",zoom:"mgs:fnfal_3_zoom",scope_level:3},{id:"fnfal_4",model:"mgs:fnfal_4",zoom:"mgs:fnfal_4_zoom",scope_level:4}]
data modify storage mgs:zombies scope_variants."g3a3" set value [{id:"g3a3",model:"mgs:g3a3",zoom:"mgs:g3a3_zoom"},{id:"g3a3_1",model:"mgs:g3a3_1",zoom:"mgs:g3a3_1_zoom"},{id:"g3a3_2",model:"mgs:g3a3_2",zoom:"mgs:g3a3_2_zoom"},{id:"g3a3_3",model:"mgs:g3a3_3",zoom:"mgs:g3a3_3_zoom",scope_level:3},{id:"g3a3_4",model:"mgs:g3a3_4",zoom:"mgs:g3a3_4_zoom",scope_level:4}]
data modify storage mgs:zombies scope_variants."scar17" set value [{id:"scar17",model:"mgs:scar17",zoom:"mgs:scar17_zoom"},{id:"scar17_1",model:"mgs:scar17_1",zoom:"mgs:scar17_1_zoom"},{id:"scar17_2",model:"mgs:scar17_2",zoom:"mgs:scar17_2_zoom"},{id:"scar17_3",model:"mgs:scar17_3",zoom:"mgs:scar17_3_zoom",scope_level:3},{id:"scar17_4",model:"mgs:scar17_4",zoom:"mgs:scar17_4_zoom",scope_level:4}]
data modify storage mgs:zombies scope_variants."mp5" set value [{id:"mp5",model:"mgs:mp5",zoom:"mgs:mp5_zoom"},{id:"mp5_1",model:"mgs:mp5_1",zoom:"mgs:mp5_1_zoom"},{id:"mp5_2",model:"mgs:mp5_2",zoom:"mgs:mp5_2_zoom"},{id:"mp5_3",model:"mgs:mp5_3",zoom:"mgs:mp5_3_zoom",scope_level:3},{id:"mp5_4",model:"mgs:mp5_4",zoom:"mgs:mp5_4_zoom",scope_level:4}]
data modify storage mgs:zombies scope_variants."mp7" set value [{id:"mp7",model:"mgs:mp7",zoom:"mgs:mp7_zoom"},{id:"mp7_1",model:"mgs:mp7_1",zoom:"mgs:mp7_1_zoom"},{id:"mp7_2",model:"mgs:mp7_2",zoom:"mgs:mp7_2_zoom"},{id:"mp7_3",model:"mgs:mp7_3",zoom:"mgs:mp7_3_zoom",scope_level:3},{id:"mp7_4",model:"mgs:mp7_4",zoom:"mgs:mp7_4_zoom",scope_level:4}]
data modify storage mgs:zombies scope_variants."svd" set value [{id:"svd",model:"mgs:svd",zoom:"mgs:svd_zoom"},{id:"svd_1",model:"mgs:svd_1",zoom:"mgs:svd_1_zoom"},{id:"svd_2",model:"mgs:svd_2",zoom:"mgs:svd_2_zoom"},{id:"svd_3",model:"mgs:svd_3",zoom:"mgs:svd_3_zoom",scope_level:3},{id:"svd_4",model:"mgs:svd_4",zoom:"mgs:svd_4_zoom",scope_level:4}]
data modify storage mgs:zombies scope_variants."m82" set value [{id:"m82",model:"mgs:m82",zoom:"mgs:m82_zoom"},{id:"m82_1",model:"mgs:m82_1",zoom:"mgs:m82_1_zoom"},{id:"m82_2",model:"mgs:m82_2",zoom:"mgs:m82_2_zoom"},{id:"m82_3",model:"mgs:m82_3",zoom:"mgs:m82_3_zoom",scope_level:3},{id:"m82_4",model:"mgs:m82_4",zoom:"mgs:m82_4_zoom",scope_level:4}]
data modify storage mgs:zombies scope_variants."m24" set value [{id:"m24",model:"mgs:m24",zoom:"mgs:m24_zoom"},{id:"m24_1",model:"mgs:m24_1",zoom:"mgs:m24_1_zoom"},{id:"m24_2",model:"mgs:m24_2",zoom:"mgs:m24_2_zoom"},{id:"m24_3",model:"mgs:m24_3",zoom:"mgs:m24_3_zoom",scope_level:3},{id:"m24_4",model:"mgs:m24_4",zoom:"mgs:m24_4_zoom",scope_level:4}]
data modify storage mgs:zombies scope_variants."rpk" set value [{id:"rpk",model:"mgs:rpk",zoom:"mgs:rpk_zoom"},{id:"rpk_1",model:"mgs:rpk_1",zoom:"mgs:rpk_1_zoom"},{id:"rpk_2",model:"mgs:rpk_2",zoom:"mgs:rpk_2_zoom"},{id:"rpk_3",model:"mgs:rpk_3",zoom:"mgs:rpk_3_zoom",scope_level:3},{id:"rpk_4",model:"mgs:rpk_4",zoom:"mgs:rpk_4_zoom",scope_level:4}]
data modify storage mgs:zombies scope_variants."spas12" set value [{id:"spas12",model:"mgs:spas12",zoom:"mgs:spas12_zoom"},{id:"spas12_1",model:"mgs:spas12_1",zoom:"mgs:spas12_1_zoom"},{id:"spas12_2",model:"mgs:spas12_2",zoom:"mgs:spas12_2_zoom"},{id:"spas12_3",model:"mgs:spas12_3",zoom:"mgs:spas12_3_zoom",scope_level:3}]
data modify storage mgs:zombies scope_variants."m500" set value [{id:"m500",model:"mgs:m500",zoom:"mgs:m500_zoom"},{id:"m500_1",model:"mgs:m500_1",zoom:"mgs:m500_1_zoom"},{id:"m500_2",model:"mgs:m500_2",zoom:"mgs:m500_2_zoom"},{id:"m500_3",model:"mgs:m500_3",zoom:"mgs:m500_3_zoom",scope_level:3}]
data modify storage mgs:zombies scope_variants."m590" set value [{id:"m590",model:"mgs:m590",zoom:"mgs:m590_zoom"},{id:"m590_1",model:"mgs:m590_1",zoom:"mgs:m590_1_zoom"},{id:"m590_2",model:"mgs:m590_2",zoom:"mgs:m590_2_zoom"},{id:"m590_3",model:"mgs:m590_3",zoom:"mgs:m590_3_zoom",scope_level:3}]
data modify storage mgs:zombies scope_variants."m249" set value [{id:"m249",model:"mgs:m249",zoom:"mgs:m249_zoom"},{id:"m249_1",model:"mgs:m249_1",zoom:"mgs:m249_1_zoom"},{id:"m249_2",model:"mgs:m249_2",zoom:"mgs:m249_2_zoom"},{id:"m249_3",model:"mgs:m249_3",zoom:"mgs:m249_3_zoom",scope_level:3}]
data modify storage mgs:zombies scope_variants."mosin" set value [{id:"mosin",model:"mgs:mosin",zoom:"mgs:mosin_zoom"},{id:"mosin_1",model:"mgs:mosin_1",zoom:"mgs:mosin_1_zoom"}]
data modify storage mgs:zombies scope_variants."deagle" set value [{id:"deagle",model:"mgs:deagle",zoom:"mgs:deagle_zoom"},{id:"deagle_4",model:"mgs:deagle_4",zoom:"mgs:deagle_4_zoom",scope_level:4}]

# Barrier entity scoreboards
scoreboard objectives add mgs.zb.barrier.id dummy
scoreboard objectives add mgs.zb.barrier.state dummy
scoreboard objectives add mgs.zb.barrier.r_timer dummy
scoreboard objectives add mgs.zb.barrier.rp_timer dummy
scoreboard objectives add mgs.zb.barrier.radius dummy
scoreboard objectives add mgs.zb.barrier.removing_id dummy
scoreboard objectives add mgs.zb.barrier.repairing_id dummy

# Door entity scoreboards
scoreboard objectives add mgs.zb.door.link dummy
scoreboard objectives add mgs.zb.door.price dummy
scoreboard objectives add mgs.zb.door.gid dummy
scoreboard objectives add mgs.zb.door.bgid dummy
scoreboard objectives add mgs.zb.door.anim dummy
scoreboard objectives add mgs.zb.door.rot dummy

# Wallbuy entity scoreboards
scoreboard objectives add mgs.zb.wb.id dummy
scoreboard objectives add mgs.zb.wb.price dummy
scoreboard objectives add mgs.zb.wb.rfprice dummy
scoreboard objectives add mgs.zb.wb.rfpap dummy

# Perk machine entity scoreboards
scoreboard objectives add mgs.zb.perk.id dummy
scoreboard objectives add mgs.zb.perk.price dummy
scoreboard objectives add mgs.zb.perk.power dummy

# Perk ownership scoreboards
scoreboard objectives add mgs.zb.perk.juggernog dummy
scoreboard objectives add mgs.zb.perk.speed_cola dummy
scoreboard objectives add mgs.zb.perk.double_tap dummy
scoreboard objectives add mgs.zb.perk.quick_revive dummy
scoreboard objectives add mgs.zb.perk.mule_kick dummy

# Revive system scoreboards
scoreboard objectives add mgs.zb.downed dummy
scoreboard objectives add mgs.zb.bleed dummy
scoreboard objectives add mgs.zb.revive_p dummy

# Trap entity scoreboards
scoreboard objectives add mgs.zb.trap.id dummy
scoreboard objectives add mgs.zb.trap.price dummy
scoreboard objectives add mgs.zb.trap.power dummy
scoreboard objectives add mgs.zb.trap.type dummy
scoreboard objectives add mgs.zb.trap.dur dummy
scoreboard objectives add mgs.zb.trap.cd_max dummy
scoreboard objectives add mgs.zb.trap.timer dummy
scoreboard objectives add mgs.zb.trap.cd dummy
scoreboard objectives add mgs.zb.trap.rx dummy
scoreboard objectives add mgs.zb.trap.ry dummy
scoreboard objectives add mgs.zb.trap.rz dummy

## Multiplayer scoreboards
# Team assignment (1 = red, 2 = blue, 0 = none/spectator)
scoreboard objectives add mgs.mp.team dummy
# Personal stats
scoreboard objectives add mgs.mp.kills dummy
scoreboard objectives add mgs.mp.deaths dummy
# Round timer (ticks remaining)
scoreboard objectives add mgs.mp.timer dummy
# In-game tag scoreboard (1 = in active game)
scoreboard objectives add mgs.mp.in_game dummy

# Boundary checking coords
scoreboard objectives add mgs.mp.bx dummy
scoreboard objectives add mgs.mp.by dummy
scoreboard objectives add mgs.mp.bz dummy

# Class change detection (for prep phase)
scoreboard objectives add mgs.mp.prev_class dummy

# Spectate timer (ticks remaining before respawn, 0 = not spectating)
scoreboard objectives add mgs.mp.spectate_timer dummy

# FFA ranking (1 = most kills, 2 = second, ..., 0 = unranked)
scoreboard objectives add mgs.mp.ffa_rank dummy

# Initialize team scores (only if not already set)
execute unless score #red mgs.mp.team matches -2147483648.. run scoreboard players set #red mgs.mp.team 0
execute unless score #blue mgs.mp.team matches -2147483648.. run scoreboard players set #blue mgs.mp.team 0

# Initialize game state (only if not yet set)
execute unless data storage mgs:multiplayer game run data modify storage mgs:multiplayer game set value {state:"lobby",gamemode:"tdm",score_limit:30,time_limit:12000,map_id:"hijacked"}


# Gamemode scoreboards
scoreboard objectives add mgs.mp.dom_progress dummy
scoreboard objectives add mgs.mp.dom_owner dummy
scoreboard objectives add mgs.mp.gm_timer dummy

# Create teams
execute unless score #mp_teams_created mgs.data matches 1 run team add mgs.red
execute unless score #mp_teams_created mgs.data matches 1 run team modify mgs.red color red
execute unless score #mp_teams_created mgs.data matches 1 run team modify mgs.red friendlyFire true
execute unless score #mp_teams_created mgs.data matches 1 run team modify mgs.red nametagVisibility hideForOtherTeams
execute unless score #mp_teams_created mgs.data matches 1 run team add mgs.blue
execute unless score #mp_teams_created mgs.data matches 1 run team modify mgs.blue color blue
execute unless score #mp_teams_created mgs.data matches 1 run team modify mgs.blue friendlyFire true
execute unless score #mp_teams_created mgs.data matches 1 run team modify mgs.blue nametagVisibility hideForOtherTeams
scoreboard players set #mp_teams_created mgs.data 1

data modify storage mgs:multiplayer classes_list set value [{id:"assault",name:"Assault",lore:"Versatile frontline",trigger_value:11,main_gun:"ak47",secondary_gun:"m1911",main_mag_count:3,secondary_mag_count:2,equip_display:"2x Frag, 1x Smoke",slots:[{slot:"hotbar.0",loot:"mgs:i/ak47",count:1,consumable:0b,bullets:0},{slot:"hotbar.1",loot:"mgs:i/m1911",count:1,consumable:0b,bullets:0},{slot:"hotbar.8",loot:"mgs:i/frag_grenade",count:2,consumable:0b,bullets:0},{slot:"hotbar.7",loot:"mgs:i/smoke_grenade",count:1,consumable:0b,bullets:0},{slot:"inventory.0",loot:"mgs:i/ak47_mag",count:1,consumable:0b,bullets:0},{slot:"inventory.1",loot:"mgs:i/ak47_mag",count:1,consumable:0b,bullets:0},{slot:"inventory.2",loot:"mgs:i/ak47_mag",count:1,consumable:0b,bullets:0},{slot:"inventory.3",loot:"mgs:i/m1911_mag",count:1,consumable:0b,bullets:0},{slot:"inventory.4",loot:"mgs:i/m1911_mag",count:1,consumable:0b,bullets:0}]},{id:"rifleman",name:"Rifleman",lore:"Accurate mid-range",trigger_value:12,main_gun:"m16a4",secondary_gun:"m9",main_mag_count:3,secondary_mag_count:2,equip_display:"1x Flash, 1x Smoke",slots:[{slot:"hotbar.0",loot:"mgs:i/m16a4",count:1,consumable:0b,bullets:0},{slot:"hotbar.1",loot:"mgs:i/m9",count:1,consumable:0b,bullets:0},{slot:"hotbar.8",loot:"mgs:i/flash_grenade",count:1,consumable:0b,bullets:0},{slot:"hotbar.7",loot:"mgs:i/smoke_grenade",count:1,consumable:0b,bullets:0},{slot:"inventory.0",loot:"mgs:i/m16a4_mag",count:1,consumable:0b,bullets:0},{slot:"inventory.1",loot:"mgs:i/m16a4_mag",count:1,consumable:0b,bullets:0},{slot:"inventory.2",loot:"mgs:i/m16a4_mag",count:1,consumable:0b,bullets:0},{slot:"inventory.3",loot:"mgs:i/m9_mag",count:1,consumable:0b,bullets:0},{slot:"inventory.4",loot:"mgs:i/m9_mag",count:1,consumable:0b,bullets:0}]},{id:"support",name:"Support",lore:"Suppressive heavy",trigger_value:13,main_gun:"m249",secondary_gun:"glock17",main_mag_count:3,secondary_mag_count:2,equip_display:"2x Smoke",slots:[{slot:"hotbar.0",loot:"mgs:i/m249",count:1,consumable:0b,bullets:0},{slot:"hotbar.1",loot:"mgs:i/glock17",count:1,consumable:0b,bullets:0},{slot:"hotbar.8",loot:"mgs:i/smoke_grenade",count:2,consumable:0b,bullets:0},{slot:"inventory.0",loot:"mgs:i/m249_mag",count:1,consumable:0b,bullets:0},{slot:"inventory.1",loot:"mgs:i/m249_mag",count:1,consumable:0b,bullets:0},{slot:"inventory.2",loot:"mgs:i/m249_mag",count:1,consumable:0b,bullets:0},{slot:"inventory.3",loot:"mgs:i/glock17_mag",count:1,consumable:0b,bullets:0},{slot:"inventory.4",loot:"mgs:i/glock17_mag",count:1,consumable:0b,bullets:0}]},{id:"sniper",name:"Sniper",lore:"Long-range precision",trigger_value:14,main_gun:"m24_4",secondary_gun:"deagle",main_mag_count:10,secondary_mag_count:2,equip_display:"1x Flash",slots:[{slot:"hotbar.0",loot:"mgs:i/m24_4",count:1,consumable:0b,bullets:0},{slot:"hotbar.1",loot:"mgs:i/deagle",count:1,consumable:0b,bullets:0},{slot:"hotbar.8",loot:"mgs:i/flash_grenade",count:1,consumable:0b,bullets:0},{slot:"inventory.0",loot:"mgs:i/m24_bullet",count:1,consumable:1b,bullets:10},{slot:"inventory.1",loot:"mgs:i/deagle_mag",count:1,consumable:0b,bullets:0},{slot:"inventory.2",loot:"mgs:i/deagle_mag",count:1,consumable:0b,bullets:0}]},{id:"smg",name:"SMG",lore:"Close quarters",trigger_value:15,main_gun:"mp7",secondary_gun:"glock18",main_mag_count:4,secondary_mag_count:2,equip_display:"2x Flash",slots:[{slot:"hotbar.0",loot:"mgs:i/mp7",count:1,consumable:0b,bullets:0},{slot:"hotbar.1",loot:"mgs:i/glock18",count:1,consumable:0b,bullets:0},{slot:"hotbar.8",loot:"mgs:i/flash_grenade",count:2,consumable:0b,bullets:0},{slot:"inventory.0",loot:"mgs:i/mp7_mag",count:1,consumable:0b,bullets:0},{slot:"inventory.1",loot:"mgs:i/mp7_mag",count:1,consumable:0b,bullets:0},{slot:"inventory.2",loot:"mgs:i/mp7_mag",count:1,consumable:0b,bullets:0},{slot:"inventory.3",loot:"mgs:i/mp7_mag",count:1,consumable:0b,bullets:0},{slot:"inventory.4",loot:"mgs:i/glock18_mag",count:1,consumable:0b,bullets:0},{slot:"inventory.5",loot:"mgs:i/glock18_mag",count:1,consumable:0b,bullets:0}]},{id:"shotgunner",name:"Shotgunner",lore:"Breaching / CQB",trigger_value:16,main_gun:"spas12",secondary_gun:"m9",main_mag_count:16,secondary_mag_count:2,equip_display:"2x Semtex",slots:[{slot:"hotbar.0",loot:"mgs:i/spas12",count:1,consumable:0b,bullets:0},{slot:"hotbar.1",loot:"mgs:i/m9",count:1,consumable:0b,bullets:0},{slot:"hotbar.8",loot:"mgs:i/semtex",count:2,consumable:0b,bullets:0},{slot:"inventory.0",loot:"mgs:i/spas12_shell",count:1,consumable:1b,bullets:16},{slot:"inventory.1",loot:"mgs:i/m9_mag",count:1,consumable:0b,bullets:0},{slot:"inventory.2",loot:"mgs:i/m9_mag",count:1,consumable:0b,bullets:0}]},{id:"engineer",name:"Engineer",lore:"Objective / demolitions",trigger_value:17,main_gun:"mp5",secondary_gun:"makarov",main_mag_count:3,secondary_mag_count:2,equip_display:"2x Semtex, 1x Smoke",slots:[{slot:"hotbar.0",loot:"mgs:i/mp5",count:1,consumable:0b,bullets:0},{slot:"hotbar.1",loot:"mgs:i/makarov",count:1,consumable:0b,bullets:0},{slot:"hotbar.8",loot:"mgs:i/semtex",count:2,consumable:0b,bullets:0},{slot:"hotbar.7",loot:"mgs:i/smoke_grenade",count:1,consumable:0b,bullets:0},{slot:"inventory.0",loot:"mgs:i/mp5_mag",count:1,consumable:0b,bullets:0},{slot:"inventory.1",loot:"mgs:i/mp5_mag",count:1,consumable:0b,bullets:0},{slot:"inventory.2",loot:"mgs:i/mp5_mag",count:1,consumable:0b,bullets:0},{slot:"inventory.3",loot:"mgs:i/makarov_mag",count:1,consumable:0b,bullets:0},{slot:"inventory.4",loot:"mgs:i/makarov_mag",count:1,consumable:0b,bullets:0}]},{id:"medic",name:"Medic",lore:"Team sustain",trigger_value:18,main_gun:"famas",secondary_gun:"m1911",main_mag_count:3,secondary_mag_count:2,equip_display:"2x Smoke",slots:[{slot:"hotbar.0",loot:"mgs:i/famas",count:1,consumable:0b,bullets:0},{slot:"hotbar.1",loot:"mgs:i/m1911",count:1,consumable:0b,bullets:0},{slot:"hotbar.8",loot:"mgs:i/smoke_grenade",count:2,consumable:0b,bullets:0},{slot:"inventory.0",loot:"mgs:i/famas_mag",count:1,consumable:0b,bullets:0},{slot:"inventory.1",loot:"mgs:i/famas_mag",count:1,consumable:0b,bullets:0},{slot:"inventory.2",loot:"mgs:i/famas_mag",count:1,consumable:0b,bullets:0},{slot:"inventory.3",loot:"mgs:i/m1911_mag",count:1,consumable:0b,bullets:0},{slot:"inventory.4",loot:"mgs:i/m1911_mag",count:1,consumable:0b,bullets:0}]},{id:"marksman",name:"Marksman",lore:"Semi-auto precision",trigger_value:19,main_gun:"svd",secondary_gun:"glock17",main_mag_count:3,secondary_mag_count:2,equip_display:"1x Flash, 1x Smoke",slots:[{slot:"hotbar.0",loot:"mgs:i/svd",count:1,consumable:0b,bullets:0},{slot:"hotbar.1",loot:"mgs:i/glock17",count:1,consumable:0b,bullets:0},{slot:"hotbar.8",loot:"mgs:i/flash_grenade",count:1,consumable:0b,bullets:0},{slot:"hotbar.7",loot:"mgs:i/smoke_grenade",count:1,consumable:0b,bullets:0},{slot:"inventory.0",loot:"mgs:i/svd_mag",count:1,consumable:0b,bullets:0},{slot:"inventory.1",loot:"mgs:i/svd_mag",count:1,consumable:0b,bullets:0},{slot:"inventory.2",loot:"mgs:i/svd_mag",count:1,consumable:0b,bullets:0},{slot:"inventory.3",loot:"mgs:i/glock17_mag",count:1,consumable:0b,bullets:0},{slot:"inventory.4",loot:"mgs:i/glock17_mag",count:1,consumable:0b,bullets:0}]},{id:"heavy",name:"Heavy",lore:"Armored suppressor",trigger_value:20,main_gun:"rpk",secondary_gun:"makarov",main_mag_count:3,secondary_mag_count:2,equip_display:"2x Frag",slots:[{slot:"hotbar.0",loot:"mgs:i/rpk",count:1,consumable:0b,bullets:0},{slot:"hotbar.1",loot:"mgs:i/makarov",count:1,consumable:0b,bullets:0},{slot:"hotbar.8",loot:"mgs:i/frag_grenade",count:2,consumable:0b,bullets:0},{slot:"inventory.0",loot:"mgs:i/rpk_mag",count:1,consumable:0b,bullets:0},{slot:"inventory.1",loot:"mgs:i/rpk_mag",count:1,consumable:0b,bullets:0},{slot:"inventory.2",loot:"mgs:i/rpk_mag",count:1,consumable:0b,bullets:0},{slot:"inventory.3",loot:"mgs:i/makarov_mag",count:1,consumable:0b,bullets:0},{slot:"inventory.4",loot:"mgs:i/makarov_mag",count:1,consumable:0b,bullets:0}]}]

# Class selection scoreboard (1-10 = class id, 0 = none)
scoreboard objectives add mgs.mp.class dummy

# Death detection for respawn
scoreboard objectives add mgs.mp.death_count deathCount

# Class menu right-click detection (warped fungus on a stick)
scoreboard objectives add mgs.class_menu minecraft.used:minecraft.warped_fungus_on_a_stick

## Custom loadout system
# Unique player IDs (auto-increment, used to identify loadout ownership)
# Global next-pid counter
# Player's default custom loadout ID (0 = none → use standard class)
# Editor state tracker (0 = not editing)
scoreboard objectives add mgs.mp.pid dummy
execute unless score #next_pid mgs.data matches 1.. run scoreboard players set #next_pid mgs.data 1
scoreboard objectives add mgs.mp.default dummy
scoreboard objectives add mgs.mp.edit_step dummy
# Pick-10 points remaining during loadout editing
scoreboard objectives add mgs.mp.edit_points dummy

# Constant for negation (used to store custom loadout ID as negative mp.class)
scoreboard players set #minus_one mgs.data -1

# Custom loadouts list (persists across reloads)
execute unless data storage mgs:multiplayer custom_loadouts run data modify storage mgs:multiplayer custom_loadouts set value []
# Per-player preference data (persists across reloads)
execute unless data storage mgs:multiplayer player_data run data modify storage mgs:multiplayer player_data set value []
# Auto-increment counter for loadout IDs
execute unless data storage mgs:multiplayer next_loadout_id run data modify storage mgs:multiplayer next_loadout_id set value 1

# Slot lookup tables for custom loadout editor (pre-computed at build time)
data modify storage mgs:multiplayer primary_slot_table set value [{id:"ak47",gun_slot:{slot:"hotbar.0",loot:"mgs:i/ak47",count:1,consumable:0b,bullets:0},mag_id:"ak47_mag",mag_consumable:0b,mag_bullets:0},{id:"m16a4",gun_slot:{slot:"hotbar.0",loot:"mgs:i/m16a4",count:1,consumable:0b,bullets:0},mag_id:"m16a4_mag",mag_consumable:0b,mag_bullets:0},{id:"famas",gun_slot:{slot:"hotbar.0",loot:"mgs:i/famas",count:1,consumable:0b,bullets:0},mag_id:"famas_mag",mag_consumable:0b,mag_bullets:0},{id:"aug",gun_slot:{slot:"hotbar.0",loot:"mgs:i/aug",count:1,consumable:0b,bullets:0},mag_id:"aug_mag",mag_consumable:0b,mag_bullets:0},{id:"m4a1",gun_slot:{slot:"hotbar.0",loot:"mgs:i/m4a1",count:1,consumable:0b,bullets:0},mag_id:"m4a1_mag",mag_consumable:0b,mag_bullets:0},{id:"fnfal",gun_slot:{slot:"hotbar.0",loot:"mgs:i/fnfal",count:1,consumable:0b,bullets:0},mag_id:"fnfal_mag",mag_consumable:0b,mag_bullets:0},{id:"g3a3",gun_slot:{slot:"hotbar.0",loot:"mgs:i/g3a3",count:1,consumable:0b,bullets:0},mag_id:"g3a3_mag",mag_consumable:0b,mag_bullets:0},{id:"scar17",gun_slot:{slot:"hotbar.0",loot:"mgs:i/scar17",count:1,consumable:0b,bullets:0},mag_id:"scar17_mag",mag_consumable:0b,mag_bullets:0},{id:"mp5",gun_slot:{slot:"hotbar.0",loot:"mgs:i/mp5",count:1,consumable:0b,bullets:0},mag_id:"mp5_mag",mag_consumable:0b,mag_bullets:0},{id:"mp7",gun_slot:{slot:"hotbar.0",loot:"mgs:i/mp7",count:1,consumable:0b,bullets:0},mag_id:"mp7_mag",mag_consumable:0b,mag_bullets:0},{id:"mac10",gun_slot:{slot:"hotbar.0",loot:"mgs:i/mac10",count:1,consumable:0b,bullets:0},mag_id:"mac10_mag",mag_consumable:0b,mag_bullets:0},{id:"ppsh41",gun_slot:{slot:"hotbar.0",loot:"mgs:i/ppsh41",count:1,consumable:0b,bullets:0},mag_id:"ppsh41_mag",mag_consumable:0b,mag_bullets:0},{id:"sten",gun_slot:{slot:"hotbar.0",loot:"mgs:i/sten",count:1,consumable:0b,bullets:0},mag_id:"sten_mag",mag_consumable:0b,mag_bullets:0},{id:"m249",gun_slot:{slot:"hotbar.0",loot:"mgs:i/m249",count:1,consumable:0b,bullets:0},mag_id:"m249_mag",mag_consumable:0b,mag_bullets:0},{id:"rpk",gun_slot:{slot:"hotbar.0",loot:"mgs:i/rpk",count:1,consumable:0b,bullets:0},mag_id:"rpk_mag",mag_consumable:0b,mag_bullets:0},{id:"svd",gun_slot:{slot:"hotbar.0",loot:"mgs:i/svd",count:1,consumable:0b,bullets:0},mag_id:"svd_mag",mag_consumable:0b,mag_bullets:0},{id:"m82",gun_slot:{slot:"hotbar.0",loot:"mgs:i/m82",count:1,consumable:0b,bullets:0},mag_id:"m82_mag",mag_consumable:0b,mag_bullets:0},{id:"mosin",gun_slot:{slot:"hotbar.0",loot:"mgs:i/mosin",count:1,consumable:0b,bullets:0},mag_id:"mosin_bullet",mag_consumable:1b,mag_bullets:10},{id:"m24",gun_slot:{slot:"hotbar.0",loot:"mgs:i/m24",count:1,consumable:0b,bullets:0},mag_id:"m24_bullet",mag_consumable:1b,mag_bullets:10},{id:"spas12",gun_slot:{slot:"hotbar.0",loot:"mgs:i/spas12",count:1,consumable:0b,bullets:0},mag_id:"spas12_shell",mag_consumable:1b,mag_bullets:16},{id:"m500",gun_slot:{slot:"hotbar.0",loot:"mgs:i/m500",count:1,consumable:0b,bullets:0},mag_id:"m500_shell",mag_consumable:1b,mag_bullets:12},{id:"m590",gun_slot:{slot:"hotbar.0",loot:"mgs:i/m590",count:1,consumable:0b,bullets:0},mag_id:"m590_shell",mag_consumable:1b,mag_bullets:16},{id:"rpg7",gun_slot:{slot:"hotbar.0",loot:"mgs:i/rpg7",count:1,consumable:0b,bullets:0},mag_id:"rpg7_rocket",mag_consumable:1b,mag_bullets:3}]
data modify storage mgs:multiplayer secondary_slot_table set value [{id:"m1911",gun_slot:{slot:"hotbar.1",loot:"mgs:i/m1911",count:1,consumable:0b,bullets:0},mag_id:"m1911_mag",mag_consumable:0b,mag_bullets:0},{id:"m9",gun_slot:{slot:"hotbar.1",loot:"mgs:i/m9",count:1,consumable:0b,bullets:0},mag_id:"m9_mag",mag_consumable:0b,mag_bullets:0},{id:"deagle",gun_slot:{slot:"hotbar.1",loot:"mgs:i/deagle",count:1,consumable:0b,bullets:0},mag_id:"deagle_mag",mag_consumable:0b,mag_bullets:0},{id:"makarov",gun_slot:{slot:"hotbar.1",loot:"mgs:i/makarov",count:1,consumable:0b,bullets:0},mag_id:"makarov_mag",mag_consumable:0b,mag_bullets:0},{id:"glock17",gun_slot:{slot:"hotbar.1",loot:"mgs:i/glock17",count:1,consumable:0b,bullets:0},mag_id:"glock17_mag",mag_consumable:0b,mag_bullets:0},{id:"glock18",gun_slot:{slot:"hotbar.1",loot:"mgs:i/glock18",count:1,consumable:0b,bullets:0},mag_id:"glock18_mag",mag_consumable:0b,mag_bullets:0},{id:"vz61",gun_slot:{slot:"hotbar.1",loot:"mgs:i/vz61",count:1,consumable:0b,bullets:0},mag_id:"vz61_mag",mag_consumable:0b,mag_bullets:0}]

# Initialize multiplayer maps storage (empty list, only if not set)
execute unless data storage mgs:maps multiplayer run data modify storage mgs:maps multiplayer set value []

## Missions scoreboards
scoreboard objectives add mgs.mi.in_game dummy
scoreboard objectives add mgs.mi.timer dummy
scoreboard objectives add mgs.mi.total_enemies dummy
scoreboard objectives add mgs.mi.kills dummy
scoreboard objectives add mgs.mi.deaths dummy
scoreboard objectives add mgs.mi.kill_total totalKillCount
scoreboard objectives add mgs.mi.kill_base dummy

# Boundary checking coords (reuse mp prefix scores)
scoreboard objectives add mgs.mp.bx dummy
scoreboard objectives add mgs.mp.by dummy
scoreboard objectives add mgs.mp.bz dummy

# Mission mob team (created once)
execute unless score #mi_mob_team_created mgs.data matches 1 run team add mgs.mi_mobs
execute unless score #mi_mob_team_created mgs.data matches 1 run team modify mgs.mi_mobs color dark_red
execute unless score #mi_mob_team_created mgs.data matches 1 run team modify mgs.mi_mobs friendlyFire false
execute unless score #mi_mob_team_created mgs.data matches 1 run scoreboard players set #mi_mob_team_created mgs.data 1

# Initialize missions game state
execute unless data storage mgs:missions game run data modify storage mgs:missions game set value {state:"lobby",map_id:""}

# Map editor scoreboards
scoreboard objectives add mgs.mp.map_edit dummy
scoreboard objectives add mgs.mp.map_idx dummy
scoreboard objectives add mgs.mp.map_mode dummy
scoreboard objectives add mgs.mp.map_disp dummy

# Reuse warped fungus on stick detection (shared with class menu)
scoreboard objectives add mgs.class_menu minecraft.used:minecraft.warped_fungus_on_a_stick

# Initialize maps storage for all modes
execute unless data storage mgs:maps multiplayer run data modify storage mgs:maps multiplayer set value []
execute unless data storage mgs:maps zombies run data modify storage mgs:maps zombies set value []
execute unless data storage mgs:maps missions run data modify storage mgs:maps missions set value []

# Set scoreboard constants for mgs.data
scoreboard players set #2 mgs.data 2
scoreboard players set #4 mgs.data 4
scoreboard players set #5 mgs.data 5
scoreboard players set #10 mgs.data 10
scoreboard players set #20 mgs.data 20
scoreboard players set #60 mgs.data 60
scoreboard players set #100 mgs.data 100
scoreboard players set #200 mgs.data 200
scoreboard players set #1000 mgs.data 1000
scoreboard players set #1000000 mgs.data 1000000

