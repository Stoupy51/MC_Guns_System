""" Every perk's identity, price, description and the teardown that strips its effects. """
# Imports
import os
from dataclasses import dataclass

from stewbeet import Mem

from ....helpers.scores import SpecialScores
from ....stamina import STAM_MAX


# Classes
@dataclass(frozen=True)
class PerkDef:
	""" A perk's identity and the commands that grant and revoke it.

	`{ns}` and `{version}` in the command lists are substituted at generation time.
	"""
	perk_id: str
	""" Scoreboard, function and sound name; also the key PERK_DEFINITIONS is built on. """
	display_name: str
	message: str
	""" Chat feedback on purchase; the leading emoji is split off and rendered uncolored. """
	message_color: str
	text_color: str
	""" The dye colour of the perk machine model (items override_model).
	Reused wherever the perk is listed (info paper, perk display items).
	"""
	commands: tuple[str, ...] = ()
	removal_commands: tuple[str, ...] = ()

	@property
	def has_song(self) -> bool:
		""" Whether the perk's purchase jingle exists, so apply/<perk_id> plays it.

		Read off the .ogg itself rather than a hand-set flag: dropping a clip into the sounds folder is
		then the only thing a perk still missing its jingle needs. A perk without one stays silent
		instead of asking for a sound the resource pack never registered.
		"""
		sounds_folder: str = Mem.ctx.meta.get("stewbeet", {}).get("sounds", {}).get("folder", "")
		return os.path.isfile(f"{sounds_folder}/zombies/perks/{self.perk_id}.ogg")

