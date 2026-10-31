
#> mgs:v5.3.0/stats/rename
#
# @executed	as @a
#
# @within	mgs:v5.3.0/stats/login_as with storage mgs:temp _st
#
# @args		old (unknown)
#			name (unknown)
#

$execute if score $(old) bs.id matches -2147483648.. run scoreboard players operation $(name) bs.id = $(old) bs.id
$execute if score $(old) mgs.st.index matches -2147483648.. run scoreboard players operation $(name) mgs.st.index = $(old) mgs.st.index
$execute if score $(old) mgs.mp.xp_total matches -2147483648.. run scoreboard players operation $(name) mgs.mp.xp_total = $(old) mgs.mp.xp_total
$execute if score $(old) mgs.mp.xp_level matches -2147483648.. run scoreboard players operation $(name) mgs.mp.xp_level = $(old) mgs.mp.xp_level
$execute if score $(old) mgs.mp.xp_prog matches -2147483648.. run scoreboard players operation $(name) mgs.mp.xp_prog = $(old) mgs.mp.xp_prog
$execute if score $(old) mgs.zb.xp_total matches -2147483648.. run scoreboard players operation $(name) mgs.zb.xp_total = $(old) mgs.zb.xp_total
$execute if score $(old) mgs.zb.xp_level matches -2147483648.. run scoreboard players operation $(name) mgs.zb.xp_level = $(old) mgs.zb.xp_level
$execute if score $(old) mgs.zb.xp_prog matches -2147483648.. run scoreboard players operation $(name) mgs.zb.xp_prog = $(old) mgs.zb.xp_prog
$execute if score $(old) mgs.zb.xp_spent_acc matches -2147483648.. run scoreboard players operation $(name) mgs.zb.xp_spent_acc = $(old) mgs.zb.xp_spent_acc
$execute if score $(old) mgs.adv.mp.kills matches -2147483648.. run scoreboard players operation $(name) mgs.adv.mp.kills = $(old) mgs.adv.mp.kills
$execute if score $(old) mgs.adv.mp.headshots matches -2147483648.. run scoreboard players operation $(name) mgs.adv.mp.headshots = $(old) mgs.adv.mp.headshots
$execute if score $(old) mgs.adv.mp.wins matches -2147483648.. run scoreboard players operation $(name) mgs.adv.mp.wins = $(old) mgs.adv.mp.wins
$execute if score $(old) mgs.adv.mp.objectives matches -2147483648.. run scoreboard players operation $(name) mgs.adv.mp.objectives = $(old) mgs.adv.mp.objectives
$execute if score $(old) mgs.adv.zb.kills matches -2147483648.. run scoreboard players operation $(name) mgs.adv.zb.kills = $(old) mgs.adv.zb.kills
$execute if score $(old) mgs.adv.zb.headshots matches -2147483648.. run scoreboard players operation $(name) mgs.adv.zb.headshots = $(old) mgs.adv.zb.headshots
$execute if score $(old) mgs.adv.zb.best_round matches -2147483648.. run scoreboard players operation $(name) mgs.adv.zb.best_round = $(old) mgs.adv.zb.best_round
$execute if score $(old) mgs.adv.zb.revives matches -2147483648.. run scoreboard players operation $(name) mgs.adv.zb.revives = $(old) mgs.adv.zb.revives
$execute if score $(old) mgs.adv.zb.perks matches -2147483648.. run scoreboard players operation $(name) mgs.adv.zb.perks = $(old) mgs.adv.zb.perks
$execute if score $(old) mgs.adv.zb.pap matches -2147483648.. run scoreboard players operation $(name) mgs.adv.zb.pap = $(old) mgs.adv.zb.pap
$execute if score $(old) mgs.adv.zb.box matches -2147483648.. run scoreboard players operation $(name) mgs.adv.zb.box = $(old) mgs.adv.zb.box
$execute if score $(old) mgs.adv.zb.spending matches -2147483648.. run scoreboard players operation $(name) mgs.adv.zb.spending = $(old) mgs.adv.zb.spending
$execute if score $(old) mgs.adv.mi.kills matches -2147483648.. run scoreboard players operation $(name) mgs.adv.mi.kills = $(old) mgs.adv.mi.kills
$execute if score $(old) mgs.adv.mi.completed matches -2147483648.. run scoreboard players operation $(name) mgs.adv.mi.completed = $(old) mgs.adv.mi.completed
$execute if score $(old) mgs.player.hitmarker matches -2147483648.. run scoreboard players operation $(name) mgs.player.hitmarker = $(old) mgs.player.hitmarker
$execute if score $(old) mgs.player.damage_debug matches -2147483648.. run scoreboard players operation $(name) mgs.player.damage_debug = $(old) mgs.player.damage_debug
$execute if score $(old) mgs.mp.class matches -2147483648.. run scoreboard players operation $(name) mgs.mp.class = $(old) mgs.mp.class
$execute if score $(old) mgs.mp.default matches -2147483648.. run scoreboard players operation $(name) mgs.mp.default = $(old) mgs.mp.default
$execute if score $(old) mgs.mp.pid matches -2147483648.. run scoreboard players operation $(name) mgs.mp.pid = $(old) mgs.mp.pid
$execute if score $(old) mgs.zb.passive matches -2147483648.. run scoreboard players operation $(name) mgs.zb.passive = $(old) mgs.zb.passive
$execute if score $(old) mgs.zb.ability matches -2147483648.. run scoreboard players operation $(name) mgs.zb.ability = $(old) mgs.zb.ability
$execute if score $(old) mgs.zb.knife_camo matches -2147483648.. run scoreboard players operation $(name) mgs.zb.knife_camo = $(old) mgs.zb.knife_camo
$execute if score $(old) mgs.st.zb.games matches -2147483648.. run scoreboard players operation $(name) mgs.st.zb.games = $(old) mgs.st.zb.games
$execute if score $(old) mgs.st.zb.rounds matches -2147483648.. run scoreboard players operation $(name) mgs.st.zb.rounds = $(old) mgs.st.zb.rounds
$execute if score $(old) mgs.st.zb.downs matches -2147483648.. run scoreboard players operation $(name) mgs.st.zb.downs = $(old) mgs.st.zb.downs
$execute if score $(old) mgs.st.zb.deaths matches -2147483648.. run scoreboard players operation $(name) mgs.st.zb.deaths = $(old) mgs.st.zb.deaths
$execute if score $(old) mgs.st.zb.points_earned matches -2147483648.. run scoreboard players operation $(name) mgs.st.zb.points_earned = $(old) mgs.st.zb.points_earned
$execute if score $(old) mgs.st.zb.doors matches -2147483648.. run scoreboard players operation $(name) mgs.st.zb.doors = $(old) mgs.st.zb.doors
$execute if score $(old) mgs.st.zb.boxes matches -2147483648.. run scoreboard players operation $(name) mgs.st.zb.boxes = $(old) mgs.st.zb.boxes
$execute if score $(old) mgs.st.zb.wallbuys matches -2147483648.. run scoreboard players operation $(name) mgs.st.zb.wallbuys = $(old) mgs.st.zb.wallbuys
$execute if score $(old) mgs.st.zb.traps matches -2147483648.. run scoreboard players operation $(name) mgs.st.zb.traps = $(old) mgs.st.zb.traps
$execute if score $(old) mgs.st.zb.powerups matches -2147483648.. run scoreboard players operation $(name) mgs.st.zb.powerups = $(old) mgs.st.zb.powerups
$execute if score $(old) mgs.st.zb.barricades matches -2147483648.. run scoreboard players operation $(name) mgs.st.zb.barricades = $(old) mgs.st.zb.barricades
$execute if score $(old) mgs.st.zb.power matches -2147483648.. run scoreboard players operation $(name) mgs.st.zb.power = $(old) mgs.st.zb.power
$execute if score $(old) mgs.st.zb.time matches -2147483648.. run scoreboard players operation $(name) mgs.st.zb.time = $(old) mgs.st.zb.time
$execute if score $(old) mgs.st.mp.games matches -2147483648.. run scoreboard players operation $(name) mgs.st.mp.games = $(old) mgs.st.mp.games
$execute if score $(old) mgs.st.mp.losses matches -2147483648.. run scoreboard players operation $(name) mgs.st.mp.losses = $(old) mgs.st.mp.losses
$execute if score $(old) mgs.st.mp.deaths matches -2147483648.. run scoreboard players operation $(name) mgs.st.mp.deaths = $(old) mgs.st.mp.deaths
$execute if score $(old) mgs.st.mp.captures matches -2147483648.. run scoreboard players operation $(name) mgs.st.mp.captures = $(old) mgs.st.mp.captures
$execute if score $(old) mgs.st.mp.plants matches -2147483648.. run scoreboard players operation $(name) mgs.st.mp.plants = $(old) mgs.st.mp.plants
$execute if score $(old) mgs.st.mp.defuses matches -2147483648.. run scoreboard players operation $(name) mgs.st.mp.defuses = $(old) mgs.st.mp.defuses
$execute if score $(old) mgs.st.mp.time matches -2147483648.. run scoreboard players operation $(name) mgs.st.mp.time = $(old) mgs.st.mp.time
$execute if score $(old) mgs.st.mi.games matches -2147483648.. run scoreboard players operation $(name) mgs.st.mi.games = $(old) mgs.st.mi.games
$execute if score $(old) mgs.st.mi.headshots matches -2147483648.. run scoreboard players operation $(name) mgs.st.mi.headshots = $(old) mgs.st.mi.headshots
$execute if score $(old) mgs.st.mi.deaths matches -2147483648.. run scoreboard players operation $(name) mgs.st.mi.deaths = $(old) mgs.st.mi.deaths
$execute if score $(old) mgs.st.mi.time matches -2147483648.. run scoreboard players operation $(name) mgs.st.mi.time = $(old) mgs.st.mi.time
$execute if score $(old) mgs.st.mp.ffa.games matches -2147483648.. run scoreboard players operation $(name) mgs.st.mp.ffa.games = $(old) mgs.st.mp.ffa.games
$execute if score $(old) mgs.st.mp.ffa.wins matches -2147483648.. run scoreboard players operation $(name) mgs.st.mp.ffa.wins = $(old) mgs.st.mp.ffa.wins
$execute if score $(old) mgs.st.mp.tdm.games matches -2147483648.. run scoreboard players operation $(name) mgs.st.mp.tdm.games = $(old) mgs.st.mp.tdm.games
$execute if score $(old) mgs.st.mp.tdm.wins matches -2147483648.. run scoreboard players operation $(name) mgs.st.mp.tdm.wins = $(old) mgs.st.mp.tdm.wins
$execute if score $(old) mgs.st.mp.dom.games matches -2147483648.. run scoreboard players operation $(name) mgs.st.mp.dom.games = $(old) mgs.st.mp.dom.games
$execute if score $(old) mgs.st.mp.dom.wins matches -2147483648.. run scoreboard players operation $(name) mgs.st.mp.dom.wins = $(old) mgs.st.mp.dom.wins
$execute if score $(old) mgs.st.mp.hp.games matches -2147483648.. run scoreboard players operation $(name) mgs.st.mp.hp.games = $(old) mgs.st.mp.hp.games
$execute if score $(old) mgs.st.mp.hp.wins matches -2147483648.. run scoreboard players operation $(name) mgs.st.mp.hp.wins = $(old) mgs.st.mp.hp.wins
$execute if score $(old) mgs.st.mp.snd.games matches -2147483648.. run scoreboard players operation $(name) mgs.st.mp.snd.games = $(old) mgs.st.mp.snd.games
$execute if score $(old) mgs.st.mp.snd.wins matches -2147483648.. run scoreboard players operation $(name) mgs.st.mp.snd.wins = $(old) mgs.st.mp.snd.wins
$execute if score $(old) mgs.st.mp.demo.games matches -2147483648.. run scoreboard players operation $(name) mgs.st.mp.demo.games = $(old) mgs.st.mp.demo.games
$execute if score $(old) mgs.st.mp.demo.wins matches -2147483648.. run scoreboard players operation $(name) mgs.st.mp.demo.wins = $(old) mgs.st.mp.demo.wins
$scoreboard players reset $(old)

