
#> mgs:v5.1.0/zombies/stop
#
# @within	mgs:v5.1.0/zombies/game_over 100t [ scheduled ]
#

# Various cleanup to set to lobby state
data modify storage mgs:zombies game.state set value "lobby"
schedule clear mgs:v5.1.0/zombies/end_prep
schedule clear mgs:v5.1.0/zombies/start_round
execute as @a[scores={mgs.zb.in_game=1}] run attribute @s minecraft:max_health base reset
execute as @a[scores={mgs.zb.in_game=1}] run attribute @s minecraft:movement_speed base reset
execute as @a[scores={mgs.zb.in_game=1}] run attribute @s minecraft:jump_strength base reset
execute as @a[scores={mgs.zb.in_game=1}] run attribute @s minecraft:entity_interaction_range base reset
effect clear @a[scores={mgs.zb.in_game=1}]
gamemode adventure @a[scores={mgs.zb.in_game=1},gamemode=spectator]
kill @e[tag=mgs.zombie_round]
kill @e[tag=mgs.gm_entity]

# Remove forceload (only if bounds were set)
execute if score #zb_has_bounds mgs.data matches 1 run function mgs:v5.1.0/shared/remove_forceload

scoreboard objectives setdisplay sidebar
scoreboard objectives remove mgs.zb_sidebar
gamerule advance_time true

# Re-enable natural regeneration, disable custom regen system
gamerule natural_health_regeneration true
scoreboard players set #any_game_active mgs.data 0

# Tear down stamina state: stop any hunger drain and refill the bar so nobody is left winded
effect clear @a minecraft:hunger
effect give @a minecraft:saturation 5 20 true
scoreboard players set @a mgs.stam_out 0
scoreboard players set @a mgs.stam_seen 0

# Announce
tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.zombies_game_ended","color":"red"}]
execute as @a[scores={mgs.zb.in_game=1}] run function mgs:v5.1.0/shared/maps/call_leave_script_at_base

# Reset in-game state
scoreboard players set @a mgs.zb.in_game 0
scoreboard players set @a mgs.zb.points 0
scoreboard players set @a mgs.zb.kills 0
scoreboard players set @a mgs.zb.downs 0
scoreboard players set @a mgs.zb.passive 0
scoreboard players set @a mgs.zb.ability 0
scoreboard players set @a mgs.zb.ability_cd 0
scoreboard players set @a mgs.zb.prev_kills 0
scoreboard players set @a mgs.mp.spectate_timer 0
tag @a[tag=mgs.give_class_menu] remove mgs.give_class_menu

kill @e[type=minecraft:marker,tag=mgs.death_watch]

# Portals are gm_entity so the bulk cleanup already removes them; the counter they feed has to be
# zeroed by hand or a stale value would block the next game's round completion forever.
kill @e[type=minecraft:marker,tag=mgs.dog_portal]
scoreboard players set #zb_dog_pending mgs.data 0

# Escort cleanup (escort.py); the traders themselves die with the mgs.gm_entity kill above
scoreboard players set #zb_escort_count mgs.data 0
gamerule spawn_wandering_traders true
gamerule spawn_mobs true

# Remove all pull displays and presence boxes, reset all per-box state
kill @e[tag=mgs.mb_display]
kill @e[tag=mgs.mb_presence]
kill @e[tag=mgs.mb_temp]
scoreboard players set #mb_pulls mgs.data 0
scoreboard players set #mb_move_timer mgs.data 0
scoreboard players set #mb_fs_cleanup_pending mgs.data 0
scoreboard players reset @a mgs.mb.pid
scoreboard players set #mb_pid_counter mgs.data 0
tag @e remove mgs.mb_fs_active
tag @e remove mgs.mb_orig_active

# Barriers cleanup
tag @e[tag=mgs.barrier_removing] remove mgs.barrier_removing
tag @a[tag=mgs.barrier_repairing] remove mgs.barrier_repairing
scoreboard players reset @a mgs.zb.barrier_repairs

