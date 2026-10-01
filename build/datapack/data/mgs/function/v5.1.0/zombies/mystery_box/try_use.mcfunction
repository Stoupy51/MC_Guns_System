
#> mgs:v5.1.0/zombies/mystery_box/try_use
#
# @executed	at @n[tag=bs.interaction.target]
#
# @within	mgs:v5.1.0/zombies/mystery_box/box_click
#

execute unless score @s mgs.zb.points >= #zb_mystery_box_price mgs.config run return run function mgs:v5.1.0/zombies/deny/not_enough_points {score:"#zb_mystery_box_price",obj:"mgs.config"}

function mgs:v5.1.0/zombies/mystery_box/ensure_default_pool

# A stable player id lets the display record its buyer, so one player can run several pulls at once.
scoreboard players operation @s mgs.zb.points -= #zb_mystery_box_price mgs.config
execute unless score @s mgs.mb.pid matches 1.. run function mgs:v5.1.0/zombies/mystery_box/assign_pid

# Decided now: after N uses, a 1 in 3 chance (shared with Der Wunderfizz, roaming/roll_move).
scoreboard players add #mb_pulls mgs.data 1
scoreboard players operation #roam_uses mgs.data = #mb_pulls mgs.data
scoreboard players set #roam_threshold mgs.data 4
function mgs:v5.1.0/zombies/roaming/roll_move
scoreboard players operation #mb_will_move mgs.data = #roam_will_move mgs.data
# Only the active box moves, never during a Fire Sale.
execute unless entity @n[tag=bs.interaction.target,tag=mgs.mystery_box_active] run scoreboard players set #mb_will_move mgs.data 0
execute if score #zb_fire_sale_timer mgs.data matches 1.. run scoreboard players set #mb_will_move mgs.data 0
execute if score #mb_will_move mgs.data matches 1 run scoreboard players set #mb_pulls mgs.data 0

function mgs:v5.1.0/zombies/mystery_box/spawn_display
scoreboard players operation @n[tag=mgs.mb_display_new] mgs.mb.box = #cur_box mgs.data
scoreboard players set @n[tag=mgs.mb_display_new] mgs.mb.anim 105
scoreboard players operation @n[tag=mgs.mb_display_new] mgs.mb.willmove = #mb_will_move mgs.data
scoreboard players operation @n[tag=mgs.mb_display_new] mgs.mb.buyer = @s mgs.mb.pid

# Timeslip: 2x spin.
scoreboard players set @n[tag=mgs.mb_display_new] mgs.mb.timeslip 0
execute if score @s mgs.special.timeslip matches 1.. run scoreboard players set @n[tag=mgs.mb_display_new] mgs.mb.timeslip 1

tag @n[tag=mgs.mb_display_new] remove mgs.mb_display_new

# Lid, open and spin sounds, and a private announce to the buyer.
function mgs:v5.1.0/zombies/mystery_box/open_lid
playsound mgs:zombies/mystery_box/open ambient @a[scores={mgs.zb.in_game=1}] ~ ~ ~ 1.0 1.0
# Timeslip owners hear the sped-up tune.
execute unless score @s mgs.special.timeslip matches 1.. run playsound mgs:zombies/mystery_box/box_spin ambient @a[scores={mgs.zb.in_game=1}] ~ ~ ~ 0.1 1.0
execute unless score @s mgs.special.timeslip matches 1.. run playsound mgs:zombies/mystery_box/music_box ambient @a[scores={mgs.zb.in_game=1}] ~ ~ ~ 1.0 1.0
execute if score @s mgs.special.timeslip matches 1.. run playsound mgs:zombies/mystery_box/box_spin ambient @a[scores={mgs.zb.in_game=1}] ~ ~ ~ 0.1 1.0
execute if score @s mgs.special.timeslip matches 1.. run playsound mgs:zombies/mystery_box/music_box_short ambient @a[scores={mgs.zb.in_game=1}] ~ ~ ~ 1.0 1.0
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.mystery_box_spinning","color":"light_purple"}]

