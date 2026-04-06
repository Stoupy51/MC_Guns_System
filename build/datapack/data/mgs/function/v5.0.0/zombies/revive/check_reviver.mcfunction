
#> mgs:v5.0.0/zombies/revive/check_reviver
#
# @executed	as @a[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator,distance=..2.5] & facing entity @s eyes
#
# @within	mgs:v5.0.0/zombies/revive/downed_tick [ as @a[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator,distance=..2.5] & facing entity @s eyes ]
#

# The command runs 'as @a[alive, nearby] facing entity @s[downed] eyes'
# Check if the alive player's view direction roughly points at the downed player
# We use a simple raycast: the alive player's look direction should point within ~30° of the downed player

# Simple approach: just check distance (if within range, they are reviving)
# The 'facing entity @s eyes' rotation is set but we just need proximity + not downed
scoreboard players set #zb_reviving mgs.data 1

# Show actionbar to reviver
execute store result storage mgs:temp _rv_prog int 1 run scoreboard players get @p[tag=mgs.downed,sort=nearest,distance=..2.5] mgs.zb.revive_p

# Check if reviver has Quick Revive perk
execute if entity @s[tag=mgs.perk.quick_revive] run function mgs:v5.0.0/zombies/revive/show_reviver_bar_quick
execute unless entity @s[tag=mgs.perk.quick_revive] run function mgs:v5.0.0/zombies/revive/show_reviver_bar_normal

