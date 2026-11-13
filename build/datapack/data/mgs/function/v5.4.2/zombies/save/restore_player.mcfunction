
#> mgs:v5.4.2/zombies/save/restore_player
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/save/restore [ at @s ]
#

function mgs:v5.4.2/zombies/save/find_player
execute unless data storage mgs:temp _sv_player run return 0

# Their passive is restored, so the Zonweeb pick is not asked again.
dialog clear @s
execute store result score @s mgs.zb.points run data get storage mgs:temp _sv_player.scores.points
execute store result score @s mgs.zb.kills run data get storage mgs:temp _sv_player.scores.kills
execute store result score @s mgs.zb.downs run data get storage mgs:temp _sv_player.scores.downs
execute store result score @s mgs.zb.passive run data get storage mgs:temp _sv_player.scores.passive
execute store result score @s mgs.zb.ability run data get storage mgs:temp _sv_player.scores.ability
execute store result score @s mgs.zb.ability_cd run data get storage mgs:temp _sv_player.scores.ability_cd
execute store result score @s mgs.zb.tactical_type run data get storage mgs:temp _sv_player.scores.tactical_type
execute store result score @s mgs.zb.lethal_type run data get storage mgs:temp _sv_player.scores.lethal_type
execute store result score @s mgs.zb.qr_uses run data get storage mgs:temp _sv_player.scores.qr_uses
execute store result score @s mgs.zb.dw_uses run data get storage mgs:temp _sv_player.scores.dw_uses
execute store result score @s mgs.zb.perk.juggernog run data get storage mgs:temp _sv_player.scores.perk_juggernog
execute store result score @s mgs.zb.perk.speed_cola run data get storage mgs:temp _sv_player.scores.perk_speed_cola
execute store result score @s mgs.zb.perk.double_tap run data get storage mgs:temp _sv_player.scores.perk_double_tap
execute store result score @s mgs.zb.perk.quick_revive run data get storage mgs:temp _sv_player.scores.perk_quick_revive
execute store result score @s mgs.zb.perk.mule_kick run data get storage mgs:temp _sv_player.scores.perk_mule_kick
execute store result score @s mgs.zb.perk.stamin_up run data get storage mgs:temp _sv_player.scores.perk_stamin_up
execute store result score @s mgs.zb.perk.phd_flopper run data get storage mgs:temp _sv_player.scores.perk_phd_flopper
execute store result score @s mgs.zb.perk.deadshot run data get storage mgs:temp _sv_player.scores.perk_deadshot
execute store result score @s mgs.zb.perk.timeslip run data get storage mgs:temp _sv_player.scores.perk_timeslip
execute store result score @s mgs.zb.perk.electric_cherry run data get storage mgs:temp _sv_player.scores.perk_electric_cherry
execute store result score @s mgs.zb.perk.tombstone run data get storage mgs:temp _sv_player.scores.perk_tombstone
execute store result score @s mgs.zb.perk.whos_who run data get storage mgs:temp _sv_player.scores.perk_whos_who
execute store result score @s mgs.zb.perk.dying_wish run data get storage mgs:temp _sv_player.scores.perk_dying_wish
execute store result score @s mgs.zb.perk.widows_wine run data get storage mgs:temp _sv_player.scores.perk_widows_wine
execute store result score @s mgs.zb.perkpaid.juggernog run data get storage mgs:temp _sv_player.scores.perkpaid_juggernog
execute store result score @s mgs.zb.perkpaid.speed_cola run data get storage mgs:temp _sv_player.scores.perkpaid_speed_cola
execute store result score @s mgs.zb.perkpaid.double_tap run data get storage mgs:temp _sv_player.scores.perkpaid_double_tap
execute store result score @s mgs.zb.perkpaid.quick_revive run data get storage mgs:temp _sv_player.scores.perkpaid_quick_revive
execute store result score @s mgs.zb.perkpaid.mule_kick run data get storage mgs:temp _sv_player.scores.perkpaid_mule_kick
execute store result score @s mgs.zb.perkpaid.stamin_up run data get storage mgs:temp _sv_player.scores.perkpaid_stamin_up
execute store result score @s mgs.zb.perkpaid.phd_flopper run data get storage mgs:temp _sv_player.scores.perkpaid_phd_flopper
execute store result score @s mgs.zb.perkpaid.deadshot run data get storage mgs:temp _sv_player.scores.perkpaid_deadshot
execute store result score @s mgs.zb.perkpaid.timeslip run data get storage mgs:temp _sv_player.scores.perkpaid_timeslip
execute store result score @s mgs.zb.perkpaid.electric_cherry run data get storage mgs:temp _sv_player.scores.perkpaid_electric_cherry
execute store result score @s mgs.zb.perkpaid.tombstone run data get storage mgs:temp _sv_player.scores.perkpaid_tombstone
execute store result score @s mgs.zb.perkpaid.whos_who run data get storage mgs:temp _sv_player.scores.perkpaid_whos_who
execute store result score @s mgs.zb.perkpaid.dying_wish run data get storage mgs:temp _sv_player.scores.perkpaid_dying_wish
execute store result score @s mgs.zb.perkpaid.widows_wine run data get storage mgs:temp _sv_player.scores.perkpaid_widows_wine
# Or the XP tracker reads the restored points as earned.
scoreboard players operation @s mgs.zb.xp_pts_prev = @s mgs.zb.points

