
#> mgs:v5.1.0/zombies/wunderfizz/grant/speed_cola
#
# @executed	at @n[tag=bs.interaction.target]
#
# @within	mgs:v5.1.0/zombies/wunderfizz/collect
#

data modify storage mgs:temp _wf_grant.perk_id set value "speed_cola"
function mgs:v5.1.0/zombies/perks/apply with storage mgs:temp _wf_grant
function #mgs:zombies/on_new_perk

