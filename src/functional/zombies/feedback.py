
# Zombies Interaction Feedback
# Shared sound cues used by interaction systems (wallbuys, doors, perks, traps, mystery box).
from stewbeet import Mem, write_versioned_function


def generate_zombies_feedback() -> None:
	ns: str = Mem.ctx.project_id

	write_versioned_function("zombies/feedback/sound_success", """
playsound minecraft:entity.experience_orb.pickup ambient @s ~ ~ ~ 0.8 1.25
""")
	write_versioned_function("zombies/feedback/sound_refill", """
playsound minecraft:block.note_block.pling ambient @s ~ ~ ~ 0.8 1.45
""")
	write_versioned_function("zombies/feedback/sound_replace", """
playsound minecraft:item.armor.equip_iron ambient @s ~ ~ ~ 0.9 1.0
""")
	write_versioned_function("zombies/feedback/sound_deny", """
playsound minecraft:entity.villager.no ambient @s ~ ~ ~ 0.8 1.0
""")
	write_versioned_function("zombies/feedback/sound_announce", f"""
playsound minecraft:block.note_block.bit ambient @a[scores={{{ns}.zb.in_game=1}}] ~ ~ ~ 0.6 0.9
""")
	write_versioned_function("zombies/feedback/sound_power_on", f"""
playsound minecraft:block.beacon.activate ambient @a[scores={{{ns}.zb.in_game=1}}] ~ ~ ~ 0.9 1.0
""")
	write_versioned_function("zombies/feedback/sound_box_spin", f"""
playsound {ns}:zombies/mystery_box/box_spin ambient @a[scores={{{ns}.zb.in_game=1}}] ~ ~ ~ 0.1 1.0
playsound {ns}:zombies/mystery_box/music_box ambient @a[scores={{{ns}.zb.in_game=1}}] ~ ~ ~ 1.0 1.0
""")
	write_versioned_function("zombies/feedback/sound_box_ready", f"""
playsound minecraft:entity.player.levelup ambient @a[scores={{{ns}.zb.in_game=1}}] ~ ~ ~ 0.7 1.0
""")

	## Mystery Box: Black Ops-style sound effects
	write_versioned_function("zombies/feedback/sound_box_open", f"""
playsound {ns}:zombies/mystery_box/open ambient @a[scores={{{ns}.zb.in_game=1}}] ~ ~ ~ 0.9 1.0
""")
	write_versioned_function("zombies/feedback/sound_box_close", f"""
playsound {ns}:zombies/mystery_box/close ambient @a[scores={{{ns}.zb.in_game=1}}] ~ ~ ~ 0.9 1.0
""")
	write_versioned_function("zombies/feedback/sound_box_bye_bye", f"""
execute as @a[scores={{{ns}.zb.in_game=1}}] at @s run playsound {ns}:zombies/mystery_box/bye_bye ambient @s ~ ~ ~ 1.0 1.0
""")
	write_versioned_function("zombies/feedback/sound_box_woosh", f"""
playsound {ns}:zombies/mystery_box/woosh ambient @a[scores={{{ns}.zb.in_game=1}}] ~ ~ ~ 1.0 1.0
""")
	write_versioned_function("zombies/feedback/sound_box_disappear", f"""
playsound {ns}:zombies/mystery_box/disappear ambient @a[scores={{{ns}.zb.in_game=1}}] ~ ~ ~ 1.0 1.0
""")
	write_versioned_function("zombies/feedback/sound_box_poof", f"""
playsound {ns}:zombies/mystery_box/poof ambient @a[scores={{{ns}.zb.in_game=1}}] ~ ~ ~ 1.0 1.0
""")
	write_versioned_function("zombies/feedback/sound_box_land", f"""
playsound {ns}:zombies/mystery_box/land ambient @a[scores={{{ns}.zb.in_game=1}}] ~ ~ ~ 1.0 1.0
""")

	## PAP: Black Ops-style sound effects (positional, distance-limited)
	write_versioned_function("zombies/feedback/sound_pap_knuckle_crack", f"""
playsound {ns}:zombies/pap/knuckle_crack ambient @a[scores={{{ns}.zb.in_game=1}}] ~ ~ ~ 1.0 1.0
""")
	write_versioned_function("zombies/feedback/sound_pap_loop", f"""
playsound {ns}:zombies/pap/pap_loop ambient @a[scores={{{ns}.zb.in_game=1}}] ~ ~ ~ 0.25 1.0
""")
	write_versioned_function("zombies/feedback/sound_pap_dispense", f"""
playsound {ns}:zombies/pap/dispense ambient @a[scores={{{ns}.zb.in_game=1}}] ~ ~ ~ 1.0 1.0
""")
	write_versioned_function("zombies/feedback/sound_pap_upgrade", f"""
playsound {ns}:zombies/pap/upgrade ambient @a[scores={{{ns}.zb.in_game=1}}] ~ ~ ~ 0.5 1.0
""")
	write_versioned_function("zombies/feedback/sound_pap_jingle_sting", f"""
playsound {ns}:zombies/pap/jingle_sting ambient @a[scores={{{ns}.zb.in_game=1}}] ~ ~ ~ 1.0 1.0
""")
	write_versioned_function("zombies/feedback/sound_pap_ready", f"""
playsound {ns}:zombies/pap/ready ambient @a[scores={{{ns}.zb.in_game=1}}] ~ ~ ~ 1.0 1.0
""")
	write_versioned_function("zombies/feedback/sound_pap_retreat_loop", f"""
playsound {ns}:zombies/pap/retreat_loop ambient @a[scores={{{ns}.zb.in_game=1}}] ~ ~ ~ 0.5 1.0
""")
	write_versioned_function("zombies/feedback/sound_pap_power_on", f"""
playsound {ns}:zombies/pap/power_on ambient @a[scores={{{ns}.zb.in_game=1}}] ~ ~ ~ 1.0 1.0
""")
	write_versioned_function("zombies/feedback/sound_pap_deny", f"""
playsound {ns}:zombies/pap/deny ambient @a[scores={{{ns}.zb.in_game=1}}] ~ ~ ~ 1.0 1.0
""")

