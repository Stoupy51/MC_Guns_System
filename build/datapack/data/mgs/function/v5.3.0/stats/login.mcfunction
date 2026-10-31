
#> mgs:v5.3.0/stats/login
#
# @executed	as @a
#
# @within	mgs:v5.3.0/progression/tick_player
#

scoreboard players set @s mgs.st.login 0
execute unless score @s mgs.mp.xp_level matches 1.. run function mgs:v5.3.0/progression/mp/init
execute unless score @s mgs.zb.xp_level matches 1.. run function mgs:v5.3.0/progression/zb/init

function mgs:v5.3.0/players/read_name
data modify storage mgs:temp _st set value {}
data modify storage mgs:temp _st.uuid set from entity @s UUID
data modify storage mgs:temp _st.name set from storage mgs:temp _name
function mgs:v5.3.0/stats/login_as with storage mgs:temp _st

