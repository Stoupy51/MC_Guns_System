
#> mgs:v5.1.0/zombies/reset_player
#
# @executed	as @a[scores={mgs.zb.in_game=1}]
#
# @within	mgs:v5.1.0/zombies/stop [ as @a[scores={mgs.zb.in_game=1}] ]
#			mgs:v5.1.0/zombies/clear_stale_player
#

attribute @s minecraft:max_health base reset
attribute @s minecraft:movement_speed base reset
attribute @s minecraft:jump_strength base reset
attribute @s minecraft:entity_interaction_range base reset
effect clear @s
gamemode adventure @s[gamemode=spectator]
function mgs:v5.1.0/shared/maps/call_script_at_base {mode:"zombies",script:"leave"}
function mgs:v5.1.0/lobby/return

scoreboard players set @s mgs.zb.in_game 0
scoreboard players set @s mgs.zb.run 0
scoreboard players set @s mgs.zb.tactical_type 0
# The XP spend tracker is reset too, or the reset reads as points spent (see xp).
scoreboard players set @s mgs.zb.points 0
scoreboard players set @s mgs.zb.xp_pts_prev 0
scoreboard players set @s mgs.zb.xp_spent_acc 0
scoreboard players set @s mgs.zb.kills 0
scoreboard players set @s mgs.zb.downs 0
scoreboard players set @s mgs.zb.passive 0
scoreboard players set @s mgs.zb.ability 0
scoreboard players set @s mgs.zb.ability_cd 0
scoreboard players set @s mgs.zb.prev_kills 0
scoreboard players set @s mgs.mp.spectate_timer 0
tag @s remove mgs.give_class_menu

scoreboard players reset @s mgs.mb.pid

tag @s remove mgs.barricade_repairing
scoreboard players reset @s mgs.zb.barricade_repairs

execute as @s run attribute @s minecraft:max_health base reset
execute as @s run attribute @s minecraft:movement_speed modifier remove mgs:stamin_up
execute as @s run attribute @s minecraft:fall_damage_multiplier base reset
execute as @s run attribute @s minecraft:attack_damage modifier remove mgs:widows_wine
execute as @s run attribute @s minecraft:attack_damage modifier remove mgs:dying_wish
tag @s remove mgs.dying_wish_active
scoreboard players set @s mgs.zb.dw_uses 0
scoreboard players set @s mgs.zb.dw_cd 0
scoreboard players set @s mgs.zb.dw_timer 0
scoreboard players set @s mgs.stam_bonus 0
tag @s remove mgs.perk.speed_cola
tag @s remove mgs.perk.double_tap
tag @s remove mgs.perk.quick_revive
scoreboard players set @s mgs.special.instant_kill 0
scoreboard players set @s mgs.special.infinite_ammo 0
scoreboard players set @s mgs.special.double_points 0
scoreboard players set @s mgs.special.quick_reload 0
scoreboard players set @s mgs.special.quick_swap 0
scoreboard players set @s mgs.special.double_tap 0
scoreboard players set @s mgs.special.phd_flopper 0
scoreboard players set @s mgs.special.deadshot 0
scoreboard players set @s mgs.special.timeslip 0
scoreboard players set @s mgs.special.electric_cherry 0
scoreboard players set @s mgs.special.widows_wine 0
scoreboard players set @s mgs.special.juggernaut 0
scoreboard players set @s mgs.special.scavenger 0
scoreboard players set @s mgs.special.flak_jacket 0
scoreboard players set @s mgs.special.tracker 0
scoreboard players set @s mgs.special.tactical_mask 0
scoreboard players set @s mgs.special.overkill 0
scoreboard players set @s mgs.special.quick_fix 0

tag @s remove mgs.ww_active
scoreboard players set @s mgs.zb.ww.id 0

scoreboard players set @s mgs.zb.downed 0
scoreboard players set @s mgs.zb.bleed 0
scoreboard players set @s mgs.zb.revive_p 0
scoreboard players set @s mgs.zb.qr_uses 0
scoreboard players set @s mgs.zb.downed_id 0
tag @s remove mgs.downed_spectator
tag @s remove mgs.zb_qr_armed

