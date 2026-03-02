
#> mgs:v5.0.0/grenade/detonate
#
# @executed	as @e[tag=mgs.grenade] & at @s
#
# @within	mgs:v5.0.0/grenade/tick
#			mgs:v5.0.0/grenade/move_semtex
#			mgs:v5.0.0/grenade/tick_stuck
#

# Route to the appropriate detonation effect based on grenade type
execute if data entity @s data.config{grenade_type:"frag"} run return run function mgs:v5.0.0/grenade/detonate_frag
execute if data entity @s data.config{grenade_type:"semtex"} run return run function mgs:v5.0.0/grenade/detonate_frag
execute if data entity @s data.config{grenade_type:"smoke"} run return run function mgs:v5.0.0/grenade/detonate_smoke
execute if data entity @s data.config{grenade_type:"flash"} run return run function mgs:v5.0.0/grenade/detonate_flash

