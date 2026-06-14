
# TODO:
- zombie AI: please don't get stuck, look at minecraft source code

# Done:
- random perk: counts unowned perks with `unless ... matches 1` (perk scores are reset/unset at game start, so the old `matches 0` wrongly reported every perk as owned)
- perks machine item display raised by +0.13 (perk call site only, not the shared PAP display)
- player info paper now lists owned perks (themed by perk colour) under the stats
- editor: constant/enum fields (trap type, door animation, link_id, perk_id, power, …) show an `ⓘ` hover tooltip describing the possible values (see `FIELD_DOCS` in `map_editor.py`)
- zombies are summoned `Silent`; a managed horde-ambience plays one controlled, count-scaled, volume-capped groan per player (~every 35t) so a big horde sounds full without blowing out the player's ears
- downed players can pick up power-ups by crawling their mannequin over them (credited to the downed player)
