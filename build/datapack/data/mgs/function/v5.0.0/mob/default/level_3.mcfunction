
#> mgs:v5.0.0/mob/default/level_3
#
# @within	???
#
# @args		entity (unknown)
#

$execute summon $(entity) run function mgs:v5.0.0/mob/default/on_new {entity:"$(entity)",level:3,active_time:60,sleep_time:20}

