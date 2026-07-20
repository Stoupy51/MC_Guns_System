
#> mgs:v5.1.0/zombies/monkey/on_throw
#
# @executed	anchored eyes & positioned ^ ^ ^0.5
#
# @within	mgs:v5.1.0/grenade/init
#

# Tag drives the per-tick attraction hook and lets cleanup find monkey grenades
tag @s add mgs.monkey_bomb

# Wind-up cue (placeholder: the real toy-jingle .ogg is a HUMAN asset, see zombies README task 8)
playsound minecraft:block.note_block.chime ambient @a[distance=..24] ~ ~ ~ 0.8 1.6

# The taunt only exists inside an active zombies game (elsewhere it's just a long-fuse frag)
execute unless data storage mgs:zombies game{state:"active"} run return 0

# Pair ids, then summon the taunt at the grenade (it follows every tick from zombies/monkey/tick)
scoreboard players add #monkey_id_next mgs.data 1
scoreboard players operation @s mgs.monkey_id = #monkey_id_next mgs.data
summon minecraft:iron_golem ~ ~ ~ {Tags:["mgs.monkey_taunt","mgs.monkey_taunt_new","mgs.gm_entity"],NoAI:1b,Silent:1b,Invulnerable:1b,PersistenceRequired:1b,DeathLootTable:"minecraft:empty",Attributes:[{id:"minecraft:scale",base:0.08d}]}
scoreboard players operation @n[tag=mgs.monkey_taunt_new] mgs.monkey_id = @s mgs.monkey_id
tag @n[tag=mgs.monkey_taunt_new] remove mgs.monkey_taunt_new

