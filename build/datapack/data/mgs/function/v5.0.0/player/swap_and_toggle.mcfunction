
#> mgs:v5.0.0/player/swap_and_toggle
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/mode_check
#

# Move offhand item to mainhand
item replace entity @s weapon.mainhand from entity @s weapon.offhand
item replace entity @s weapon.offhand with air

# Toggle fire mode for the swapped weapon (storage-level)
function mgs:v5.0.0/switch/do_toggle_fire_mode

