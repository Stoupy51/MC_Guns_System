scoreboard players set v1 V 0
scoreboard players operation v0 V = @s weapon_id
execute as @e[type=item,scores={weapon_id=1..}] if score @s weapon_id = v0 V store success score v1 V run tag @s add matched
execute if score v1 V matches 1 run function mgs:core/q_reload_helper