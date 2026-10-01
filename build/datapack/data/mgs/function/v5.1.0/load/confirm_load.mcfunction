
#> mgs:v5.1.0/load/confirm_load
#
# @within	mgs:v5.1.0/load/valid_dependencies
#

scoreboard objectives add mgs.player.config trigger

# Off by default.
scoreboard objectives add mgs.player.hitmarker dummy
scoreboard objectives add mgs.player.damage_debug dummy

## Length of the selected item id, to detect a change.
scoreboard objectives add mgs.previous_selected dummy

# Continuous right-click detection.
scoreboard objectives add mgs.pending_clicks dummy

# Held right click, as opposed to a single tap.
scoreboard objectives add mgs.held_click dummy

# Shots fired in the current burst.
scoreboard objectives add mgs.burst_count dummy

# The drop key switches fire mode.
scoreboard objectives add mgs.dropped minecraft.custom:minecraft.drop

# Expiry tick before the next shot.
scoreboard objectives add mgs.cooldown dummy

# Was zooming, so the slowness can be removed.
scoreboard objectives add mgs.zoom dummy

# Last selected weapon id, for switch detection.
scoreboard objectives add mgs.last_selected dummy

# Bullets in the selected weapon.
scoreboard objectives add mgs.remaining_bullets dummy

# Sum of the magazine bullets in the inventory, updated on reload and after about 60 idle ticks.
scoreboard objectives add mgs.reserve_ammo dummy

# Room acoustics, for the crack sounds.
scoreboard objectives add mgs.acoustics_level dummy

# Ticks since the last muzzle flash this player saw.
scoreboard objectives add mgs.last_muzzle_flash dummy

## Server config (#projectile_explosion_power, ...): 0 means no block destruction.
scoreboard objectives add mgs.config dummy

## From SpecialScores.ALL, which game starts also wipe.
# Instant kill: duration in ticks (kills entities in one hit, except mgs.no_instant_kill tagged)
scoreboard objectives add mgs.special.instant_kill dummy
# Infinite ammo: duration in ticks (don't consume ammo, set ammo to max capacity)
scoreboard objectives add mgs.special.infinite_ammo dummy
# Double points: duration in ticks (double points earned from kills/hits in zombies)
scoreboard objectives add mgs.special.double_points dummy
# Quick reload: percentage faster reload (20 = 20% faster, 50 = 50% faster)
scoreboard objectives add mgs.special.quick_reload dummy
# Quick swap: percentage faster weapon switch (20 = 20% faster, 50 = 50% faster)
scoreboard objectives add mgs.special.quick_swap dummy
# Double Tap perk: bullet damage x2
scoreboard objectives add mgs.special.double_tap dummy
# PhD Flopper perk: immune to explosive self-damage (fall damage handled by attribute)
scoreboard objectives add mgs.special.phd_flopper dummy
# Deadshot Daiquiri perk: 65% weapon spread + recoil
scoreboard objectives add mgs.special.deadshot dummy
# Timeslip perk: faster traps / Mystery Box / Pack-a-Punch for the owner
scoreboard objectives add mgs.special.timeslip dummy
# Electric Cherry perk: reload discharges a shock that damages/stuns nearby zombies
scoreboard objectives add mgs.special.electric_cherry dummy
# Widow's Wine perk: web grenades + web-on-hurt passive + stronger knife
scoreboard objectives add mgs.special.widows_wine dummy
# Multiplayer loadout perk flags, set on loadout apply
scoreboard objectives add mgs.special.juggernaut dummy
scoreboard objectives add mgs.special.scavenger dummy
scoreboard objectives add mgs.special.flak_jacket dummy
scoreboard objectives add mgs.special.tracker dummy
scoreboard objectives add mgs.special.tactical_mask dummy
scoreboard objectives add mgs.special.overkill dummy
scoreboard objectives add mgs.special.quick_fix dummy
# Damage per second, accumulated then snapshotted for the actionbar.
scoreboard objectives add mgs.dps dummy
scoreboard objectives add mgs.previous_dps dummy
scoreboard objectives add mgs.dps_timer dummy

# Forces an actionbar refresh for changes the idle gate cannot see (fire-mode toggle).
scoreboard objectives add mgs.ab_force dummy

scoreboard players add #slow_bullet_count mgs.data 0

# Semtex pairing: a unique id objective and a global counter.
scoreboard objectives add mgs.grenade_launch dummy
scoreboard objectives add mgs.stuck_id dummy

# Accumulated tumble angle (1e-4 rad units).
scoreboard objectives add mgs.grenade_spin dummy
scoreboard players set #semtex_id mgs.data 0

# Defaults, only when unset.
execute unless score #projectile_explosion_power mgs.config matches -2147483648.. run scoreboard players set #projectile_explosion_power mgs.config 0
execute unless score #grenade_explosion_power mgs.config matches -2147483648.. run scoreboard players set #grenade_explosion_power mgs.config 0
execute unless score #max_ammo_reload_weapons mgs.config matches -2147483648.. run scoreboard players set #max_ammo_reload_weapons mgs.config 0
execute unless score #damage_debug mgs.config matches -2147483648.. run scoreboard players set #damage_debug mgs.config 0

# Health regeneration, shared by every mode.
scoreboard objectives add mgs.last_hit dummy
scoreboard objectives add mgs.hp_prev dummy

# Read-only criteria the server keeps current: a score read instead of serializing the player NBT for Health or foodLevel.
# mgs.health = ceil(health + absorption), and the pack has no absorption source.
scoreboard objectives add mgs.health health
scoreboard objectives add mgs.food food

# Global stopwatch, a lag-immune wall clock. Recreated on every load, which is harmless: only per-tick deltas are used.
stopwatch remove mgs:clock
stopwatch create mgs:clock
scoreboard players set #real_prev mgs.data 0


# Confirm load
tellraw @a[tag=convention.debug] {"translate":"mgs.loaded_mc_guns_system_v5_1_0","color":"green"}
scoreboard players set #mgs.loaded load.status 1

