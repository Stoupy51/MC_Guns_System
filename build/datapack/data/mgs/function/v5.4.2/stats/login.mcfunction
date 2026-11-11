
#> mgs:v5.4.2/stats/login
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/progression/tick_player
#

execute if entity @s[gamemode=spectator,scores={mgs.mp.in_game=1}] if data storage mgs:multiplayer game{state:"lobby"} run function mgs:v5.4.2/multiplayer/reset_player

scoreboard players set @s mgs.st.login 0
execute unless score @s mgs.mp.xp_level matches 1.. run function mgs:v5.4.2/progression/mp/init
execute unless score @s mgs.zb.xp_level matches 1.. run function mgs:v5.4.2/progression/zb/init

function mgs:v5.4.2/players/read_name
data modify storage mgs:temp _st set value {}
data modify storage mgs:temp _st.uuid set from entity @s UUID
data modify storage mgs:temp _st.name set from storage mgs:temp _name
function mgs:v5.4.2/stats/login_as with storage mgs:temp _st

