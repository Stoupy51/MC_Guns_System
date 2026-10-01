
#> mgs:v5.1.0/zombies/powerups/do_pickup
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/powerups/entity_tick
#

# Free PaP upgrades the gun in hotbar 1-3, so a player without one cannot use it: the drop stays for a teammate.
scoreboard players set #pu_pap_ok mgs.data 0
execute if score @s mgs.zb.pu.type matches 8 as @p[scores={mgs.zb.in_game=1},gamemode=!spectator,distance=..1.5] run function mgs:v5.1.0/zombies/powerups/check_pap_taker
execute if score @s mgs.zb.pu.type matches 8 if score #pu_pap_ok mgs.data matches 0 run return fail

# The nearest eligible player collects.
tag @p[scores={mgs.zb.in_game=1},gamemode=!spectator,distance=..1.5,tag=!mgs.pu_collecting] add mgs.pu_collecting

# Nobody alive took it: a downed player crawled their mannequin over it.
execute unless entity @a[tag=mgs.pu_collecting] if entity @e[type=minecraft:mannequin,tag=mgs.downed_mannequin,distance=..1.5] run function mgs:v5.1.0/zombies/powerups/pickup_downed_collector

scoreboard players operation #pu_type_pickup mgs.data = @s mgs.zb.pu.type

# First, while the position is still valid.
kill @n[type=minecraft:text_display,tag=mgs.pu_text,distance=..3]

execute as @a[scores={mgs.zb.in_game=1}] at @s run playsound mgs:zombies/powerups/item/grab ambient @s ~ ~ ~ 0.4 1.0

# The collector tag is still set here.
function mgs:v5.1.0/zombies/powerups/dispatch_activate

# Silent award: eleven types with eleven announces, so no single message to suffix.
execute as @a[tag=mgs.pu_collecting] run function mgs:v5.1.0/progression/zb/award_powerup

kill @s
scoreboard players remove #pu_active mgs.data 1

tag @a[tag=mgs.pu_collecting] remove mgs.pu_collecting

