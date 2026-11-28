
#> mgs:v5.4.4/stats/login
#
# @within	mgs:v5.4.4/dialog/close_then
#			mgs:v5.4.4/progression/tick_player
#

execute if entity @s[gamemode=spectator,scores={mgs.mp.in_game=1}] if data storage mgs:multiplayer game{state:"lobby"} run function mgs:v5.4.4/multiplayer/reset_player

scoreboard players set @s mgs.st.login 0
execute if score @s mgs.st.reset matches 1 run function mgs:v5.4.4/stats/finish_reset
execute unless score @s mgs.mp.xp_level matches 1.. run function mgs:v5.4.4/progression/mp/init
execute unless score @s mgs.zb.xp_level matches 1.. run function mgs:v5.4.4/progression/zb/init

function mgs:v5.4.4/players/read_name
data modify storage mgs:temp _st set value {}
data modify storage mgs:temp _st.uuid set from entity @s UUID
data modify storage mgs:temp _st.name set from storage mgs:temp _name
function mgs:v5.4.4/stats/login_as with storage mgs:temp _st

