
#> mgs:v5.1.0/mob/default/level_3
#
# @within	mgs:mob/default/level_3 {entity:"$(entity)"}
#
# @args		entity (string)
#

$execute summon $(entity) run function mgs:v5.1.0/mob/default/on_new {entity:"$(entity)",level:3,active_time:60,sleep_time:20}

