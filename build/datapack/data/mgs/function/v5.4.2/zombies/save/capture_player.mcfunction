
#> mgs:v5.4.2/zombies/save/capture_player
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/save/save [ as @a[scores={mgs.zb.in_game=1}] ]
#

function mgs:v5.4.2/ammo/update_old_weapon

data modify storage mgs:zombies_saves _slot.players append value {scores:{}}
data modify storage mgs:zombies_saves _slot.players[-1].uuid set from entity @s UUID
data modify storage mgs:zombies_saves _slot.players[-1].inventory set from entity @s Inventory
execute store result storage mgs:zombies_saves _slot.players[-1].scores.points int 1 run scoreboard players get @s mgs.zb.points
execute store result storage mgs:zombies_saves _slot.players[-1].scores.kills int 1 run scoreboard players get @s mgs.zb.kills
execute store result storage mgs:zombies_saves _slot.players[-1].scores.downs int 1 run scoreboard players get @s mgs.zb.downs
execute store result storage mgs:zombies_saves _slot.players[-1].scores.passive int 1 run scoreboard players get @s mgs.zb.passive
execute store result storage mgs:zombies_saves _slot.players[-1].scores.ability int 1 run scoreboard players get @s mgs.zb.ability
execute store result storage mgs:zombies_saves _slot.players[-1].scores.ability_cd int 1 run scoreboard players get @s mgs.zb.ability_cd
execute store result storage mgs:zombies_saves _slot.players[-1].scores.tactical_type int 1 run scoreboard players get @s mgs.zb.tactical_type
execute store result storage mgs:zombies_saves _slot.players[-1].scores.lethal_type int 1 run scoreboard players get @s mgs.zb.lethal_type
execute store result storage mgs:zombies_saves _slot.players[-1].scores.qr_uses int 1 run scoreboard players get @s mgs.zb.qr_uses
execute store result storage mgs:zombies_saves _slot.players[-1].scores.dw_uses int 1 run scoreboard players get @s mgs.zb.dw_uses
execute store result storage mgs:zombies_saves _slot.players[-1].scores.perk_juggernog int 1 run scoreboard players get @s mgs.zb.perk.juggernog
execute store result storage mgs:zombies_saves _slot.players[-1].scores.perk_speed_cola int 1 run scoreboard players get @s mgs.zb.perk.speed_cola
execute store result storage mgs:zombies_saves _slot.players[-1].scores.perk_double_tap int 1 run scoreboard players get @s mgs.zb.perk.double_tap
execute store result storage mgs:zombies_saves _slot.players[-1].scores.perk_quick_revive int 1 run scoreboard players get @s mgs.zb.perk.quick_revive
execute store result storage mgs:zombies_saves _slot.players[-1].scores.perk_mule_kick int 1 run scoreboard players get @s mgs.zb.perk.mule_kick
execute store result storage mgs:zombies_saves _slot.players[-1].scores.perk_stamin_up int 1 run scoreboard players get @s mgs.zb.perk.stamin_up
execute store result storage mgs:zombies_saves _slot.players[-1].scores.perk_phd_flopper int 1 run scoreboard players get @s mgs.zb.perk.phd_flopper
execute store result storage mgs:zombies_saves _slot.players[-1].scores.perk_deadshot int 1 run scoreboard players get @s mgs.zb.perk.deadshot
execute store result storage mgs:zombies_saves _slot.players[-1].scores.perk_timeslip int 1 run scoreboard players get @s mgs.zb.perk.timeslip
execute store result storage mgs:zombies_saves _slot.players[-1].scores.perk_electric_cherry int 1 run scoreboard players get @s mgs.zb.perk.electric_cherry
execute store result storage mgs:zombies_saves _slot.players[-1].scores.perk_tombstone int 1 run scoreboard players get @s mgs.zb.perk.tombstone
execute store result storage mgs:zombies_saves _slot.players[-1].scores.perk_whos_who int 1 run scoreboard players get @s mgs.zb.perk.whos_who
execute store result storage mgs:zombies_saves _slot.players[-1].scores.perk_dying_wish int 1 run scoreboard players get @s mgs.zb.perk.dying_wish
execute store result storage mgs:zombies_saves _slot.players[-1].scores.perk_widows_wine int 1 run scoreboard players get @s mgs.zb.perk.widows_wine
execute store result storage mgs:zombies_saves _slot.players[-1].scores.perkpaid_juggernog int 1 run scoreboard players get @s mgs.zb.perkpaid.juggernog
execute store result storage mgs:zombies_saves _slot.players[-1].scores.perkpaid_speed_cola int 1 run scoreboard players get @s mgs.zb.perkpaid.speed_cola
execute store result storage mgs:zombies_saves _slot.players[-1].scores.perkpaid_double_tap int 1 run scoreboard players get @s mgs.zb.perkpaid.double_tap
execute store result storage mgs:zombies_saves _slot.players[-1].scores.perkpaid_quick_revive int 1 run scoreboard players get @s mgs.zb.perkpaid.quick_revive
execute store result storage mgs:zombies_saves _slot.players[-1].scores.perkpaid_mule_kick int 1 run scoreboard players get @s mgs.zb.perkpaid.mule_kick
execute store result storage mgs:zombies_saves _slot.players[-1].scores.perkpaid_stamin_up int 1 run scoreboard players get @s mgs.zb.perkpaid.stamin_up
execute store result storage mgs:zombies_saves _slot.players[-1].scores.perkpaid_phd_flopper int 1 run scoreboard players get @s mgs.zb.perkpaid.phd_flopper
execute store result storage mgs:zombies_saves _slot.players[-1].scores.perkpaid_deadshot int 1 run scoreboard players get @s mgs.zb.perkpaid.deadshot
execute store result storage mgs:zombies_saves _slot.players[-1].scores.perkpaid_timeslip int 1 run scoreboard players get @s mgs.zb.perkpaid.timeslip
execute store result storage mgs:zombies_saves _slot.players[-1].scores.perkpaid_electric_cherry int 1 run scoreboard players get @s mgs.zb.perkpaid.electric_cherry
execute store result storage mgs:zombies_saves _slot.players[-1].scores.perkpaid_tombstone int 1 run scoreboard players get @s mgs.zb.perkpaid.tombstone
execute store result storage mgs:zombies_saves _slot.players[-1].scores.perkpaid_whos_who int 1 run scoreboard players get @s mgs.zb.perkpaid.whos_who
execute store result storage mgs:zombies_saves _slot.players[-1].scores.perkpaid_dying_wish int 1 run scoreboard players get @s mgs.zb.perkpaid.dying_wish
execute store result storage mgs:zombies_saves _slot.players[-1].scores.perkpaid_widows_wine int 1 run scoreboard players get @s mgs.zb.perkpaid.widows_wine

