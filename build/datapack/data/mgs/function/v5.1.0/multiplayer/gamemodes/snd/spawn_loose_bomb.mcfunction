
#> mgs:v5.1.0/multiplayer/gamemodes/snd/spawn_loose_bomb
#
# @executed	at @e[tag=mgs.spawn_red,limit=1]
#
# @within	mgs:v5.1.0/multiplayer/gamemodes/snd/start_round [ at @e[tag=mgs.spawn_red,limit=1] ]
#			mgs:v5.1.0/multiplayer/gamemodes/snd/start_round [ at @e[tag=mgs.spawn_blue,limit=1] ]
#			mgs:v5.1.0/multiplayer/gamemodes/snd/start_round [ at @e[tag=mgs.spawn_point,limit=1] ]
#			mgs:v5.1.0/multiplayer/gamemodes/snd/drop_bomb [ at @e[tag=mgs.snd_carrier_label,limit=1] ]
#

data modify storage mgs:input with set value {}
data modify storage mgs:input with.blocks set value "function #bs.hitbox:callback/get_block_shape_with_fluid"
data modify storage mgs:input with.piercing set value 0
data modify storage mgs:input with.max_distance set value 100
data modify storage mgs:input with.ignored_blocks set value "#mgs:v5.1.0/empty"
data modify storage mgs:input with.on_entry_point set value "function mgs:v5.1.0/multiplayer/gamemodes/snd/place_loose_bomb"
scoreboard players set #snd_bomb_grounded mgs.data 0
execute rotated ~ 90 run function #bs.raycast:run with storage mgs:input

# Dropped over the void: leave it where it fell rather than lose it entirely
execute if score #snd_bomb_grounded mgs.data matches 0 run function mgs:v5.1.0/multiplayer/gamemodes/snd/place_loose_bomb

