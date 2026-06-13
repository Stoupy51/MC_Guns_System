
#> mgs:v5.0.1/zombies/perks/update_quick_revive_price
#
# @within	mgs:v5.0.1/zombies/preload_complete
#			mgs:v5.0.1/zombies/game_tick
#

# Count alive in-game players
execute store result score #qr_players mgs.data if entity @a[scores={mgs.zb.in_game=1},gamemode=!spectator]

# Solo (or none): discounted to 500
execute if score #qr_players mgs.data matches ..1 run scoreboard players set @e[tag=mgs.pk_quick_revive] mgs.zb.perk.price 500

# Two or more: restore each machine's map-defined price
execute if score #qr_players mgs.data matches 2.. as @e[tag=mgs.pk_quick_revive] run scoreboard players operation @s mgs.zb.perk.price = @s mgs.zb.perk.base_price

