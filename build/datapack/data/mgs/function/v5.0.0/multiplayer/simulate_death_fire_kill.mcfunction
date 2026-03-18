
#> mgs:v5.0.0/multiplayer/simulate_death_fire_kill
#
# @executed	at @s
#
# @within	mgs:v5.0.0/multiplayer/simulate_death with storage mgs:input with
#
# @args		attacker (unknown)
#

$tag $(attacker) add mgs.temp_killer

# Self-kill check: if victim(@s) is also tagged as killer, it's self-damage
execute if entity @s[tag=mgs.temp_killer] run tag @s remove mgs.temp_killer
execute unless entity @a[tag=mgs.temp_killer] run return run function mgs:v5.0.0/multiplayer/random_self_kill_message

# Normal kill: fire signal and show message
tag @s add mgs.temp_victim
$execute as $(attacker) run function #mgs:signals/on_kill
function mgs:v5.0.0/multiplayer/random_kill_message
tag @s remove mgs.temp_victim