# Constants
PERK_DEFINITIONS: dict[str, PerkDef] = {perk.perk_id: perk for perk in [
	PerkDef(
		perk_id="juggernog",
		display_name="Juggernog",
		message="🍺 Juggernog! Max HP: 40",
		message_color="dark_red",
		text_color="red",
		commands=(
			"attribute @s minecraft:max_health base set 40",
		),
		removal_commands=(
			"attribute @s minecraft:max_health base reset",
		),
	),
	PerkDef(
		perk_id="speed_cola",
		display_name="Speed Cola",
		message="⚡ Speed Cola! Faster reload",
		message_color="green",
		text_color="green",
		commands=(
			"scoreboard players set @s {ns}.special.quick_reload 50",
		),
		removal_commands=(
			"scoreboard players set @s {ns}.special.quick_reload 0",
		),
	),
	PerkDef(
		perk_id="double_tap",
		display_name="Double Tap",
		message="🔥 Double Tap! More damage",
		message_color="gold",
		text_color="yellow",
		commands=(
			"scoreboard players set @s {ns}.special.double_tap 1",
		),
		removal_commands=(
			"scoreboard players set @s {ns}.special.double_tap 0",
		),
	),
	PerkDef(
		perk_id="quick_revive",
		display_name="Quick Revive",
		message="💚 Quick Revive! You can revive teammates",
		message_color="aqua",
		text_color="aqua",
		commands=(
			"tag @s add {ns}.perk.quick_revive",
		),
		# Going down strips the active tag, or a doppelganger would auto-revive off a Quick Revive they lost.
		# The score only means ownership; {ns}.zb.qr_uses blocks rebuys after the solo uses (perks/on_right_click).
		removal_commands=(
			"tag @s remove {ns}.perk.quick_revive",
		),
	),
	PerkDef(
		perk_id="mule_kick",
		display_name="Mule Kick",
		message="🎒 Mule Kick! Third weapon slot unlocked",
		message_color="gold",
		text_color="dark_green",
	),
	PerkDef(
		perk_id="stamin_up",
		display_name="Stamin-Up",
		message="🏃 Stamin-Up! Sprint longer, move faster",
		message_color="yellow",
		text_color="gold",
		# BO1 Stamin-Up: double sprint endurance and +7% move speed (multiplicative); the stam bump fills the new headroom at once.
		commands=(
			"attribute @s minecraft:movement_speed modifier add {ns}:stamin_up 0.07 add_multiplied_total",
			f"scoreboard players set @s {{ns}}.stam_bonus {STAM_MAX}",
			f"scoreboard players add @s {{ns}}.stam {STAM_MAX}",
		),
		removal_commands=(
			"attribute @s minecraft:movement_speed modifier remove {ns}:stamin_up",
			"scoreboard players set @s {ns}.stam_bonus 0",
		),
	),
	PerkDef(
		perk_id="phd_flopper",
		display_name="PhD Flopper",
		message="🧪 PhD Flopper! Immune to explosions & fall damage",
		message_color="dark_purple",
		text_color="dark_purple",
		# Fall damage is nulled by an attribute; explosive self-damage reads the special score (explosion and trap paths).
		commands=(
			"attribute @s minecraft:fall_damage_multiplier base set 0",
			"scoreboard players set @s {ns}.special.phd_flopper 1",
		),
		removal_commands=(
			"attribute @s minecraft:fall_damage_multiplier base reset",
			"scoreboard players set @s {ns}.special.phd_flopper 0",
		),
	),
	PerkDef(
		perk_id="deadshot",
		display_name="Deadshot Daiquiri",
		message="🎯 Deadshot Daiquiri! +Accuracy, -Recoil",
		message_color="dark_green",
		text_color="dark_green",
		# Read by the spread (raycast) and recoil (kick) paths: both scale to 65%.
		commands=(
			"scoreboard players set @s {ns}.special.deadshot 1",
		),
		removal_commands=(
			"scoreboard players set @s {ns}.special.deadshot 0",
		),
	),
	PerkDef(
		perk_id="timeslip",
		display_name="Timeslip",
		message="⏳ Timeslip! Faster traps & Mystery Box",
		message_color="light_purple",
		text_color="light_purple",
		# Owner-only speed-ups, x2 by default (no official BO4 number), x3 for Pack-a-Punch whose animation is long.
		# Read by traps (cooldown x0.75), mystery_box (spin x2), pap (x3) and raycast (throw x0.5).
		commands=(
			"scoreboard players set @s {ns}.special.timeslip 1",
		),
		removal_commands=(
			"scoreboard players set @s {ns}.special.timeslip 0",
		),
	),
	PerkDef(
		perk_id="electric_cherry",
		display_name="Electric Cherry",
		message="🍒 Electric Cherry! Reloads discharge a shock",
		message_color="blue",
		text_color="blue",
		# The discharge runs from the on_reload signal; its size scales with how empty the magazine was.
		commands=(
			"scoreboard players set @s {ns}.special.electric_cherry 1",
		),
		removal_commands=(
			"scoreboard players set @s {ns}.special.electric_cherry 0",
		),
	),
	PerkDef(
		perk_id="tombstone",
		display_name="Tombstone",
		message="🪦 Tombstone! Recover your gear if you bleed out",
		message_color="yellow",
		text_color="gold",
		# No purchase effect: going down spawns a tombstone (revive/on_down); see perks/tombstone.
	),
	PerkDef(
		perk_id="whos_who",
		display_name="Who's Who",
		message="👥 Who's Who! Play on as a doppelganger when downed",
		message_color="aqua",
		text_color="dark_aqua",
		# No purchase effect: going down leaves the owner playing as a doppelganger; see whos_who.
	),
	PerkDef(
		perk_id="dying_wish",
		display_name="Dying Wish",
		message="⚔ Dying Wish! Cheat death with a berserk",
		message_color="blue",
		text_color="blue",
		# No purchase effect: revive/on_down triggers it when off cooldown.
	),
	PerkDef(
		perk_id="widows_wine",
		display_name="Widow's Wine",
		message="🕸 Widow's Wine! Web grenades & webbing melee",
		message_color="dark_red",
		text_color="dark_red",
		# Web-on-hurt and the knife bonus read the special flag; the replenish paths swap the grenade slot to webs.
		commands=(
			"scoreboard players set @s {ns}.special.widows_wine 1",
		# Small flat melee bonus (BO3).
			"attribute @s minecraft:attack_damage modifier add {ns}:widows_wine 6 add_value",
			# The flag above makes loot_replace_lethal give web grenades.
			"function {ns}:v{version}/zombies/inventory/loot_replace_lethal",
			"item modify entity @s hotbar.7 {ns}:v{version}/grenade/set_count_2",
			'function {ns}:v{version}/zombies/inventory/apply_slot_tag {slot:"hotbar.7",group:"hotbar",index:7}',
		),
		removal_commands=(
			"scoreboard players set @s {ns}.special.widows_wine 0",
			"attribute @s minecraft:attack_damage modifier remove {ns}:widows_wine",
		),
	),
]}

