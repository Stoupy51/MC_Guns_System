
# TODO:
- custom model for the power
- idea for better zombie AI: use a different entity (for instance warden)

# Done:
- round-end revive of a still-downed player now fully tears down their mannequin/HUD/camera (matched by downed_id) and clears the downed state via `clear_downed_state`, instead of leaving an orphaned mannequin
- falling out of the border is now a TOTAL elimination with no mannequin (`zombies/check_bounds_player` → `revive/full_death`): straight to bled-out spectator, respawned at round end at the player spawn nearest a random alive teammate (`respawn_near_player`)
- reviver actionbar score fixed ("/30t" → "15/30t"): a selector inside a score component didn't resolve in the packet, so the value is read into the `#rv_reviver_disp` holder first
- zombie horde groan is now positional (played from a random nearby zombie's position so it's directional) instead of centred on the player
- power-up cues are now global/non-positional (played at each in-game player's own position) so everyone hears them at full volume, since power-ups affect everyone
- zombie AI getting stuck: `follow_range` lowered 2048 → 40 (it drives both the pathfinding region radius = range+16 and node budget = range*16, so 2048 built a multi-thousand-block region and exploded the A* search → failed paths → frozen zombies). Stuck zombies are now teleported to the nearest unlocked zombie spawn near a player (same pool as the spawner) instead of being killed. Stuck-detection timings unchanged.
- zombies are summoned `Silent`; a managed horde-ambience plays one controlled, count-scaled, volume-capped groan per player (~every 35t) so a big horde sounds full without blowing out the player's ears
