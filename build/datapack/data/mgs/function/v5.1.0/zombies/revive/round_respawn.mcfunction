
#> mgs:v5.1.0/zombies/revive/round_respawn
#
# @within	mgs:v5.1.0/zombies/round_complete
#

# A player still downed when the round ends is revived for free, keeping the loadout: the bleed timer never ran out.
# revive_complete never touches the hotbar; perks stay lost. Must run before the respawn below, which resets the loadout.
execute as @a[tag=mgs.downed_spectator,scores={mgs.zb.in_game=1}] run function mgs:v5.1.0/zombies/revive/revive_complete

# The rest bled out during the round, which costs the loadout.
execute as @a[scores={mgs.zb.in_game=1},gamemode=spectator] run function mgs:v5.1.0/zombies/revive/do_round_respawn

