
#> mgs:v5.1.0/zombies/wunderfizz/land_bear
#
# @executed	as @e[type=item_display,tag=mgs.wunderfizz_orb] & at @s
#
# @within	mgs:v5.1.0/zombies/wunderfizz/land
#

# Refund the buyer (the machine roams away instead of granting a perk — Black Ops teddy-bear rule)
scoreboard players operation #wf_b mgs.data = @s mgs.zb.wf.buyer
scoreboard players operation #wf_refund mgs.data = @s mgs.zb.wf.paid
execute as @a[scores={mgs.zb.in_game=1}] if score @s mgs.zb.wf_pid = #wf_b mgs.data run scoreboard players operation @s mgs.zb.points += #wf_refund mgs.data

tellraw @a[scores={mgs.zb.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.der_wunderfizz_is_moving_2","color":"yellow","bold":true}]
execute as @a[scores={mgs.zb.in_game=1}] at @s run playsound mgs:zombies/mystery_box/bye_bye ambient @s ~ ~ ~ 1.0 1.0

# Spawn the teddy bear at the active machine and start the roam timer, then remove the orb
execute as @n[tag=mgs.wf_active] at @s run function mgs:v5.1.0/zombies/wunderfizz/move_start
kill @s

