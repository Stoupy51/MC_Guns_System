
#> mgs:v5.4.1/zombies/revive/stay_down
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/zombies/revive/bleed_out
#			mgs:v5.4.1/zombies/revive/body_lost
#

scoreboard players add @s mgs.st.zb.deaths 1
scoreboard players set @s mgs.zb.downed 0
scoreboard players set @s mgs.zb.revive_p 0
tag @s remove mgs.downed_spectator

# Id-matched: two players downed together can be each other's nearest mannequin.
scoreboard players operation #my_downed_id mgs.data = @s mgs.zb.downed_id

# Tombstone: snapshot the inventory while it is intact.
function mgs:v5.4.1/zombies/perks/tombstone_on_bleed_out

function mgs:v5.4.1/zombies/revive/hide_body

# Full spectator until the next round.
ride @s dismount
gamemode spectator @s

execute as @r[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator,limit=1] run spectate @s
# No alive player: stay where the camera was.
execute unless entity @a[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator] run tp @s ~ ~ ~

