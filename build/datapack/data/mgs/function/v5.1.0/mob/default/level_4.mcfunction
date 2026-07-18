
#> mgs:v5.1.0/mob/default/level_4
#
# @within	mgs:mob/default/level_4 {entity:"$(entity)"}
#
# @args		entity (string)
#

$execute summon $(entity) run function mgs:v5.1.0/mob/default/on_new {entity:"$(entity)",level:4,active_time:72000,sleep_time:1}

