
#> mgs:v5.1.0/mob/default/level_2
#
# @within	mgs:mob/default/level_2 {entity:"$(entity)"}
#
# @args		entity (string)
#

$execute summon $(entity) run function mgs:v5.1.0/mob/default/on_new {entity:"$(entity)",level:2,active_time:50,sleep_time:50}

