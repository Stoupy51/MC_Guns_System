
#> mgs:v5.1.0/player/hurt_tick
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/player/tick
#

scoreboard players set #hurt_tier mgs.data 0
execute unless entity @s[gamemode=spectator] if score @s mgs.mp.in_game matches 1 run function mgs:v5.1.0/player/hurt_resolve
execute unless entity @s[gamemode=spectator] if score @s mgs.mi.in_game matches 1 run function mgs:v5.1.0/player/hurt_resolve
execute unless entity @s[gamemode=spectator] if score @s mgs.zb.in_game matches 1 run function mgs:v5.1.0/player/hurt_resolve
execute unless score @s mgs.hurt_fx matches -2147483648.. run scoreboard players set @s mgs.hurt_fx 0
# No overlay and no fade playing: every 2 s, take off any hurt id the scores missed, so a desync can never leave the screen red.
execute if score @s mgs.hurt_fx matches 0 if score #hurt_tier mgs.data matches 0 unless score @s mgs.hurt_out_until matches -2147483648.. if score #fx_sweep mgs.data matches 0 run function mgs:v5.1.0/player/hurt_sweep
execute if score @s mgs.hurt_fx = #hurt_tier mgs.data run return run scoreboard players reset @s mgs.hurt_pending
execute if score #hurt_tier mgs.data > @s mgs.hurt_fx run return run function mgs:v5.1.0/player/hurt_swap

# Healing: wait for the bar to settle, so crossing several thresholds becomes a single fade.
# A fade still playing finishes first: the next id starts from its end look, so starting early would jump.
scoreboard players add @s mgs.hurt_pending 1
execute if score @s mgs.hurt_pending matches 10.. unless score @s mgs.hurt_fall_until > #total_tick mgs.data run function mgs:v5.1.0/player/hurt_swap

