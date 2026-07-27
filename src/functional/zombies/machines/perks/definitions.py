""" Every perk's identity, price, description and the teardown that strips its effects. """
# Imports
from dataclasses import dataclass

from ....helpers.scores import SpecialScores
from ....stamina import STAM_MAX
from ...player.revive.shared import SOLO_QR_MAX


# Classes
@dataclass(frozen=True)
class PerkDef:
	""" A perk's identity and the commands that grant and revoke it.

	`{ns}` and `{version}` in the command lists are substituted at generation time.
	"""
	display_name: str
	message: str
	""" Chat feedback on purchase; the leading emoji is split off and rendered uncolored. """
	message_color: str
	text_color: str
	""" Matches the perk MACHINE model's dye color (items.py override_model), and is reused
	everywhere the perk is listed (info paper, perk display items) so the colors stay consistent. """
	commands: tuple[str, ...] = ()
	removal_commands: tuple[str, ...] = ()
	persistent_score: bool = False
	""" Skip the blanket score reset in lose_all — the perk manages its own score (quick_revive). """

# Constants
PERK_DEFINITIONS: dict[str, PerkDef] = {
	"juggernog": PerkDef(
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
	"speed_cola": PerkDef(
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
	"double_tap": PerkDef(
		display_name="Double Tap",
		message="🔥 Double Tap! More damage",
		message_color="gold",
		text_color="yellow",
		commands=(
			"scoreboard players set @s {ns}.special.additional_shots 1",
		),
		removal_commands=(
			"scoreboard players set @s {ns}.special.additional_shots 0",
		),
	),
	"quick_revive": PerkDef(
		display_name="Quick Revive",
		message="💚 Quick Revive! You can revive teammates",
		message_color="aqua",
		text_color="aqua",
		commands=(
			"tag @s add {ns}.perk.quick_revive",
		),
		# Going down strips the active tag, or a doppelganger would auto-revive off a QR they no longer own.
		# The score drops to 0 unless the solo uses are exhausted, where 1 keeps the machine blocked.
		# Hence persistent_score: lose_all must not blanket-reset it.
		removal_commands=(
			"tag @s remove {ns}.perk.quick_revive",
			f"execute unless score @s {{ns}}.zb.qr_uses matches {SOLO_QR_MAX}.. run scoreboard players set @s {{ns}}.zb.perk.quick_revive 0",
		),
		persistent_score=True,
	),
	"mule_kick": PerkDef(
		display_name="Mule Kick",
		message="🎒 Mule Kick! Third weapon slot unlocked",
		message_color="gold",
		text_color="dark_green",
	),
	"stamin_up": PerkDef(
		display_name="Stamin-Up",
		message="🏃 Stamin-Up! Sprint longer, move faster",
		message_color="yellow",
		text_color="gold",
		# BO1 Stamin-Up (zombies/stamina.md): double sprint endurance plus 7% move speed, multiplicative.
		# The stam bump refills the new headroom instantly so the bar doesn't drop at purchase.
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
	"phd_flopper": PerkDef(
		display_name="PhD Flopper",
		message="🧪 PhD Flopper! Immune to explosions & fall damage",
		message_color="dark_purple",
		text_color="dark_purple",
		# Fall damage is nulled by an attribute.
		# Explosive self-damage is gated on the special score in the shared explosion and trap paths.
		commands=(
			"attribute @s minecraft:fall_damage_multiplier base set 0",
			"scoreboard players set @s {ns}.special.phd_flopper 1",
		),
		removal_commands=(
			"attribute @s minecraft:fall_damage_multiplier base reset",
			"scoreboard players set @s {ns}.special.phd_flopper 0",
		),
	),
	"deadshot": PerkDef(
		display_name="Deadshot Daiquiri",
		message="🎯 Deadshot Daiquiri! +Accuracy, -Recoil",
		message_color="dark_green",
		text_color="dark_green",
		# Read in the weapon spread path (raycast.py) and the recoil path (kick.py): both scale to 65%.
		commands=(
			"scoreboard players set @s {ns}.special.deadshot 1",
		),
		removal_commands=(
			"scoreboard players set @s {ns}.special.deadshot 0",
		),
	),
	"timeslip": PerkDef(
		display_name="Timeslip",
		message="⏳ Timeslip! Faster traps & Mystery Box",
		message_color="light_purple",
		text_color="light_purple",
		# Owner-only speed-ups keyed off the special score, x2 by default (no official BO4 number).
		# Pack-a-Punch is x3 instead, because its 300-tick animation is already long.
		# Wired in traps.py (cd x0.75), mystery_box.py (spin x2), pap.py (x3), raycast.py (throw x0.5).
		commands=(
			"scoreboard players set @s {ns}.special.timeslip 1",
		),
		removal_commands=(
			"scoreboard players set @s {ns}.special.timeslip 0",
		),
	),
	"electric_cherry": PerkDef(
		display_name="Electric Cherry",
		message="🍒 Electric Cherry! Reloads discharge a shock",
		message_color="blue",
		text_color="blue",
		# The discharge is wired through the on_reload signal, so the perk only raises the special flag.
		# Shock size scales with how empty the mag was.
		commands=(
			"scoreboard players set @s {ns}.special.electric_cherry 1",
		),
		removal_commands=(
			"scoreboard players set @s {ns}.special.electric_cherry 0",
		),
	),
	"tombstone": PerkDef(
		display_name="Tombstone",
		message="🪦 Tombstone! Recover your gear if you bleed out",
		message_color="yellow",
		text_color="gold",
		# No purchase-time effect: going down spawns a tombstone marker (revive/on_down).
		# Bleeding out gives 60s after the round respawn to walk back and recover perks + weapons.
		# Tombstone itself is excluded, and the whole thing is disabled solo.
	),
	"whos_who": PerkDef(
		display_name="Who's Who",
		message="👥 Who's Who! Play on as a doppelganger when downed",
		message_color="aqua",
		text_color="dark_aqua",
		# No purchase-time effect: going down leaves the owner playing as a doppelganger with a pistol.
		# The body drops as a NORMAL revivable mannequin any alive player, including the owner, can revive.
		# Works solo and outranks solo Quick Revive; see whos_who.py.
	),
	"dying_wish": PerkDef(
		display_name="Dying Wish",
		message="⚔ Dying Wish! Cheat death with a berserk",
		message_color="blue",
		text_color="blue",
		# No purchase-time effect: revive/on_down intercepts to dying_wish_trigger when off cooldown.
		# Ownership is read straight off zb.perk.dying_wish.
	),
	"widows_wine": PerkDef(
		display_name="Widow's Wine",
		message="🕸 Widow's Wine! Web grenades & webbing melee",
		message_color="dark_red",
		text_color="dark_red",
		# The passive web-on-hurt and stronger knife read the special flag directly.
		# The grenade slot is swapped to web grenades by the inventory/replenish paths.
		commands=(
			"scoreboard players set @s {ns}.special.widows_wine 1",
		# Stronger knife while owned (small flat melee bonus, BO3 Widow's Wine melee buff)
			"attribute @s minecraft:attack_damage modifier add {ns}:widows_wine 6 add_value",
			# The widows_wine flag is set above, so loot_replace_lethal routes hotbar.7 to i/web_grenade
			"function {ns}:v{version}/zombies/inventory/loot_replace_lethal",
			"item modify entity @s hotbar.7 {ns}:v{version}/grenade/set_count_2",
			'function {ns}:v{version}/zombies/inventory/apply_slot_tag {slot:"hotbar.7",group:"hotbar",index:7}',
		),
		removal_commands=(
			"scoreboard players set @s {ns}.special.widows_wine 0",
			"attribute @s minecraft:attack_damage modifier remove {ns}:widows_wine",
		),
	),
}

RECOMMENDED_PRICES: dict[str, int] = {
	"juggernog": 2500, "speed_cola": 3000, "double_tap": 2000, "quick_revive": 1500,
	"mule_kick": 4000, "stamin_up": 2000, "phd_flopper": 2000, "deadshot": 1500,
	"timeslip": 1500, "electric_cherry": 2000, "tombstone": 2000, "whos_who": 2000,
	"dying_wish": 2000, "widows_wine": 4000,
}

PERK_DESCRIPTIONS: dict[str, list[str]] = {
	"juggernog": ["Raises your max health to 40 (x4).", "Survive far more hits before going down."],
	"speed_cola": ["Reload all your weapons much faster.", "About twice the reload speed."],
	"double_tap": ["Fires an extra bullet with every shot.", "Roughly doubles your damage output."],
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

	Run at BOTH ends of a game: at stop to hand players back a clean profile, and at start because
	the effects can also arrive from outside zombies entirely — the multiplayer/missions loadout
	perks and the debug menu write the same `special.*` scores, and nothing else clears them for a
	zombies player. Wiping the whole `SpecialScores.ALL` set (not just the ones perks grant) is what
	keeps e.g. a multiplayer Quick Reload class from handing out free Speed Cola in zombies.
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

