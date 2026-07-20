
#> mgs:v5.1.0/zombies/monkey/detonate
#
# @executed	as @e[tag=mgs.grenade] & at @s
#
# @within	mgs:v5.1.0/grenade/detonate
#

scoreboard players operation #monkey_cur_id mgs.data = @s mgs.monkey_id
execute as @e[tag=mgs.monkey_taunt] if score @s mgs.monkey_id = #monkey_cur_id mgs.data run kill @s
function mgs:v5.1.0/grenade/detonate_frag