scoreboard objectives add mgs.flash_id dummy
scoreboard objectives add mgs.flash_slot dummy
scoreboard objectives add mgs.flash_off dummy
scoreboard objectives add mgs.zoom_fx dummy
scoreboard objectives add mgs.zoom_fx_off dummy
scoreboard objectives add mgs.cross_from dummy
scoreboard objectives add mgs.cross_to dummy
scoreboard objectives add mgs.hurt_fx dummy
scoreboard objectives add mgs.hurt_from dummy
scoreboard objectives add mgs.hurt_pending dummy
scoreboard objectives add mgs.hurt_fall_until dummy
scoreboard objectives add mgs.hurt_out_until dummy
scoreboard objectives add mgs.fx_deaths deathCount
scoreboard objectives add mgs.fx_rejoins custom:leave_game
scoreboard players set #fx_sweep_period mgs.data 40

execute as @a run function mgs:v5.1.0/player/fx_reset

# Black Ops style stamina, per player.
scoreboard objectives add mgs.stam dummy
scoreboard objectives add mgs.stam_max dummy
scoreboard objectives add mgs.stam_bonus dummy
scoreboard objectives add mgs.stam_rest dummy
scoreboard objectives add mgs.stam_out dummy
scoreboard objectives add mgs.stam_seen dummy

# Counts swim ticks, so the drain applies once per SWIM_DRAIN_FACTOR ticks (see stamina_swim_drain).
scoreboard objectives add mgs.stam_swim dummy

# Set while refill pulses may have left invisible saturation; only then does the at-target branch read foodSaturationLevel to burn it off.
scoreboard objectives add mgs.stam_dirty dummy

# The tick loop is skipped at 0.
scoreboard players add #armed_mob_count mgs.data 0

scoreboard objectives add mgs.mob.timer dummy
scoreboard objectives add mgs.mob.active_time dummy
scoreboard objectives add mgs.mob.sleep_time dummy

# Shared vanilla teams
team add mgs.red
team modify mgs.red color red
team modify mgs.red friendlyFire false
team modify mgs.red nametagVisibility hideForOtherTeams
team add mgs.blue
team modify mgs.blue color blue
team modify mgs.blue friendlyFire false
team modify mgs.blue nametagVisibility hideForOtherTeams
team add mgs.ffa
team modify mgs.ffa color yellow
team modify mgs.ffa friendlyFire true
team modify mgs.ffa nametagVisibility never
team add mgs.zombies
team modify mgs.zombies color yellow
team modify mgs.zombies friendlyFire false
team modify mgs.zombies nametagVisibility hideForOtherTeams
team add mgs.mi_mobs
team modify mgs.mi_mobs color dark_red
team modify mgs.mi_mobs friendlyFire true
team modify mgs.mi_mobs nametagVisibility always

# Ticks before a dropped gun despawns.
scoreboard objectives add mgs.drop_timer dummy

# xp_total is authoritative; xp_level and xp_prog are caches derived from it.
scoreboard objectives add mgs.mp.xp_total dummy
scoreboard objectives add mgs.mp.xp_level dummy
scoreboard objectives add mgs.mp.xp_prog dummy
scoreboard objectives add mgs.mp.xp_session dummy
scoreboard objectives add mgs.zb.xp_total dummy
scoreboard objectives add mgs.zb.xp_level dummy
scoreboard objectives add mgs.zb.xp_prog dummy
scoreboard objectives add mgs.zb.xp_pts_prev dummy
scoreboard objectives add mgs.zb.xp_spent_acc dummy

# 14 challenge counters; the level chains read mgs.mp.xp_level and mgs.zb.xp_level.
scoreboard objectives add mgs.adv.mp.kills dummy
scoreboard objectives add mgs.adv.mp.headshots dummy
scoreboard objectives add mgs.adv.mp.objectives dummy
scoreboard objectives add mgs.adv.mp.wins dummy
scoreboard objectives add mgs.adv.mi.completed dummy
scoreboard objectives add mgs.adv.mi.kills dummy
scoreboard objectives add mgs.adv.zb.kills dummy
scoreboard objectives add mgs.adv.zb.headshots dummy
scoreboard objectives add mgs.adv.zb.best_round dummy
scoreboard objectives add mgs.adv.zb.revives dummy
scoreboard objectives add mgs.adv.zb.perks dummy
scoreboard objectives add mgs.adv.zb.pap dummy
scoreboard objectives add mgs.adv.zb.box dummy
scoreboard objectives add mgs.adv.zb.spending dummy

scoreboard objectives add mgs.adv.caught dummy
scoreboard players reset * mgs.adv.caught

scoreboard objectives add mgs.zb.in_game dummy
scoreboard objectives add mgs.zb.points dummy
scoreboard objectives add mgs.zb.kills dummy
scoreboard objectives add mgs.zb.downs dummy

# Index into LETHAL_GRENADE_IDS (0 = frag), so an emptied lethal slot refills the bought type (see inventory).
scoreboard objectives add mgs.zb.lethal_type dummy

# zb.passive: 0 none, 1 points x1.2, 2 power-ups x1.5. zb.ability: 0 none, 1 coward, 2 guardian.
# zb.ability_cd: rounds of cooldown left (0 = ready).
scoreboard objectives add mgs.zb.passive dummy
scoreboard objectives add mgs.zb.ability dummy
scoreboard objectives add mgs.zb.ability_cd dummy

# Ticks to this player's next horde vocal.
scoreboard objectives add mgs.zb.horde_cd dummy

# #total_tick when each vocal channel frees up (see vocals). Never reset: #total_tick only grows,
# and an unset score fails the `>` test, which reads as ready.
scoreboard objectives add mgs.zb.vox_sprint dummy
scoreboard objectives add mgs.zb.vox_attack dummy
scoreboard objectives add mgs.zb.vox_death dummy

scoreboard objectives add mgs.zb.spawn.gid dummy

# Held by spawn markers, and by zombies as the last spawn they used, so a rescue never reuses it.
scoreboard objectives add mgs.zb.spawn.sid dummy

scoreboard objectives add mgs.zb.sb_rank dummy

scoreboard objectives add mgs.zb.rise_tick dummy

# totalKillCount, and the baseline snapshot.
scoreboard objectives add mgs.total_kills totalKillCount
scoreboard objectives add mgs.zb.prev_kills dummy

scoreboard objectives add mgs.zb.stuck_x dummy
scoreboard objectives add mgs.zb.stuck_z dummy
scoreboard objectives add mgs.zb.stuck_ticks dummy
scoreboard objectives add mgs.zb.stuck_dist dummy

