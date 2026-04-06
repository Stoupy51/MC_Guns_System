
#> mgs:v5.0.0/zombies/mystery_box/cycle_step
#
# @within	mgs:v5.0.0/zombies/mystery_box/spin_tick
#

# elapsed = 80 - timer
scoreboard players set #mb_elapsed mgs.data 80
scoreboard players operation #mb_elapsed mgs.data -= #mb_anim_timer mgs.data

# Constants for modulo cadence checks
scoreboard players set #mb_c2 mgs.data 2
scoreboard players set #mb_c5 mgs.data 5
scoreboard players set #mb_c8 mgs.data 8

# 0..29 ticks elapsed: every 2 ticks
scoreboard players operation #mb_mod mgs.data = #mb_elapsed mgs.data
execute if score #mb_elapsed mgs.data matches ..29 run scoreboard players operation #mb_mod mgs.data %= #mb_c2 mgs.data
execute if score #mb_elapsed mgs.data matches ..29 if score #mb_mod mgs.data matches 0 run function mgs:v5.0.0/zombies/mystery_box/cycle_display

# 30..49 ticks elapsed: every 5 ticks
scoreboard players operation #mb_mod mgs.data = #mb_elapsed mgs.data
execute if score #mb_elapsed mgs.data matches 30..49 run scoreboard players operation #mb_mod mgs.data %= #mb_c5 mgs.data
execute if score #mb_elapsed mgs.data matches 30..49 if score #mb_mod mgs.data matches 0 run function mgs:v5.0.0/zombies/mystery_box/cycle_display

# 50+ ticks elapsed: every 8 ticks
scoreboard players operation #mb_mod mgs.data = #mb_elapsed mgs.data
execute if score #mb_elapsed mgs.data matches 50.. run scoreboard players operation #mb_mod mgs.data %= #mb_c8 mgs.data
execute if score #mb_elapsed mgs.data matches 50.. if score #mb_mod mgs.data matches 0 run function mgs:v5.0.0/zombies/mystery_box/cycle_display

