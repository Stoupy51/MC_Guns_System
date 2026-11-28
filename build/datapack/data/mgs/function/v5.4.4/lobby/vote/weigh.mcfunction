
#> mgs:v5.4.4/lobby/vote/weigh
#
# @within	mgs:v5.4.4/dialog/close_then
#			mgs:v5.4.4/lobby/multiplayer/resolve {slot:1}
#			mgs:v5.4.4/lobby/multiplayer/resolve {slot:2}
#			mgs:v5.4.4/lobby/multiplayer/resolve {slot:3}
#			mgs:v5.4.4/lobby/multiplayer/resolve {slot:4}
#			mgs:v5.4.4/lobby/multiplayer/resolve {slot:5}
#			mgs:v5.4.4/lobby/multiplayer/resolve {slot:6}
#			mgs:v5.4.4/lobby/multiplayer/resolve {slot:7}
#			mgs:v5.4.4/lobby/multiplayer/resolve {slot:8}
#			mgs:v5.4.4/lobby/zombies/resolve {slot:1}
#			mgs:v5.4.4/lobby/zombies/resolve {slot:2}
#			mgs:v5.4.4/lobby/zombies/resolve {slot:3}
#			mgs:v5.4.4/lobby/zombies/resolve {slot:4}
#			mgs:v5.4.4/lobby/zombies/resolve {slot:5}
#			mgs:v5.4.4/lobby/zombies/resolve {slot:6}
#			mgs:v5.4.4/lobby/zombies/resolve {slot:7}
#			mgs:v5.4.4/lobby/zombies/resolve {slot:8}
#			mgs:v5.4.4/lobby/missions/resolve {slot:1}
#			mgs:v5.4.4/lobby/missions/resolve {slot:2}
#			mgs:v5.4.4/lobby/missions/resolve {slot:3}
#			mgs:v5.4.4/lobby/missions/resolve {slot:4}
#			mgs:v5.4.4/lobby/missions/resolve {slot:5}
#			mgs:v5.4.4/lobby/missions/resolve {slot:6}
#			mgs:v5.4.4/lobby/missions/resolve {slot:7}
#			mgs:v5.4.4/lobby/missions/resolve {slot:8}
#
# @args		slot (int)
#

scoreboard players operation #lv_k mgs.data *= #100 mgs.data
execute store result score #lv_r mgs.data run random value 0..99
scoreboard players operation #lv_k mgs.data += #lv_r mgs.data
execute unless score #lv_k mgs.data > #lv_best mgs.data run return 0
scoreboard players operation #lv_best mgs.data = #lv_k mgs.data
$scoreboard players set #lv_win mgs.data $(slot)

