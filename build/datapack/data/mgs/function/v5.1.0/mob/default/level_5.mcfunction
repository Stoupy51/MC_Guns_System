
#> mgs:v5.1.0/mob/default/level_5
#
# @within	mgs:mob/default/level_5 {entity:"$(entity)"}
#
# @args		entity (string)
#

$execute summon $(entity) run function mgs:v5.1.0/mob/default/on_new_lv5 {entity:"$(entity)"}