execute unless data storage mgs:zombies game run data modify storage mgs:zombies game set value {state:"lobby",map_id:"",round:0}

# "vanilla": classic CoD zombies; "zonweeb": passives, abilities and special zombies.
execute unless data storage mgs:zombies game.variant run data modify storage mgs:zombies game.variant set value "zonweeb"

# Extended through a function tag.
execute unless data storage mgs:zombies mystery_box_pool run data modify storage mgs:zombies mystery_box_pool set value []

# Ticks left before the teleport-rescue fallback.
scoreboard objectives add mgs.zb.escort_ttl dummy

# Gates the per-tick escorted-zombie scan.
scoreboard players add #zb_escort_count mgs.data 0

# One-shot target of the next escort/start, reset there: 0 nearest player (stuck rescue, PaP lure),
# 1 a thrown monkey bomb, 2 the walk-to spot pinned on the zombie (data.walk_to).
scoreboard players add #zb_escort_mode mgs.data 0

# Zombies and escort traders are allied, so the trader's AvoidEntityGoal(Zombie) never fires (it would flee at sprint speed)
# and zombies never attack it. Created at load, so a mid-game /reload cannot lose it. pushOtherTeams: members do not push
# each other (the zombie overlaps its trader) but still push players and everything else.
team add mgs.horde
team modify mgs.horde collisionRule pushOtherTeams

# Shared by a box's interaction entity and its pull display.
scoreboard objectives add mgs.mb.box dummy
# >0 spinning, <=0 ready window.
scoreboard objectives add mgs.mb.anim dummy
# 1 when the buyer owns Timeslip (2x spin).
scoreboard objectives add mgs.mb.timeslip dummy
# 1 when the pull ends in a box move (active box only, never during a Fire Sale).
scoreboard objectives add mgs.mb.willmove dummy
# Stable player id, assigned on first pull. During a Fire Sale one player can run several pulls,
# so the buyer is stored per display (mb.buyer).
scoreboard objectives add mgs.mb.pid dummy
scoreboard objectives add mgs.mb.buyer dummy

scoreboard objectives add mgs.zb.pap.id dummy
scoreboard objectives add mgs.zb.pap.price dummy
scoreboard objectives add mgs.zb.pap.power dummy
scoreboard objectives add mgs.pap_anim dummy
# 1 when the starting player owns Timeslip (3x animation).
scoreboard objectives add mgs.zb.pap.timeslip dummy

# For cleanup when the weapon is lost or collected.
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
data modify storage mgs:zombies camo_variants._default set value ["gold","autumn","galaxy","red_polymer_stripes"]

scoreboard objectives add mgs.zb.barricade.id dummy
scoreboard objectives add mgs.zb.barricade.state dummy
scoreboard objectives add mgs.zb.barricade.r_timer dummy
scoreboard objectives add mgs.zb.barricade.rp_timer dummy
scoreboard objectives add mgs.zb.barricade.radius dummy
scoreboard objectives add mgs.zb.barricade.removing_id dummy
scoreboard objectives add mgs.zb.barricade.repairing_id dummy
# Reset each round; only 25 repairs per round pay.
scoreboard objectives add mgs.zb.barricade_repairs dummy

# #total_tick when each barricade sound frees up, as in vocals: never reset, and an unset score reads as ready.
scoreboard objectives add mgs.zb.barricade.bang_at dummy
scoreboard objectives add mgs.zb.barricade.rep_at dummy

scoreboard objectives add mgs.zb.pu.type dummy
scoreboard objectives add mgs.zb.pu.timer dummy
# Tick of the last player weapon hit, so only player kills drop.
scoreboard objectives add mgs.zb.player_hit dummy

scoreboard objectives add mgs.zb.door.link dummy
scoreboard objectives add mgs.zb.door.price dummy
scoreboard objectives add mgs.zb.door.bgid dummy
scoreboard objectives add mgs.zb.door.anim dummy
scoreboard objectives add mgs.zb.door.rot dummy
# Chip-in: chunk size (0 = off) and what the group paid; progress is global, so `paid` is mirrored on the whole link group.
scoreboard objectives add mgs.zb.door.partial dummy
scoreboard objectives add mgs.zb.door.paid dummy

scoreboard objectives add mgs.zb.wb.id dummy
scoreboard objectives add mgs.zb.wb.price dummy
scoreboard objectives add mgs.zb.wb.rfprice dummy
scoreboard objectives add mgs.zb.wb.rfpap dummy

scoreboard objectives add mgs.zb.perk.id dummy
scoreboard objectives add mgs.zb.perk.price dummy
# Kept so dynamic discounts (solo Quick Revive) can be reverted.
scoreboard objectives add mgs.zb.perk.base_price dummy
scoreboard objectives add mgs.zb.perk.power dummy
# 0 = buy in one payment.
scoreboard objectives add mgs.zb.perk.partial dummy

scoreboard objectives add mgs.zb.perk.juggernog dummy
scoreboard objectives add mgs.zb.perk.speed_cola dummy
scoreboard objectives add mgs.zb.perk.double_tap dummy
scoreboard objectives add mgs.zb.perk.quick_revive dummy
scoreboard objectives add mgs.zb.perk.mule_kick dummy
scoreboard objectives add mgs.zb.perk.stamin_up dummy
scoreboard objectives add mgs.zb.perk.phd_flopper dummy
scoreboard objectives add mgs.zb.perk.deadshot dummy
scoreboard objectives add mgs.zb.perk.timeslip dummy
scoreboard objectives add mgs.zb.perk.electric_cherry dummy
scoreboard objectives add mgs.zb.perk.tombstone dummy
scoreboard objectives add mgs.zb.perk.whos_who dummy
scoreboard objectives add mgs.zb.perk.dying_wish dummy
scoreboard objectives add mgs.zb.perk.widows_wine dummy

