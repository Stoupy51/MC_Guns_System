
#> mgs:v5.4.4/stats/admin/reset_name
#
# @within	mgs:v5.4.4/dialog/close_then
#			mgs:v5.4.4/stats/admin/reset_uuid with storage mgs:temp _st_one
#
# @args		name (unknown)
#			uuid (unknown)
#

$scoreboard players reset $(name) mgs.mp.xp_total
$scoreboard players reset $(name) mgs.mp.xp_level
$scoreboard players reset $(name) mgs.mp.xp_prog
$scoreboard players reset $(name) mgs.zb.xp_total
$scoreboard players reset $(name) mgs.zb.xp_level
$scoreboard players reset $(name) mgs.zb.xp_prog
$scoreboard players reset $(name) mgs.zb.xp_spent_acc
$scoreboard players reset $(name) mgs.adv.mp.kills
$scoreboard players reset $(name) mgs.adv.mp.headshots
$scoreboard players reset $(name) mgs.adv.mp.wins
$scoreboard players reset $(name) mgs.adv.mp.objectives
$scoreboard players reset $(name) mgs.adv.zb.kills
$scoreboard players reset $(name) mgs.adv.zb.headshots
$scoreboard players reset $(name) mgs.adv.zb.best_round
$scoreboard players reset $(name) mgs.adv.zb.revives
$scoreboard players reset $(name) mgs.adv.zb.perks
$scoreboard players reset $(name) mgs.adv.zb.pap
$scoreboard players reset $(name) mgs.adv.zb.box
$scoreboard players reset $(name) mgs.adv.zb.spending
$scoreboard players reset $(name) mgs.adv.mi.kills
$scoreboard players reset $(name) mgs.adv.mi.completed
$scoreboard players reset $(name) mgs.player.hitmarker
$scoreboard players reset $(name) mgs.player.damage_debug
$scoreboard players reset $(name) mgs.mp.class
$scoreboard players reset $(name) mgs.mp.default
$scoreboard players reset $(name) mgs.zb.passive
$scoreboard players reset $(name) mgs.zb.ability
$scoreboard players reset $(name) mgs.zb.knife_camo
$scoreboard players reset $(name) mgs.st.zb.games
$scoreboard players reset $(name) mgs.st.zb.rounds
$scoreboard players reset $(name) mgs.st.zb.shots
$scoreboard players reset $(name) mgs.st.zb.hits
$scoreboard players reset $(name) mgs.st.zb.downs
$scoreboard players reset $(name) mgs.st.zb.deaths
$scoreboard players reset $(name) mgs.st.zb.points_earned
$scoreboard players reset $(name) mgs.st.zb.doors
$scoreboard players reset $(name) mgs.st.zb.boxes
$scoreboard players reset $(name) mgs.st.zb.wallbuys
$scoreboard players reset $(name) mgs.st.zb.traps
$scoreboard players reset $(name) mgs.st.zb.powerups
$scoreboard players reset $(name) mgs.st.zb.barricades
$scoreboard players reset $(name) mgs.st.zb.power
$scoreboard players reset $(name) mgs.st.zb.time
$scoreboard players reset $(name) mgs.st.mp.games
$scoreboard players reset $(name) mgs.st.mp.losses
$scoreboard players reset $(name) mgs.st.mp.deaths
$scoreboard players reset $(name) mgs.st.mp.shots
$scoreboard players reset $(name) mgs.st.mp.hits
$scoreboard players reset $(name) mgs.st.mp.captures
$scoreboard players reset $(name) mgs.st.mp.plants
$scoreboard players reset $(name) mgs.st.mp.defuses
$scoreboard players reset $(name) mgs.st.mp.time
$scoreboard players reset $(name) mgs.st.mi.games
$scoreboard players reset $(name) mgs.st.mi.headshots
$scoreboard players reset $(name) mgs.st.mi.shots
$scoreboard players reset $(name) mgs.st.mi.hits
$scoreboard players reset $(name) mgs.st.mi.deaths
$scoreboard players reset $(name) mgs.st.mi.time
$scoreboard players reset $(name) mgs.st.mp.ffa.games
$scoreboard players reset $(name) mgs.st.mp.ffa.wins
$scoreboard players reset $(name) mgs.st.mp.tdm.games
$scoreboard players reset $(name) mgs.st.mp.tdm.wins
$scoreboard players reset $(name) mgs.st.mp.dom.games
$scoreboard players reset $(name) mgs.st.mp.dom.wins
$scoreboard players reset $(name) mgs.st.mp.hp.games
$scoreboard players reset $(name) mgs.st.mp.hp.wins
$scoreboard players reset $(name) mgs.st.mp.snd.games
$scoreboard players reset $(name) mgs.st.mp.snd.wins
$scoreboard players reset $(name) mgs.st.mp.demo.games
$scoreboard players reset $(name) mgs.st.mp.demo.wins
$scoreboard players set $(name) mgs.mp.xp_level 1
$scoreboard players set $(name) mgs.zb.xp_level 1
$function mgs:v5.4.4/stats/board/forget {uuid:$(uuid)}
$execute as $(name) run function mgs:v5.4.4/progression/mp/init
$execute as $(name) run function mgs:v5.4.4/progression/zb/init
$execute if entity $(name) run advancement revoke $(name) everything
$execute unless entity $(name) run scoreboard players set $(name) mgs.st.reset 1
$function mgs:v5.4.4/stats/snapshot/player {uuid:$(uuid),name:"$(name)"}
$tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.fully_reset","fallback":"Fully reset: ","color":"yellow"},{"text":"$(name)","color":"white"}]

