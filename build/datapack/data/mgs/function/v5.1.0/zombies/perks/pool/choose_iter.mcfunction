
#> mgs:v5.1.0/zombies/perks/pool/choose_iter
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/perks/pool/choose
#			mgs:v5.1.0/zombies/perks/pool/choose_iter
#

# Safety counter: at most one full loop over the perk list
scoreboard players add #pool_tries mgs.data 1
execute if score #pool_tries mgs.data matches 10.. run return 0
execute if score #pool_chosen mgs.data matches 0.. run return 0

execute if score #pool_roll mgs.data matches 0 run function mgs:v5.1.0/zombies/perks/pool/try_index/juggernog
execute if score #pool_chosen mgs.data matches 0.. run return 0
execute if score #pool_roll mgs.data matches 1 run function mgs:v5.1.0/zombies/perks/pool/try_index/speed_cola
execute if score #pool_chosen mgs.data matches 0.. run return 0
execute if score #pool_roll mgs.data matches 2 run function mgs:v5.1.0/zombies/perks/pool/try_index/double_tap
execute if score #pool_chosen mgs.data matches 0.. run return 0
execute if score #pool_roll mgs.data matches 3 run function mgs:v5.1.0/zombies/perks/pool/try_index/quick_revive
execute if score #pool_chosen mgs.data matches 0.. run return 0
execute if score #pool_roll mgs.data matches 4 run function mgs:v5.1.0/zombies/perks/pool/try_index/mule_kick
execute if score #pool_chosen mgs.data matches 0.. run return 0
execute if score #pool_roll mgs.data matches 5 run function mgs:v5.1.0/zombies/perks/pool/try_index/stamin_up
execute if score #pool_chosen mgs.data matches 0.. run return 0
execute if score #pool_roll mgs.data matches 6 run function mgs:v5.1.0/zombies/perks/pool/try_index/phd_flopper
execute if score #pool_chosen mgs.data matches 0.. run return 0
execute if score #pool_roll mgs.data matches 7 run function mgs:v5.1.0/zombies/perks/pool/try_index/deadshot
execute if score #pool_chosen mgs.data matches 0.. run return 0
execute if score #pool_roll mgs.data matches 8 run function mgs:v5.1.0/zombies/perks/pool/try_index/timeslip
execute if score #pool_chosen mgs.data matches 0.. run return 0

# Nothing available at this index: advance and recurse
scoreboard players add #pool_roll mgs.data 1
execute if score #pool_roll mgs.data matches 9.. run scoreboard players set #pool_roll mgs.data 0
function mgs:v5.1.0/zombies/perks/pool/choose_iter