scoreboard objectives add mgs.zb.perkpaid.juggernog dummy
scoreboard objectives add mgs.zb.perkpaid.speed_cola dummy
scoreboard objectives add mgs.zb.perkpaid.double_tap dummy
scoreboard objectives add mgs.zb.perkpaid.quick_revive dummy
scoreboard objectives add mgs.zb.perkpaid.mule_kick dummy
scoreboard objectives add mgs.zb.perkpaid.stamin_up dummy
scoreboard objectives add mgs.zb.perkpaid.phd_flopper dummy
scoreboard objectives add mgs.zb.perkpaid.deadshot dummy
scoreboard objectives add mgs.zb.perkpaid.timeslip dummy
scoreboard objectives add mgs.zb.perkpaid.electric_cherry dummy
scoreboard objectives add mgs.zb.perkpaid.tombstone dummy
scoreboard objectives add mgs.zb.perkpaid.whos_who dummy
scoreboard objectives add mgs.zb.perkpaid.dying_wish dummy
scoreboard objectives add mgs.zb.perkpaid.widows_wine dummy

# Last discharge (gametime).
scoreboard objectives add mgs.zb.ec_last dummy
# Widow's Wine: last web burst (gametime).
scoreboard objectives add mgs.zb.ww_last dummy
# Dying Wish: uses (escalating cooldown), cooldown, berserk timer.
scoreboard objectives add mgs.zb.dw_uses dummy
scoreboard objectives add mgs.zb.dw_cd dummy
scoreboard objectives add mgs.zb.dw_timer dummy
# Tombstone: state (0 pending, 1 active) and recovery timer; the marker also carries zb.downed_id for downed_id_match.
scoreboard objectives add mgs.zb.ts.state dummy
scoreboard objectives add mgs.zb.ts.timer dummy
# Tombstone: the owner's perks when they went down.
scoreboard objectives add mgs.zb.tsp.juggernog dummy
scoreboard objectives add mgs.zb.tsp.speed_cola dummy
scoreboard objectives add mgs.zb.tsp.double_tap dummy
scoreboard objectives add mgs.zb.tsp.quick_revive dummy
scoreboard objectives add mgs.zb.tsp.mule_kick dummy
scoreboard objectives add mgs.zb.tsp.stamin_up dummy
scoreboard objectives add mgs.zb.tsp.phd_flopper dummy
scoreboard objectives add mgs.zb.tsp.deadshot dummy
scoreboard objectives add mgs.zb.tsp.timeslip dummy
scoreboard objectives add mgs.zb.tsp.electric_cherry dummy
scoreboard objectives add mgs.zb.tsp.whos_who dummy
scoreboard objectives add mgs.zb.tsp.dying_wish dummy
scoreboard objectives add mgs.zb.tsp.widows_wine dummy

scoreboard objectives add mgs.zb.wf.id dummy
scoreboard objectives add mgs.zb.wf.price dummy
scoreboard objectives add mgs.zb.wf.power dummy
scoreboard objectives add mgs.zb.wf.allperks dummy
# Orb: timer (>0 spinning, <=0 ready window), buyer pid, chosen perk index.
scoreboard objectives add mgs.zb.wf.anim dummy
scoreboard objectives add mgs.zb.wf.buyer dummy
scoreboard objectives add mgs.zb.wf.perk dummy
# 1 when the buyer owns Timeslip (2x spin, like the Mystery Box).
scoreboard objectives add mgs.zb.wf.timeslip dummy
# 1 when this pull roams the machine (teddy bear) instead of granting a perk.
scoreboard objectives add mgs.zb.wf.willmove dummy
# Refunded when the pull roams.
scoreboard objectives add mgs.zb.wf.paid dummy
# Stable buyer id, assigned on first use.
scoreboard objectives add mgs.zb.wf_pid dummy

# zb.ww.id links the owner to the body and survives later normal downs, unlike zb.downed_id.
# Bleed and revive progress use the owner's normal zb.bleed and zb.revive_p scores.
scoreboard objectives add mgs.zb.ww.id dummy
scoreboard objectives add mgs.zb.wwp.juggernog dummy
scoreboard objectives add mgs.zb.wwp.speed_cola dummy
scoreboard objectives add mgs.zb.wwp.double_tap dummy
scoreboard objectives add mgs.zb.wwp.quick_revive dummy
scoreboard objectives add mgs.zb.wwp.mule_kick dummy
scoreboard objectives add mgs.zb.wwp.stamin_up dummy
scoreboard objectives add mgs.zb.wwp.phd_flopper dummy
scoreboard objectives add mgs.zb.wwp.deadshot dummy
scoreboard objectives add mgs.zb.wwp.timeslip dummy
scoreboard objectives add mgs.zb.wwp.electric_cherry dummy
scoreboard objectives add mgs.zb.wwp.tombstone dummy
scoreboard objectives add mgs.zb.wwp.dying_wish dummy
scoreboard objectives add mgs.zb.wwp.widows_wine dummy

scoreboard objectives add mgs.zb.downed dummy
scoreboard objectives add mgs.zb.bleed dummy
scoreboard objectives add mgs.zb.revive_p dummy

scoreboard objectives add mgs.zb.qr_uses dummy

# Links a player to their mannequin.
scoreboard objectives add mgs.zb.downed_id dummy

scoreboard objectives add mgs.zb.trap.id dummy
scoreboard objectives add mgs.zb.trap.price dummy
scoreboard objectives add mgs.zb.trap.power dummy
scoreboard objectives add mgs.zb.trap.type dummy
scoreboard objectives add mgs.zb.trap.dur dummy
scoreboard objectives add mgs.zb.trap.cd_max dummy
# 1 when the activator owns Timeslip (cooldown at 75%).
scoreboard objectives add mgs.zb.trap.timeslip dummy
scoreboard objectives add mgs.zb.trap.timer dummy
scoreboard objectives add mgs.zb.trap.cd dummy
scoreboard objectives add mgs.zb.trap.rx dummy
scoreboard objectives add mgs.zb.trap.ry dummy
scoreboard objectives add mgs.zb.trap.rz dummy

## 1 red, 2 blue, 0 none or spectator.
scoreboard objectives add mgs.mp.team dummy
scoreboard objectives add mgs.mp.kills dummy
scoreboard objectives add mgs.mp.deaths dummy
# 1 while in an active game.
scoreboard objectives add mgs.mp.in_game dummy

scoreboard objectives add mgs.mp.bx dummy
scoreboard objectives add mgs.mp.by dummy
scoreboard objectives add mgs.mp.bz dummy

