scoreboard players set @s fire 0
scoreboard players set @s selector 0
tag @s[scores={cooldown=1..}] remove reloading
tag @s[tag=loaded] remove loaded
execute if score @s weapon matches 0 run scoreboard players set @s cooldown 0
execute if score @s weapon matches 10..109 run function mgs:guns/_common/handler_switch_rifle
execute if score @s weapon matches 110..209 run function mgs:guns/_common/handler_switch_pistol
execute if score @s weapon matches 210..309 run function mgs:guns/_common/handler_switch_smg
execute if score @s weapon matches 310..409 run function mgs:guns/_common/handler_switch_shotgun
execute if score @s weapon matches 410..509 run function mgs:guns/_common/handler_switch_sniper
execute if score @s weapon matches 510..609 run function mgs:guns/_common/handler_switch_special
execute if score @s weapon matches 1.. run scoreboard players operation v0 V = @s weapon
execute if score @s weapon matches 1.. run scoreboard players operation v0 V %= 10 C
execute if score @s weapon matches 1.. if score v0 V matches 5..9 run function mgs:guns/_common/switch_out
execute if score @s weapon matches 1.. run tag @s add switch
execute if score enableUI V matches 1 if score @s weapon matches 1.. run title @s actionbar {"text":". . .","color":"red"}
stopsound @s voice