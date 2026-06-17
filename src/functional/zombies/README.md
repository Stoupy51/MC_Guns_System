
# TODO:
- downed player, when round finishes and they revive (not correctly btw), the mannequin is not removed.
- When falling out of the border, it should totally kill the player (no down mannequin), respawn at nearest player spawn from random player at round end.
- revive text does not show the proper score value : "/30t" instead of "x/30t"
- custom model for the power
- idea for better zombie AI: use a different entity (for instance warden)

# Done:
- zombie AI getting stuck: `follow_range` lowered 2048 → 40 (it drives both the pathfinding region radius = range+16 and node budget = range*16, so 2048 built a multi-thousand-block region and exploded the A* search → failed paths → frozen zombies). Stuck zombies are now teleported to the nearest unlocked zombie spawn near a player (same pool as the spawner) instead of being killed. Stuck-detection timings unchanged.
- zombies are summoned `Silent`; a managed horde-ambience plays one controlled, count-scaled, volume-capped groan per player (~every 35t) so a big horde sounds full without blowing out the player's ears