# Which of the 4 boundary-check phases a player is in (see enforce_bounds); #bphase_next is the round-robin cursor.
scoreboard objectives add mgs.mp.bphase dummy
scoreboard players set #bphase_next mgs.data 0

# Class change detection during prep.
scoreboard objectives add mgs.mp.prev_class dummy

# Ticks left before respawn, 0 when not spectating.
scoreboard objectives add mgs.mp.spectate_timer dummy

# 1 for most kills, 0 unranked.
scoreboard objectives add mgs.mp.ffa_rank dummy

execute unless score #red mgs.mp.team matches -2147483648.. run scoreboard players set #red mgs.mp.team 0
execute unless score #blue mgs.mp.team matches -2147483648.. run scoreboard players set #blue mgs.mp.team 0

execute unless data storage mgs:multiplayer game run data modify storage mgs:multiplayer game set value {state:"lobby",gamemode:"tdm",score_limit:30,time_limit:12000,map_id:"hijacked"}

scoreboard objectives add mgs.mp.dom_progress dummy
scoreboard objectives add mgs.mp.dom_owner dummy
scoreboard objectives add mgs.demo_state dummy
scoreboard objectives add mgs.demo_prog dummy
scoreboard objectives add mgs.demo_fuse dummy
scoreboard objectives add mgs.demo_owner dummy

