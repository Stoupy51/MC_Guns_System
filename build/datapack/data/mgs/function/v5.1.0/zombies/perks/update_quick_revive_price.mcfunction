
#> mgs:v5.1.0/zombies/perks/update_quick_revive_price
#
# @within	mgs:v5.1.0/zombies/preload_complete
#			mgs:v5.1.0/zombies/game_tick
#

execute store result score #qr_players mgs.data if entity @a[scores={mgs.zb.in_game=1},gamemode=!spectator]

execute if score #qr_players mgs.data matches ..1 run scoreboard players set @e[tag=mgs.pk_quick_revive] mgs.zb.perk.price 500

# Two or more: each machine's map price.
execute if score #qr_players mgs.data matches 2.. as @e[tag=mgs.pk_quick_revive] run scoreboard players operation @s mgs.zb.perk.price = @s mgs.zb.perk.base_price

