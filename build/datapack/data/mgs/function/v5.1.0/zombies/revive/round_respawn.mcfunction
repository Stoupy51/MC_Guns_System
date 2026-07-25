
#> mgs:v5.1.0/zombies/revive/round_respawn
#
# @within	mgs:v5.1.0/zombies/round_complete
#

# Free pickup first: a player still DOWNED when the round ended, with a live teammate standing within
# 10 blocks of their body, is revived instead of respawned — they keep their guns.
# Must run before the respawn pass below, which would otherwise wipe them back to the starting loadout.
execute as @a[tag=mgs.downed_spectator,scores={mgs.zb.in_game=1}] run function mgs:v5.1.0/zombies/revive/round_end_pickup

# Respawn every remaining spectator (bled out, or downed with nobody close enough)
execute as @a[scores={mgs.zb.in_game=1},gamemode=spectator] run function mgs:v5.1.0/zombies/revive/do_round_respawn