data modify storage mgs:multiplayer classes_list set value [{id:"assault",name:"Assault",lore:"Versatile frontline",trigger_value:11,main_gun:"ak47",secondary_gun:"m1911",main_mag_count:3,secondary_mag_count:2,equip_display:"2x Frag, 1x Smoke",perks_display:"Sleight of Hand, Scavenger, Fast Hands",perks:["quick_reload","scavenger","quick_swap"],slots:[{slot:"hotbar.1",loot:"mgs:i/ak47",count:1,consumable:0b,bullets:0},{slot:"hotbar.2",loot:"mgs:i/m1911",count:1,consumable:0b,bullets:0},{slot:"hotbar.8",loot:"mgs:i/frag_grenade",count:2,consumable:0b,bullets:0},{slot:"hotbar.7",loot:"mgs:i/smoke_grenade",count:1,consumable:0b,bullets:0},{slot:"inventory.0",loot:"mgs:i/ak47_mag",count:1,consumable:0b,bullets:0},{slot:"inventory.1",loot:"mgs:i/ak47_mag",count:1,consumable:0b,bullets:0},{slot:"inventory.2",loot:"mgs:i/ak47_mag",count:1,consumable:0b,bullets:0},{slot:"inventory.3",loot:"mgs:i/m1911_mag",count:1,consumable:0b,bullets:0},{slot:"inventory.4",loot:"mgs:i/m1911_mag",count:1,consumable:0b,bullets:0}]},{id:"rifleman",name:"Rifleman",lore:"Accurate mid-range",trigger_value:12,main_gun:"m16a4",secondary_gun:"m9",main_mag_count:3,secondary_mag_count:2,equip_display:"1x Flash, 1x Smoke",perks_display:"Sleight of Hand, Tactical Mask, Tracker",perks:["quick_reload","tactical_mask","tracker"],slots:[{slot:"hotbar.1",loot:"mgs:i/m16a4",count:1,consumable:0b,bullets:0},{slot:"hotbar.2",loot:"mgs:i/m9",count:1,consumable:0b,bullets:0},{slot:"hotbar.8",loot:"mgs:i/flash_grenade",count:1,consumable:0b,bullets:0},{slot:"hotbar.7",loot:"mgs:i/smoke_grenade",count:1,consumable:0b,bullets:0},{slot:"inventory.0",loot:"mgs:i/m16a4_mag",count:1,consumable:0b,bullets:0},{slot:"inventory.1",loot:"mgs:i/m16a4_mag",count:1,consumable:0b,bullets:0},{slot:"inventory.2",loot:"mgs:i/m16a4_mag",count:1,consumable:0b,bullets:0},{slot:"inventory.3",loot:"mgs:i/m9_mag",count:1,consumable:0b,bullets:0},{slot:"inventory.4",loot:"mgs:i/m9_mag",count:1,consumable:0b,bullets:0}]},{id:"support",name:"Support",lore:"Suppressive heavy",trigger_value:13,main_gun:"m249",secondary_gun:"glock17",main_mag_count:3,secondary_mag_count:2,equip_display:"2x Smoke",perks_display:"Scavenger, Juggernaut, Flak Jacket",perks:["scavenger","juggernaut","flak_jacket"],slots:[{slot:"hotbar.1",loot:"mgs:i/m249",count:1,consumable:0b,bullets:0},{slot:"hotbar.2",loot:"mgs:i/glock17",count:1,consumable:0b,bullets:0},{slot:"hotbar.8",loot:"mgs:i/smoke_grenade",count:2,consumable:0b,bullets:0},{slot:"inventory.0",loot:"mgs:i/m249_mag",count:1,consumable:0b,bullets:0},{slot:"inventory.1",loot:"mgs:i/m249_mag",count:1,consumable:0b,bullets:0},{slot:"inventory.2",loot:"mgs:i/m249_mag",count:1,consumable:0b,bullets:0},{slot:"inventory.3",loot:"mgs:i/glock17_mag",count:1,consumable:0b,bullets:0},{slot:"inventory.4",loot:"mgs:i/glock17_mag",count:1,consumable:0b,bullets:0}]},{id:"sniper",name:"Sniper",lore:"Long-range precision",trigger_value:14,main_gun:"m24_4",secondary_gun:"deagle",main_mag_count:10,secondary_mag_count:2,equip_display:"1x Flash",perks_display:"Fast Hands, Tracker, Tactical Mask",perks:["quick_swap","tracker","tactical_mask"],slots:[{slot:"hotbar.1",loot:"mgs:i/m24_4",count:1,consumable:0b,bullets:0},{slot:"hotbar.2",loot:"mgs:i/deagle",count:1,consumable:0b,bullets:0},{slot:"hotbar.8",loot:"mgs:i/flash_grenade",count:1,consumable:0b,bullets:0},{slot:"inventory.0",loot:"mgs:i/m24_bullet",count:1,consumable:1b,bullets:10},{slot:"inventory.1",loot:"mgs:i/deagle_mag",count:1,consumable:0b,bullets:0},{slot:"inventory.2",loot:"mgs:i/deagle_mag",count:1,consumable:0b,bullets:0}]},{id:"smg",name:"SMG",lore:"Close quarters",trigger_value:15,main_gun:"mp7",secondary_gun:"glock18",main_mag_count:4,secondary_mag_count:2,equip_display:"2x Flash",perks_display:"Sleight of Hand, Fast Hands, Quick Fix",perks:["quick_reload","quick_swap","quick_fix"],slots:[{slot:"hotbar.1",loot:"mgs:i/mp7",count:1,consumable:0b,bullets:0},{slot:"hotbar.2",loot:"mgs:i/glock18",count:1,consumable:0b,bullets:0},{slot:"hotbar.8",loot:"mgs:i/flash_grenade",count:2,consumable:0b,bullets:0},{slot:"inventory.0",loot:"mgs:i/mp7_mag",count:1,consumable:0b,bullets:0},{slot:"inventory.1",loot:"mgs:i/mp7_mag",count:1,consumable:0b,bullets:0},{slot:"inventory.2",loot:"mgs:i/mp7_mag",count:1,consumable:0b,bullets:0},{slot:"inventory.3",loot:"mgs:i/mp7_mag",count:1,consumable:0b,bullets:0},{slot:"inventory.4",loot:"mgs:i/glock18_mag",count:1,consumable:0b,bullets:0},{slot:"inventory.5",loot:"mgs:i/glock18_mag",count:1,consumable:0b,bullets:0}]},{id:"shotgunner",name:"Shotgunner",lore:"Breaching / CQB",trigger_value:16,main_gun:"spas12",secondary_gun:"m9",main_mag_count:16,secondary_mag_count:2,equip_display:"2x Semtex",perks_display:"Juggernaut, Flak Jacket, Fast Hands",perks:["juggernaut","flak_jacket","quick_swap"],slots:[{slot:"hotbar.1",loot:"mgs:i/spas12",count:1,consumable:0b,bullets:0},{slot:"hotbar.2",loot:"mgs:i/m9",count:1,consumable:0b,bullets:0},{slot:"hotbar.8",loot:"mgs:i/semtex",count:2,consumable:0b,bullets:0},{slot:"inventory.0",loot:"mgs:i/spas12_shell",count:1,consumable:1b,bullets:16},{slot:"inventory.1",loot:"mgs:i/m9_mag",count:1,consumable:0b,bullets:0},{slot:"inventory.2",loot:"mgs:i/m9_mag",count:1,consumable:0b,bullets:0}]},{id:"engineer",name:"Engineer",lore:"Objective / demolitions",trigger_value:17,main_gun:"mp5",secondary_gun:"makarov",main_mag_count:3,secondary_mag_count:2,equip_display:"2x Semtex, 1x Smoke",perks_display:"Flak Jacket, Scavenger, Tactical Mask",perks:["flak_jacket","scavenger","tactical_mask"],slots:[{slot:"hotbar.1",loot:"mgs:i/mp5",count:1,consumable:0b,bullets:0},{slot:"hotbar.2",loot:"mgs:i/makarov",count:1,consumable:0b,bullets:0},{slot:"hotbar.8",loot:"mgs:i/semtex",count:2,consumable:0b,bullets:0},{slot:"hotbar.7",loot:"mgs:i/smoke_grenade",count:1,consumable:0b,bullets:0},{slot:"inventory.0",loot:"mgs:i/mp5_mag",count:1,consumable:0b,bullets:0},{slot:"inventory.1",loot:"mgs:i/mp5_mag",count:1,consumable:0b,bullets:0},{slot:"inventory.2",loot:"mgs:i/mp5_mag",count:1,consumable:0b,bullets:0},{slot:"inventory.3",loot:"mgs:i/makarov_mag",count:1,consumable:0b,bullets:0},{slot:"inventory.4",loot:"mgs:i/makarov_mag",count:1,consumable:0b,bullets:0}]},{id:"medic",name:"Medic",lore:"Team sustain",trigger_value:18,main_gun:"famas",secondary_gun:"m1911",main_mag_count:3,secondary_mag_count:2,equip_display:"2x Smoke",perks_display:"Quick Fix, Tactical Mask, Scavenger",perks:["quick_fix","tactical_mask","scavenger"],slots:[{slot:"hotbar.1",loot:"mgs:i/famas",count:1,consumable:0b,bullets:0},{slot:"hotbar.2",loot:"mgs:i/m1911",count:1,consumable:0b,bullets:0},{slot:"hotbar.8",loot:"mgs:i/smoke_grenade",count:2,consumable:0b,bullets:0},{slot:"inventory.0",loot:"mgs:i/famas_mag",count:1,consumable:0b,bullets:0},{slot:"inventory.1",loot:"mgs:i/famas_mag",count:1,consumable:0b,bullets:0},{slot:"inventory.2",loot:"mgs:i/famas_mag",count:1,consumable:0b,bullets:0},{slot:"inventory.3",loot:"mgs:i/m1911_mag",count:1,consumable:0b,bullets:0},{slot:"inventory.4",loot:"mgs:i/m1911_mag",count:1,consumable:0b,bullets:0}]},{id:"marksman",name:"Marksman",lore:"Semi-auto precision",trigger_value:19,main_gun:"svd",secondary_gun:"glock17",main_mag_count:3,secondary_mag_count:2,equip_display:"1x Flash, 1x Smoke",perks_display:"Sleight of Hand, Tracker, Tactical Mask",perks:["quick_reload","tracker","tactical_mask"],slots:[{slot:"hotbar.1",loot:"mgs:i/svd",count:1,consumable:0b,bullets:0},{slot:"hotbar.2",loot:"mgs:i/glock17",count:1,consumable:0b,bullets:0},{slot:"hotbar.8",loot:"mgs:i/flash_grenade",count:1,consumable:0b,bullets:0},{slot:"hotbar.7",loot:"mgs:i/smoke_grenade",count:1,consumable:0b,bullets:0},{slot:"inventory.0",loot:"mgs:i/svd_mag",count:1,consumable:0b,bullets:0},{slot:"inventory.1",loot:"mgs:i/svd_mag",count:1,consumable:0b,bullets:0},{slot:"inventory.2",loot:"mgs:i/svd_mag",count:1,consumable:0b,bullets:0},{slot:"inventory.3",loot:"mgs:i/glock17_mag",count:1,consumable:0b,bullets:0},{slot:"inventory.4",loot:"mgs:i/glock17_mag",count:1,consumable:0b,bullets:0}]},{id:"heavy",name:"Heavy",lore:"Armored suppressor",trigger_value:20,main_gun:"rpk",secondary_gun:"makarov",main_mag_count:3,secondary_mag_count:2,equip_display:"2x Frag",perks_display:"Juggernaut, Flak Jacket, Scavenger",perks:["juggernaut","flak_jacket","scavenger"],slots:[{slot:"hotbar.1",loot:"mgs:i/rpk",count:1,consumable:0b,bullets:0},{slot:"hotbar.2",loot:"mgs:i/makarov",count:1,consumable:0b,bullets:0},{slot:"hotbar.8",loot:"mgs:i/frag_grenade",count:2,consumable:0b,bullets:0},{slot:"inventory.0",loot:"mgs:i/rpk_mag",count:1,consumable:0b,bullets:0},{slot:"inventory.1",loot:"mgs:i/rpk_mag",count:1,consumable:0b,bullets:0},{slot:"inventory.2",loot:"mgs:i/rpk_mag",count:1,consumable:0b,bullets:0},{slot:"inventory.3",loot:"mgs:i/makarov_mag",count:1,consumable:0b,bullets:0},{slot:"inventory.4",loot:"mgs:i/makarov_mag",count:1,consumable:0b,bullets:0}]}]

