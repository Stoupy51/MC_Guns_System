
#> mgs:v5.1.0/zombies/wunderfizz/collect
#
# @executed	at @n[tag=bs.interaction.target]
#
# @within	mgs:v5.1.0/zombies/wunderfizz/machine_click
#

scoreboard players operation #wf_pick mgs.data = @n[type=item_display,tag=mgs.wunderfizz_orb,distance=..3] mgs.zb.wf.perk
data remove storage mgs:temp _wf_grant.perk_id
execute if score #wf_pick mgs.data matches 0 run data modify storage mgs:temp _wf_grant.perk_id set value "juggernog"
execute if score #wf_pick mgs.data matches 1 run data modify storage mgs:temp _wf_grant.perk_id set value "speed_cola"
execute if score #wf_pick mgs.data matches 2 run data modify storage mgs:temp _wf_grant.perk_id set value "double_tap"
execute if score #wf_pick mgs.data matches 3 run data modify storage mgs:temp _wf_grant.perk_id set value "quick_revive"
execute if score #wf_pick mgs.data matches 4 run data modify storage mgs:temp _wf_grant.perk_id set value "mule_kick"
execute if score #wf_pick mgs.data matches 5 run data modify storage mgs:temp _wf_grant.perk_id set value "stamin_up"
execute if score #wf_pick mgs.data matches 6 run data modify storage mgs:temp _wf_grant.perk_id set value "phd_flopper"
execute if score #wf_pick mgs.data matches 7 run data modify storage mgs:temp _wf_grant.perk_id set value "deadshot"
execute if score #wf_pick mgs.data matches 8 run data modify storage mgs:temp _wf_grant.perk_id set value "timeslip"
execute if score #wf_pick mgs.data matches 9 run data modify storage mgs:temp _wf_grant.perk_id set value "electric_cherry"
execute if score #wf_pick mgs.data matches 10 run data modify storage mgs:temp _wf_grant.perk_id set value "tombstone"
execute if score #wf_pick mgs.data matches 11 run data modify storage mgs:temp _wf_grant.perk_id set value "whos_who"
execute if score #wf_pick mgs.data matches 12 run data modify storage mgs:temp _wf_grant.perk_id set value "dying_wish"
execute if score #wf_pick mgs.data matches 13 run data modify storage mgs:temp _wf_grant.perk_id set value "widows_wine"
execute if data storage mgs:temp _wf_grant.perk_id run function mgs:v5.1.0/zombies/perks/apply with storage mgs:temp _wf_grant
execute if data storage mgs:temp _wf_grant.perk_id run function #mgs:zombies/on_new_perk
kill @n[type=item_display,tag=mgs.wunderfizz_orb,distance=..3]
playsound minecraft:entity.experience_orb.pickup ambient @s ~ ~ ~ 0.8 1.25