# Power-up cleanup
kill @e[type=minecraft:item,tag=mgs.pu_item]
kill @e[type=minecraft:text_display,tag=mgs.pu_text]
scoreboard players set #pu_active mgs.data 0
scoreboard players set #zb_drops_this_round mgs.data 0
scoreboard players set #zb_cycle_done mgs.data 0
scoreboard players set #zb_cycle_len mgs.data 0
scoreboard players set @a mgs.special.instant_kill 0
scoreboard players set @a mgs.special.double_points 0
scoreboard players set @a mgs.special.infinite_ammo 0
data modify storage mgs:data _pu_queue set value []

# Fire Sale cleanup (reset the global timer + remove its bossbar + stop the song)
scoreboard players set #zb_fire_sale_timer mgs.data 0
scoreboard players set #mb_fs_cleanup_pending mgs.data 0
bossbar remove mgs:pu_fire_sale
stopsound @a ambient mgs:zombies/powerups/fire_sale_song
tag @e remove mgs.mb_fs_active
tag @e remove mgs.mb_orig_active
kill @e[tag=mgs.mb_temp]

# Bonfire Sale cleanup (reset the global timer + remove its bossbar)
scoreboard players set #zb_bonfire_sale_timer mgs.data 0
bossbar remove mgs:pu_bonfire_sale

# Remove all duration-based bossbars
bossbar remove mgs:pu_insta_kill
bossbar remove mgs:pu_double_points
bossbar remove mgs:pu_unlimited_ammo

# Reset perk effects
execute as @a[team=mgs.zombies] run attribute @s minecraft:max_health base reset
execute as @a[team=mgs.zombies] run attribute @s minecraft:movement_speed modifier remove mgs:stamin_up
scoreboard players set @a[team=mgs.zombies] mgs.stam_bonus 0
tag @a[team=mgs.zombies] remove mgs.perk.speed_cola
tag @a[team=mgs.zombies] remove mgs.perk.double_tap
tag @a[team=mgs.zombies] remove mgs.perk.quick_revive
scoreboard players set @a[team=mgs.zombies] mgs.special.instant_kill 0
scoreboard players set @a[team=mgs.zombies] mgs.special.infinite_ammo 0
scoreboard players set @a[team=mgs.zombies] mgs.special.double_points 0
scoreboard players set @a[team=mgs.zombies] mgs.special.quick_reload 0
scoreboard players set @a[team=mgs.zombies] mgs.special.quick_swap 0
scoreboard players set @a[team=mgs.zombies] mgs.special.additional_shots 0
scoreboard players set @a[team=mgs.zombies] mgs.special.juggernaut 0
scoreboard players set @a[team=mgs.zombies] mgs.special.scavenger 0
scoreboard players set @a[team=mgs.zombies] mgs.special.flak_jacket 0
scoreboard players set @a[team=mgs.zombies] mgs.special.tracker 0
scoreboard players set @a[team=mgs.zombies] mgs.special.tactical_mask 0
scoreboard players set @a[team=mgs.zombies] mgs.special.overkill 0
scoreboard players set @a[team=mgs.zombies] mgs.special.quick_fix 0

# Reset perk scoreboards for all known score holders (including offline players).
scoreboard players reset * mgs.zb.perk.juggernog
scoreboard players reset * mgs.zb.perk.speed_cola
scoreboard players reset * mgs.zb.perk.double_tap
scoreboard players reset * mgs.zb.perk.quick_revive
scoreboard players reset * mgs.zb.perk.mule_kick
scoreboard players reset * mgs.zb.perk.stamin_up
scoreboard players reset * mgs.zb.perkpaid.juggernog
scoreboard players reset * mgs.zb.perkpaid.speed_cola
scoreboard players reset * mgs.zb.perkpaid.double_tap
scoreboard players reset * mgs.zb.perkpaid.quick_revive
scoreboard players reset * mgs.zb.perkpaid.mule_kick
scoreboard players reset * mgs.zb.perkpaid.stamin_up

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