# 1-10 standard class, negative custom loadout id, 0 none.
scoreboard objectives add mgs.mp.class dummy

scoreboard objectives add mgs.mp.death_count deathCount

scoreboard objectives add mgs.class_menu minecraft.used:minecraft.warped_fungus_on_a_stick

# mp.pid: unique player id (loadout ownership), #next_pid its counter; mp.default: default custom loadout (0 = standard class).
scoreboard objectives add mgs.mp.pid dummy
execute unless score #next_pid mgs.data matches 1.. run scoreboard players set #next_pid mgs.data 1
scoreboard objectives add mgs.mp.default dummy
# Pick-10 points left while editing.
scoreboard objectives add mgs.mp.edit_points dummy
# 0 creates a new loadout; otherwise saving overwrites this id.
scoreboard objectives add mgs.mp.edit_target dummy

# Custom loadouts are stored as a negative mp.class.
scoreboard players set #minus_one mgs.data -1

# Survives reloads.
execute unless data storage mgs:multiplayer custom_loadouts run data modify storage mgs:multiplayer custom_loadouts set value []
execute unless data storage mgs:multiplayer player_data run data modify storage mgs:multiplayer player_data set value []
execute unless data storage mgs:multiplayer next_loadout_id run data modify storage mgs:multiplayer next_loadout_id set value 1

