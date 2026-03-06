
#> mgs:v5.0.0/missions/summon_enemy
#
# @within	mgs:v5.0.0/missions/spawn_enemy_iter with storage mgs:temp _epos
#
# @args		entity (unknown)
#			x (unknown)
#			y (unknown)
#			z (unknown)
#			hp (unknown)
#

$summon $(entity) $(x) $(y) $(z) {Tags:["mgs.mission_enemy","mgs.gm_entity"],DeathLootTable:"minecraft:empty",attributes:[{id:"minecraft:max_health",base:$(hp)}],Health:$(hp)f}