# Before the inventory, which already holds what some perks give.
execute if score @s mgs.zb.perk.juggernog matches 1 run attribute @s minecraft:max_health base set 40
execute if score @s mgs.zb.perk.speed_cola matches 1 run scoreboard players set @s mgs.special.quick_reload 50
execute if score @s mgs.zb.perk.double_tap matches 1 run scoreboard players set @s mgs.special.double_tap 1
execute if score @s mgs.zb.perk.quick_revive matches 1 run tag @s add mgs.perk.quick_revive
execute if score @s mgs.zb.perk.stamin_up matches 1 run attribute @s minecraft:movement_speed modifier add mgs:stamin_up 0.07 add_multiplied_total
execute if score @s mgs.zb.perk.stamin_up matches 1 run scoreboard players set @s mgs.stam_bonus 300
execute if score @s mgs.zb.perk.stamin_up matches 1 run scoreboard players add @s mgs.stam 300
execute if score @s mgs.zb.perk.phd_flopper matches 1 run attribute @s minecraft:fall_damage_multiplier base set 0
execute if score @s mgs.zb.perk.phd_flopper matches 1 run scoreboard players set @s mgs.special.phd_flopper 1
execute if score @s mgs.zb.perk.deadshot matches 1 run scoreboard players set @s mgs.special.deadshot 1
execute if score @s mgs.zb.perk.timeslip matches 1 run scoreboard players set @s mgs.special.timeslip 1
execute if score @s mgs.zb.perk.electric_cherry matches 1 run scoreboard players set @s mgs.special.electric_cherry 1
execute if score @s mgs.zb.perk.widows_wine matches 1 run scoreboard players set @s mgs.special.widows_wine 1
execute if score @s mgs.zb.perk.widows_wine matches 1 run attribute @s minecraft:attack_damage modifier add mgs:widows_wine 6 add_value
execute if score @s mgs.zb.perk.widows_wine matches 1 run function mgs:v5.4.2/zombies/inventory/loot_replace_lethal
execute if score @s mgs.zb.perk.widows_wine matches 1 run item modify entity @s hotbar.7 mgs:v5.4.2/grenade/set_count_2
execute if score @s mgs.zb.perk.widows_wine matches 1 run function mgs:v5.4.2/zombies/inventory/apply_slot_tag {slot:"hotbar.7",group:"hotbar",index:7}

function mgs:v5.4.2/zombies/save/rebuild_weapons
data modify storage mgs:temp _restore.items set from storage mgs:temp _sv_items
data remove storage mgs:temp _sv_items
function mgs:v5.4.2/zombies/inventory/restore_inventory
# The held gun's ammo moves to the score on the next weapon switch check.
scoreboard players set @s mgs.last_selected 0
function mgs:v5.4.2/zombies/inventory/refresh_perk_items
data remove storage mgs:temp _sv_player

