scoreboard players add @s weapon 5
execute store result storage mgs:tmp data int 1 run scoreboard players get @s weapon
item modify entity @s weapon.mainhand mgs:switch_in_out