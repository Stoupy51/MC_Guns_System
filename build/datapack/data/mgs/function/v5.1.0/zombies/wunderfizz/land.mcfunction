
#> mgs:v5.1.0/zombies/wunderfizz/land
#
# @executed	as @e[type=item_display,tag=mgs.wunderfizz_orb] & at @s
#
# @within	mgs:v5.1.0/zombies/wunderfizz/orb_tick
#

# Roam pull: the machine is about to move — show the bear, refund the buyer, no perk
execute if score @s mgs.zb.wf.willmove matches 1 run return run function mgs:v5.1.0/zombies/wunderfizz/land_bear

execute if score @s mgs.zb.wf.perk matches 0 run function mgs:v5.1.0/zombies/wunderfizz/set_model/juggernog
execute if score @s mgs.zb.wf.perk matches 1 run function mgs:v5.1.0/zombies/wunderfizz/set_model/speed_cola
execute if score @s mgs.zb.wf.perk matches 2 run function mgs:v5.1.0/zombies/wunderfizz/set_model/double_tap
execute if score @s mgs.zb.wf.perk matches 3 run function mgs:v5.1.0/zombies/wunderfizz/set_model/quick_revive
execute if score @s mgs.zb.wf.perk matches 4 run function mgs:v5.1.0/zombies/wunderfizz/set_model/mule_kick
execute if score @s mgs.zb.wf.perk matches 5 run function mgs:v5.1.0/zombies/wunderfizz/set_model/stamin_up
execute if score @s mgs.zb.wf.perk matches 6 run function mgs:v5.1.0/zombies/wunderfizz/set_model/phd_flopper
execute if score @s mgs.zb.wf.perk matches 7 run function mgs:v5.1.0/zombies/wunderfizz/set_model/deadshot
execute if score @s mgs.zb.wf.perk matches 8 run function mgs:v5.1.0/zombies/wunderfizz/set_model/timeslip
execute if score @s mgs.zb.wf.perk matches 9 run function mgs:v5.1.0/zombies/wunderfizz/set_model/electric_cherry
execute if score @s mgs.zb.wf.perk matches 10 run function mgs:v5.1.0/zombies/wunderfizz/set_model/tombstone
execute if score @s mgs.zb.wf.perk matches 11 run function mgs:v5.1.0/zombies/wunderfizz/set_model/whos_who
execute if score @s mgs.zb.wf.perk matches 12 run function mgs:v5.1.0/zombies/wunderfizz/set_model/dying_wish
execute if score @s mgs.zb.wf.perk matches 13 run function mgs:v5.1.0/zombies/wunderfizz/set_model/widows_wine
particle minecraft:totem_of_undying ~ ~ ~ 0.3 0.4 0.3 0.2 10 force @a[distance=..48]
particle minecraft:electric_spark ~ ~ ~ 0.4 0.5 0.4 0.15 10 force @a[distance=..48]
playsound minecraft:block.beacon.deactivate ambient @a[scores={mgs.zb.in_game=1}] ~ ~ ~ 0.8 1.4
playsound minecraft:entity.lightning_bolt.impact ambient @a[scores={mgs.zb.in_game=1}] ~ ~ ~ 0.5 1.7
function mgs:v5.1.0/zombies/feedback/sound_announce
scoreboard players operation #wf_b mgs.data = @s mgs.zb.wf.buyer
execute as @a[scores={mgs.zb.in_game=1}] if score @s mgs.zb.wf_pid = #wf_b mgs.data run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.perk_ready","color":"gold"},{"translate":"mgs.right_click_der_wunderfizz_to_collect","color":"green","bold":true}]

