
#> mgs:v5.1.0/mob/default/level_1
#
# @within	mgs:mob/default/level_1 {entity:"$(entity)"}
#
# @args		entity (string)
#

$execute summon $(entity) run function mgs:v5.1.0/mob/default/on_new {entity:"$(entity)",level:1,active_time:50,sleep_time:100}

