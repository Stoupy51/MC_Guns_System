
#> mgs:v5.0.0/mob/default/level_2
#
# @within	???
#
# @args		entity (unknown)
#

$execute summon $(entity) run function mgs:v5.0.0/mob/default/on_new {entity:"$(entity)",level:2,active_time:50,sleep_time:50}

