
#> mgs:v5.3.0/mob/default/on_new
#
# @within	mgs:v5.3.0/mob/default/on_new_lv5 {entity:"$(entity)",level:5,active_time:72000,sleep_time:0}
#			mgs:mob/default/level_1 {entity:"$(entity)",level:1,active_time:50,sleep_time:100}
#			mgs:mob/default/level_2 {entity:"$(entity)",level:2,active_time:50,sleep_time:50}
#			mgs:mob/default/level_3 {entity:"$(entity)",level:3,active_time:60,sleep_time:20}
#			mgs:mob/default/level_4 {entity:"$(entity)",level:4,active_time:72000,sleep_time:1}
#
# @args		entity (string)
#			level (int)
#			active_time (int)
#			sleep_time (int)
#

$function mgs:v5.3.0/mob/arm {entity:"$(entity)",level:$(level),active_time:$(active_time),sleep_time:$(sleep_time)}
function mgs:v5.3.0/utils/random_weapon

