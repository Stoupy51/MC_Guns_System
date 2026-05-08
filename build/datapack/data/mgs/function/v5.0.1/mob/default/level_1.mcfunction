
#> mgs:v5.0.1/mob/default/level_1
#
# @within	???
#
# @args		entity (unknown)
#

$execute summon $(entity) run function mgs:v5.0.1/mob/default/on_new {entity:"$(entity)",level:1,active_time:50,sleep_time:100}