TOMBSTONE_PERKS: list[str] = [pid for pid in PERK_DEFINITIONS if pid != "tombstone"]
""" Perks a tombstone gives back: itself excluded (Black Ops rule), it must be rebought. """

RECOMMENDED_PRICES: dict[str, int] = {
	"juggernog": 2500, "speed_cola": 3000, "double_tap": 2000, "quick_revive": 1500,
	"mule_kick": 4000, "stamin_up": 2000, "phd_flopper": 2000, "deadshot": 1500,
	"timeslip": 1500, "electric_cherry": 2000, "tombstone": 2000, "whos_who": 2000,
	"dying_wish": 2000, "widows_wine": 4000,
}

PERK_DESCRIPTIONS: dict[str, list[str]] = {
	"juggernog": ["Raises your max health to 40 (x4).", "Survive far more hits before going down."],
	"speed_cola": ["Reload all your weapons much faster.", "About twice the reload speed."],
	"double_tap": ["Every bullet deals double damage."],
	"quick_revive": ["Revive downed teammates faster.", "Solo: revives you after you go down."],
	"mule_kick": ["Carry a third weapon.", "Unlocks an extra weapon slot."],
	"stamin_up": ["Move faster and sprint for longer.", "+7% move speed, double sprint endurance."],
	"phd_flopper": ["Immune to fall and self-explosive damage.", "Dive to prone to set off a blast."],
	"deadshot": ["Aim snaps toward zombie heads.", "Tighter hipfire spread and less recoil."],
	"timeslip": ["Machines and power-ups spin faster.", "Pack-a-Punch, box & Wunderfizz speed up.", "Grenades throw on a shorter cooldown."],
	"electric_cherry": ["Reloading discharges a shockwave.", "Damages and stuns nearby zombies.", "Stronger the emptier your magazine."],
	"tombstone": ["If you bleed out, leave a Tombstone.", "Return to it the next round to recover", "your perks and full inventory."],
	"whos_who": ["When downed, fight on as a clone.", "Revive your own body to fully recover.", "Works solo or co-op."],
	"dying_wish": ["Cheat death when you would go down.", "Brief berserk (resistance & strength),", "then drop to 1 HP. Long cooldown."],
	"widows_wine": ["Grenades become sticky web grenades.", "Being hit bursts webbing around you.", "Stronger melee knife."],
}

# Functions
def perk_effects_teardown(ns: str, selector: str) -> str:
	""" Return the lines stripping every effect a zombies perk can leave on a player.

	Run at both ends of a game: at stop to hand back a clean profile, and at start because the effects can come from outside zombies.
	Multiplayer and missions loadout perks and the debug menu write the same `special.*` scores.
	Wiping all of `SpecialScores.ALL` keeps, for example, a multiplayer Quick Reload class from granting a free Speed Cola in zombies.
	"""
	return f"""
execute as {selector} run attribute @s minecraft:max_health base reset
execute as {selector} run attribute @s minecraft:movement_speed modifier remove {ns}:stamin_up
execute as {selector} run attribute @s minecraft:fall_damage_multiplier base reset
execute as {selector} run attribute @s minecraft:attack_damage modifier remove {ns}:widows_wine
execute as {selector} run attribute @s minecraft:attack_damage modifier remove {ns}:dying_wish
tag {selector} remove {ns}.dying_wish_active
scoreboard players set {selector} {ns}.zb.dw_uses 0
scoreboard players set {selector} {ns}.zb.dw_cd 0
scoreboard players set {selector} {ns}.zb.dw_timer 0
scoreboard players set {selector} {ns}.stam_bonus 0
tag {selector} remove {ns}.perk.speed_cola
tag {selector} remove {ns}.perk.double_tap
tag {selector} remove {ns}.perk.quick_revive
{SpecialScores.reset_special_scores_lines(ns, selector)}
""".strip()

