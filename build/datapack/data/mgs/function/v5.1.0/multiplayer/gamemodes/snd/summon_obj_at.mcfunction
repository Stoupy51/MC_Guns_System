
#> mgs:v5.1.0/multiplayer/gamemodes/snd/summon_obj_at
#
# @executed	as the player & at current position
#
# @within	mgs:v5.1.0/multiplayer/gamemodes/snd/summon_obj with storage mgs:temp _snd_pos
#
# @args		x (unknown)
#			y (unknown)
#			z (unknown)
#			label (unknown)
#

$summon minecraft:marker $(x) $(y) $(z) {Tags:["mgs.snd_obj","mgs.gm_entity","mgs.snd_site_$(label)"]}
$summon minecraft:text_display $(x) $(y) $(z) {Tags:["mgs.snd_label","mgs.gm_entity"],billboard:"vertical",text:[{"text":"💣 ","color":"gold"},{"text":"$(label)","color":"yellow","bold":true}],transformation:{translation:[0.0f,2.0f,0.0f],left_rotation:[0.0f,0.0f,0.0f,1.0f],scale:[3.0f,3.0f,3.0f],right_rotation:[0.0f,0.0f,0.0f,1.0f]},shadow:true,see_through:true}
$execute positioned $(x) $(y) $(z) run setblock ~ ~ ~ chest
$execute positioned $(x) $(y) $(z) run setblock ~ ~1 ~ barrier

