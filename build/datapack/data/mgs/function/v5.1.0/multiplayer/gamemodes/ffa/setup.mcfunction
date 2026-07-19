
#> mgs:v5.1.0/multiplayer/gamemodes/ffa/setup
#
# @within	mgs:v5.1.0/multiplayer/start
#

# Clear leftover red/blue assignments only — players must STAY on the mgs.ffa team
# (it carries nametagVisibility never + friendlyFire true; a bare 'team leave @a' made nametags visible)
team leave @a[team=mgs.red]
team leave @a[team=mgs.blue]
scoreboard players set @a mgs.mp.team 0
tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.free_for_all_everyone_for_themselves","color":"yellow"}]

