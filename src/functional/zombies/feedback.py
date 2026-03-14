
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
playsound {ns}:zombies/mystery_box_spin ambient @a[scores={{{ns}.zb.in_game=1}}] ~ ~ ~ 0.9 1.0
""")

	write_versioned_function("zombies/feedback/sound_box_ready", f"""
playsound minecraft:entity.player.levelup ambient @a[scores={{{ns}.zb.in_game=1}}] ~ ~ ~ 0.7 1.2
""")