# Computed at build time.
data modify storage mgs:multiplayer primary_slot_table set value [{id:"ak47",gun_slot:{slot:"hotbar.1",loot:"mgs:i/ak47",count:1,consumable:0b,bullets:0},mag_id:"ak47_mag",mag_consumable:0b,mag_bullets:0},{id:"m16a4",gun_slot:{slot:"hotbar.1",loot:"mgs:i/m16a4",count:1,consumable:0b,bullets:0},mag_id:"m16a4_mag",mag_consumable:0b,mag_bullets:0},{id:"famas",gun_slot:{slot:"hotbar.1",loot:"mgs:i/famas",count:1,consumable:0b,bullets:0},mag_id:"famas_mag",mag_consumable:0b,mag_bullets:0},{id:"aug",gun_slot:{slot:"hotbar.1",loot:"mgs:i/aug",count:1,consumable:0b,bullets:0},mag_id:"aug_mag",mag_consumable:0b,mag_bullets:0},{id:"m4a1",gun_slot:{slot:"hotbar.1",loot:"mgs:i/m4a1",count:1,consumable:0b,bullets:0},mag_id:"m4a1_mag",mag_consumable:0b,mag_bullets:0},{id:"fnfal",gun_slot:{slot:"hotbar.1",loot:"mgs:i/fnfal",count:1,consumable:0b,bullets:0},mag_id:"fnfal_mag",mag_consumable:0b,mag_bullets:0},{id:"g3a3",gun_slot:{slot:"hotbar.1",loot:"mgs:i/g3a3",count:1,consumable:0b,bullets:0},mag_id:"g3a3_mag",mag_consumable:0b,mag_bullets:0},{id:"scar17",gun_slot:{slot:"hotbar.1",loot:"mgs:i/scar17",count:1,consumable:0b,bullets:0},mag_id:"scar17_mag",mag_consumable:0b,mag_bullets:0},{id:"mp5",gun_slot:{slot:"hotbar.1",loot:"mgs:i/mp5",count:1,consumable:0b,bullets:0},mag_id:"mp5_mag",mag_consumable:0b,mag_bullets:0},{id:"mp7",gun_slot:{slot:"hotbar.1",loot:"mgs:i/mp7",count:1,consumable:0b,bullets:0},mag_id:"mp7_mag",mag_consumable:0b,mag_bullets:0},{id:"mac10",gun_slot:{slot:"hotbar.1",loot:"mgs:i/mac10",count:1,consumable:0b,bullets:0},mag_id:"mac10_mag",mag_consumable:0b,mag_bullets:0},{id:"ppsh41",gun_slot:{slot:"hotbar.1",loot:"mgs:i/ppsh41",count:1,consumable:0b,bullets:0},mag_id:"ppsh41_mag",mag_consumable:0b,mag_bullets:0},{id:"sten",gun_slot:{slot:"hotbar.1",loot:"mgs:i/sten",count:1,consumable:0b,bullets:0},mag_id:"sten_mag",mag_consumable:0b,mag_bullets:0},{id:"m249",gun_slot:{slot:"hotbar.1",loot:"mgs:i/m249",count:1,consumable:0b,bullets:0},mag_id:"m249_mag",mag_consumable:0b,mag_bullets:0},{id:"rpk",gun_slot:{slot:"hotbar.1",loot:"mgs:i/rpk",count:1,consumable:0b,bullets:0},mag_id:"rpk_mag",mag_consumable:0b,mag_bullets:0},{id:"svd",gun_slot:{slot:"hotbar.1",loot:"mgs:i/svd",count:1,consumable:0b,bullets:0},mag_id:"svd_mag",mag_consumable:0b,mag_bullets:0},{id:"m82",gun_slot:{slot:"hotbar.1",loot:"mgs:i/m82",count:1,consumable:0b,bullets:0},mag_id:"m82_mag",mag_consumable:0b,mag_bullets:0},{id:"mosin",gun_slot:{slot:"hotbar.1",loot:"mgs:i/mosin",count:1,consumable:0b,bullets:0},mag_id:"mosin_bullet",mag_consumable:1b,mag_bullets:10},{id:"m24",gun_slot:{slot:"hotbar.1",loot:"mgs:i/m24",count:1,consumable:0b,bullets:0},mag_id:"m24_bullet",mag_consumable:1b,mag_bullets:10},{id:"spas12",gun_slot:{slot:"hotbar.1",loot:"mgs:i/spas12",count:1,consumable:0b,bullets:0},mag_id:"spas12_shell",mag_consumable:1b,mag_bullets:16},{id:"m500",gun_slot:{slot:"hotbar.1",loot:"mgs:i/m500",count:1,consumable:0b,bullets:0},mag_id:"m500_shell",mag_consumable:1b,mag_bullets:12},{id:"m590",gun_slot:{slot:"hotbar.1",loot:"mgs:i/m590",count:1,consumable:0b,bullets:0},mag_id:"m590_shell",mag_consumable:1b,mag_bullets:16},{id:"rpg7",gun_slot:{slot:"hotbar.1",loot:"mgs:i/rpg7",count:1,consumable:0b,bullets:0},mag_id:"rpg7_rocket",mag_consumable:1b,mag_bullets:3}]
data modify storage mgs:multiplayer secondary_slot_table set value [{id:"m1911",gun_slot:{slot:"hotbar.2",loot:"mgs:i/m1911",count:1,consumable:0b,bullets:0},mag_id:"m1911_mag",mag_consumable:0b,mag_bullets:0},{id:"m9",gun_slot:{slot:"hotbar.2",loot:"mgs:i/m9",count:1,consumable:0b,bullets:0},mag_id:"m9_mag",mag_consumable:0b,mag_bullets:0},{id:"deagle",gun_slot:{slot:"hotbar.2",loot:"mgs:i/deagle",count:1,consumable:0b,bullets:0},mag_id:"deagle_mag",mag_consumable:0b,mag_bullets:0},{id:"makarov",gun_slot:{slot:"hotbar.2",loot:"mgs:i/makarov",count:1,consumable:0b,bullets:0},mag_id:"makarov_mag",mag_consumable:0b,mag_bullets:0},{id:"glock17",gun_slot:{slot:"hotbar.2",loot:"mgs:i/glock17",count:1,consumable:0b,bullets:0},mag_id:"glock17_mag",mag_consumable:0b,mag_bullets:0},{id:"glock18",gun_slot:{slot:"hotbar.2",loot:"mgs:i/glock18",count:1,consumable:0b,bullets:0},mag_id:"glock18_mag",mag_consumable:0b,mag_bullets:0},{id:"vz61",gun_slot:{slot:"hotbar.2",loot:"mgs:i/vz61",count:1,consumable:0b,bullets:0},mag_id:"vz61_mag",mag_consumable:0b,mag_bullets:0}]

execute unless data storage mgs:maps multiplayer run data modify storage mgs:maps multiplayer set value []
function #mgs:maps/register

scoreboard objectives add mgs.mi.in_game dummy
scoreboard objectives add mgs.mi.kills dummy
scoreboard objectives add mgs.mi.deaths dummy
scoreboard objectives add mgs.mi.kill_total totalKillCount
scoreboard objectives add mgs.mi.kill_base dummy

# 1 when the death was simulated: the body never moved and spectator mode already looks at the spot.
scoreboard objectives add mgs.mi.died_here dummy

# Shares the mp boundary scores.
scoreboard objectives add mgs.mp.bx dummy
scoreboard objectives add mgs.mp.by dummy
scoreboard objectives add mgs.mp.bz dummy

execute unless data storage mgs:missions game run data modify storage mgs:missions game set value {state:"lobby",map_id:""}

scoreboard objectives add mgs.mp.map_edit dummy
scoreboard objectives add mgs.mp.map_idx dummy
scoreboard objectives add mgs.mp.map_mode dummy
scoreboard objectives add mgs.mp.map_disp dummy

# Shared with the class menu.
scoreboard objectives add mgs.class_menu minecraft.used:minecraft.warped_fungus_on_a_stick

execute unless data storage mgs:maps multiplayer run data modify storage mgs:maps multiplayer set value []
execute unless data storage mgs:maps zombies run data modify storage mgs:maps zombies set value []
execute unless data storage mgs:maps missions run data modify storage mgs:maps missions set value []

# Set scoreboard constants for mgs.data
scoreboard players set #1 mgs.data 1
scoreboard players set #2 mgs.data 2
scoreboard players set #3 mgs.data 3
scoreboard players set #4 mgs.data 4
scoreboard players set #5 mgs.data 5
scoreboard players set #6 mgs.data 6
scoreboard players set #10 mgs.data 10
scoreboard players set #14 mgs.data 14
scoreboard players set #15 mgs.data 15
scoreboard players set #20 mgs.data 20
scoreboard players set #40 mgs.data 40
scoreboard players set #44 mgs.data 44
scoreboard players set #45 mgs.data 45
scoreboard players set #50 mgs.data 50
scoreboard players set #60 mgs.data 60
scoreboard players set #90 mgs.data 90
scoreboard players set #100 mgs.data 100
scoreboard players set #200 mgs.data 200
scoreboard players set #1000 mgs.data 1000
scoreboard players set #1011 mgs.data 1011
scoreboard players set #1200 mgs.data 1200
scoreboard players set #3500 mgs.data 3500
scoreboard players set #36000 mgs.data 36000
scoreboard players set #62832 mgs.data 62832
scoreboard players set #1000000 mgs.data 1000000

