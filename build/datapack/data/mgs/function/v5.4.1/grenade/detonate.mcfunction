
#> mgs:v5.4.1/grenade/detonate
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/grenade/tick
#			mgs:v5.4.1/grenade/move_semtex
#			mgs:v5.4.1/grenade/on_stick
#			mgs:v5.4.1/grenade/tick_stuck
#

execute if data entity @s data.config{grenade_type:"frag"} run return run function mgs:v5.4.1/grenade/detonate_frag
execute if data entity @s data.config{grenade_type:"semtex"} run return run function mgs:v5.4.1/grenade/detonate_frag
execute if data entity @s data.config{grenade_type:"monkey_bomb"} run return run function mgs:v5.4.1/grenade/detonate_frag
execute if data entity @s data.config{grenade_type:"smoke"} run return run function mgs:v5.4.1/grenade/detonate_smoke
execute if data entity @s data.config{grenade_type:"flash"} run return run function mgs:v5.4.1/grenade/detonate_flash
execute if data entity @s data.config{grenade_type:"web"} run return run function mgs:v5.4.1/grenade/detonate_web

