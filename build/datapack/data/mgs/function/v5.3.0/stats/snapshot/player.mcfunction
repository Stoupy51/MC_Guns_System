
#> mgs:v5.3.0/stats/snapshot/player
#
# @executed	as @a
#
# @within	mgs:v5.3.0/stats/login_as {uuid:$(uuid),name:"$(name)"}
#			mgs:v5.3.0/stats/snapshot/by_uuid with storage mgs:temp _st_one
#			mgs:v5.3.0/stats/admin/reset_name {uuid:$(uuid),name:"$(name)"}
#
# @args		uuid (unknown)
#			name (string)
#

$execute store result storage mgs:stats players."$(uuid)".zb.games int 1 run scoreboard players get $(name) mgs.st.zb.games
$execute store result storage mgs:stats players."$(uuid)".zb.rounds int 1 run scoreboard players get $(name) mgs.st.zb.rounds
$execute store result storage mgs:stats players."$(uuid)".zb.best_round int 1 run scoreboard players get $(name) mgs.adv.zb.best_round
$execute store result storage mgs:stats players."$(uuid)".zb.kills int 1 run scoreboard players get $(name) mgs.adv.zb.kills
$execute store result storage mgs:stats players."$(uuid)".zb.headshots int 1 run scoreboard players get $(name) mgs.adv.zb.headshots
$execute store result storage mgs:stats players."$(uuid)".zb.downs int 1 run scoreboard players get $(name) mgs.st.zb.downs
$execute store result storage mgs:stats players."$(uuid)".zb.deaths int 1 run scoreboard players get $(name) mgs.st.zb.deaths
$execute store result storage mgs:stats players."$(uuid)".zb.revives int 1 run scoreboard players get $(name) mgs.adv.zb.revives
$execute store result storage mgs:stats players."$(uuid)".zb.points_earned int 1 run scoreboard players get $(name) mgs.st.zb.points_earned
$execute store result storage mgs:stats players."$(uuid)".zb.points_spent int 1 run scoreboard players get $(name) mgs.adv.zb.spending
$execute store result storage mgs:stats players."$(uuid)".zb.doors int 1 run scoreboard players get $(name) mgs.st.zb.doors
$execute store result storage mgs:stats players."$(uuid)".zb.boxes int 1 run scoreboard players get $(name) mgs.st.zb.boxes
$execute store result storage mgs:stats players."$(uuid)".zb.wallbuys int 1 run scoreboard players get $(name) mgs.st.zb.wallbuys
$execute store result storage mgs:stats players."$(uuid)".zb.perks int 1 run scoreboard players get $(name) mgs.adv.zb.perks
$execute store result storage mgs:stats players."$(uuid)".zb.pap int 1 run scoreboard players get $(name) mgs.adv.zb.pap
$execute store result storage mgs:stats players."$(uuid)".zb.traps int 1 run scoreboard players get $(name) mgs.st.zb.traps
$execute store result storage mgs:stats players."$(uuid)".zb.powerups int 1 run scoreboard players get $(name) mgs.st.zb.powerups
$execute store result storage mgs:stats players."$(uuid)".zb.barricades int 1 run scoreboard players get $(name) mgs.st.zb.barricades
$execute store result storage mgs:stats players."$(uuid)".zb.power int 1 run scoreboard players get $(name) mgs.st.zb.power
$execute store result storage mgs:stats players."$(uuid)".zb.time int 1 run scoreboard players get $(name) mgs.st.zb.time
$execute store result storage mgs:stats players."$(uuid)".mp.games int 1 run scoreboard players get $(name) mgs.st.mp.games
$execute store result storage mgs:stats players."$(uuid)".mp.wins int 1 run scoreboard players get $(name) mgs.adv.mp.wins
$execute store result storage mgs:stats players."$(uuid)".mp.losses int 1 run scoreboard players get $(name) mgs.st.mp.losses
$execute store result storage mgs:stats players."$(uuid)".mp.kills int 1 run scoreboard players get $(name) mgs.adv.mp.kills
$execute store result storage mgs:stats players."$(uuid)".mp.deaths int 1 run scoreboard players get $(name) mgs.st.mp.deaths
$execute store result storage mgs:stats players."$(uuid)".mp.headshots int 1 run scoreboard players get $(name) mgs.adv.mp.headshots
$execute store result storage mgs:stats players."$(uuid)".mp.captures int 1 run scoreboard players get $(name) mgs.st.mp.captures
$execute store result storage mgs:stats players."$(uuid)".mp.plants int 1 run scoreboard players get $(name) mgs.st.mp.plants
$execute store result storage mgs:stats players."$(uuid)".mp.defuses int 1 run scoreboard players get $(name) mgs.st.mp.defuses
$execute store result storage mgs:stats players."$(uuid)".mp.objectives int 1 run scoreboard players get $(name) mgs.adv.mp.objectives
$execute store result storage mgs:stats players."$(uuid)".mp.time int 1 run scoreboard players get $(name) mgs.st.mp.time
$execute store result storage mgs:stats players."$(uuid)".mi.games int 1 run scoreboard players get $(name) mgs.st.mi.games
$execute store result storage mgs:stats players."$(uuid)".mi.completed int 1 run scoreboard players get $(name) mgs.adv.mi.completed
$execute store result storage mgs:stats players."$(uuid)".mi.kills int 1 run scoreboard players get $(name) mgs.adv.mi.kills
$execute store result storage mgs:stats players."$(uuid)".mi.headshots int 1 run scoreboard players get $(name) mgs.st.mi.headshots
$execute store result storage mgs:stats players."$(uuid)".mi.deaths int 1 run scoreboard players get $(name) mgs.st.mi.deaths
$execute store result storage mgs:stats players."$(uuid)".mi.time int 1 run scoreboard players get $(name) mgs.st.mi.time
$execute store result storage mgs:stats players."$(uuid)".mp.modes.ffa.games int 1 run scoreboard players get $(name) mgs.st.mp.ffa.games
$execute store result storage mgs:stats players."$(uuid)".mp.modes.ffa.wins int 1 run scoreboard players get $(name) mgs.st.mp.ffa.wins
$execute store result storage mgs:stats players."$(uuid)".mp.modes.tdm.games int 1 run scoreboard players get $(name) mgs.st.mp.tdm.games
$execute store result storage mgs:stats players."$(uuid)".mp.modes.tdm.wins int 1 run scoreboard players get $(name) mgs.st.mp.tdm.wins
$execute store result storage mgs:stats players."$(uuid)".mp.modes.dom.games int 1 run scoreboard players get $(name) mgs.st.mp.dom.games
$execute store result storage mgs:stats players."$(uuid)".mp.modes.dom.wins int 1 run scoreboard players get $(name) mgs.st.mp.dom.wins
$execute store result storage mgs:stats players."$(uuid)".mp.modes.hp.games int 1 run scoreboard players get $(name) mgs.st.mp.hp.games
$execute store result storage mgs:stats players."$(uuid)".mp.modes.hp.wins int 1 run scoreboard players get $(name) mgs.st.mp.hp.wins
$execute store result storage mgs:stats players."$(uuid)".mp.modes.snd.games int 1 run scoreboard players get $(name) mgs.st.mp.snd.games
$execute store result storage mgs:stats players."$(uuid)".mp.modes.snd.wins int 1 run scoreboard players get $(name) mgs.st.mp.snd.wins
$execute store result storage mgs:stats players."$(uuid)".mp.modes.demo.games int 1 run scoreboard players get $(name) mgs.st.mp.demo.games
$execute store result storage mgs:stats players."$(uuid)".mp.modes.demo.wins int 1 run scoreboard players get $(name) mgs.st.mp.demo.wins
$execute store result storage mgs:stats players."$(uuid)".level.mp int 1 run scoreboard players get $(name) mgs.mp.xp_level
$execute store result storage mgs:stats players."$(uuid)".level.zb int 1 run scoreboard players get $(name) mgs.zb.xp_level

