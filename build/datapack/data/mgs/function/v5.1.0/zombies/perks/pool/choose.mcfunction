
#> mgs:v5.1.0/zombies/perks/pool/choose
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/powerups/activate/random_perk
#

function mgs:v5.1.0/zombies/perks/pool/count
scoreboard players set #pool_chosen mgs.data -1
data modify storage mgs:temp _pool set value {}
execute if score #pool_avail mgs.data matches ..0 run return 0

# Random start index, then walk the list until an available perk is found
execute store result score #pool_roll mgs.data run random value 0..8
scoreboard players set #pool_tries mgs.data 0
function mgs:v5.1.0/zombies/perks/pool/choose_iter

