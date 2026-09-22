""" The advancement JSON: one tab, three branch roots, and every node under them.

Threshold tiers carry their own condition, so vanilla unlocks them the instant the counter qualifies and
the pack never runs `advancement grant`. That is what removes the companion scores, the unlock ladders
and the admin resync a command-driven version would have needed, and what makes a retune self-healing:
lower a threshold, reload, and everyone who already qualifies unlocks on the next tick.

Event challenges are the exception and use `minecraft:impossible`, so the single grant at their site is
the only way in.

Paths are unversioned. Reward function references are not, because the JSON is rewritten on every build
and always names a function the loaded pack has.
"""
# Imports
from stewbeet import Advancement, Item, JsonDict, Mem, set_json_encoder

from .catalog import BRANCHES, CHAINS, EVENTS, ROOT_PATH, Catalog
from .model import Branch, Chain, EventChallenge

# Constants
ROOT_BACKGROUND: str = "minecraft:block/polished_deepslate"
""" Tab background. A plain identifier resolved as `textures/<path>.png`, not a file path. """
ROOT_ICON: str = "ak47"
""" Item shown on the tab itself. Namespace-free, so it resolves to the pack's own model. """
REVEAL_SUFFIX: str = "reveal"
""" Path suffix of the sentinel closing each chain. See `Tree.write_chain`. """


# Classes
class Tree:
	""" Building the advancement files. Every method returns JSON; nothing here writes a function. """

	# Functions
	@staticmethod
	def icon_json(icon: str) -> JsonDict:
		""" Return the `ItemStackTemplate` for one node's icon.

		A namespaced id is a vanilla item and is used as-is. A bare id is one of the pack's own items, and
		becomes its real base item carrying its `item_model`, so the advancement screen shows the actual
		weapon model rather than the poisonous potato every gun is built on. `Item.from_id` is strict, so a
		mistyped weapon id fails the build instead of rendering as a potato in game.

		Args:
			icon (str): `minecraft:target`, or a pack item id such as `ak47`.
		Returns:
			JsonDict: ex: `{"id": "minecraft:poisonous_potato", "components": {"minecraft:item_model": "mgs:ak47"}}`
		"""
		if ":" in icon:
			return {"id": icon}
		item: Item = Item.from_id(icon)
		return {"id": item.base_item, "components": {"minecraft:item_model": str(item.components["item_model"])}}

	@staticmethod
	def display(title: str, description: str, icon: str, frame: str, hidden: bool = False) -> JsonDict:
		""" Return the display block shared by every node.

		`announce_to_chat` has to be written out: it defaults to true, and the pack prints its own line
		carrying the XP amount, which vanilla's announcement cannot do.

		Args:
			title       (str):  Shown in the toast and on the node.
			description (str):  Shown in the tooltip.
			icon        (str):  Item id.
			frame       (str):  `task`, `goal` or `challenge`.
			hidden      (bool): Whether the node stays invisible until earned.
		Returns:
			JsonDict: The display block.
		"""
		return {
			"icon": Tree.icon_json(icon),
			"title": {"text": title},
			"description": {"text": description},
			"frame": frame,
			"show_toast": True,
			"announce_to_chat": False,
			"hidden": hidden,
		}

	@staticmethod
	def score_criteria(objective: str, threshold: int) -> JsonDict:
		""" Return the criteria block that unlocks when a score reaches a threshold.

		`minecraft:tick` fires once per tick per player and stops being evaluated the moment the
		advancement completes, so the cost decays to zero as a player finishes the tree.

		`player` is a ContextAwarePredicate, which is a LIST of loot conditions. Handing it a bare
		condition object makes it fall through to its alternative branch, which reads the value as an
		EntityPredicate and rejects every key as an unknown entity sub-predicate type. The list is not
		cosmetic.

		Args:
			objective (str): Full objective name, ex: "mgs.adv.zb.kills".
			threshold (int): Minimum value that unlocks it.
		Returns:
			JsonDict: One criterion named `threshold`.
		"""
		return {
			"threshold": {
				"trigger": "minecraft:tick",
				"conditions": {
					"player": {
						"type": "minecraft:entity_scores",
						"entity": "this",
						"scores": {objective: {"min": threshold}},
					},
				},
			}
		}

	@staticmethod
	def write(path: str, advancement: JsonDict) -> None:
		""" Register one advancement file at an unversioned path.

		Args:
			path        (str):      Path under the namespace, ex: "challenges/zb/kills_2".
			advancement (JsonDict): The whole file.
		"""
		Mem.ctx.data[Mem.ctx.project_id].advancements[path] = set_json_encoder(Advancement(advancement), max_level=-1)

	@staticmethod
	def write_roots() -> None:
		""" Write the tab root and the three branch roots.

		All four are unconditioned `tick` criteria, so they complete on a player's first tick and every
		chain's first tier is visible immediately. A tab is one parentless advancement, which is why the
		branches are children rather than roots of their own.
		"""
		Tree.write(f"{ROOT_PATH}/root", {
			"display": {
				**Tree.display(
					title=Mem.ctx.project_name,
					description="Challenges across every mode. Each one pays XP",
					icon=ROOT_ICON,
					frame="task",
				),
				"background": ROOT_BACKGROUND,
				"show_toast": False,
			},
			"criteria": {"joined": {"trigger": "minecraft:tick"}},
		})

		for branch in BRANCHES:
			Tree.write_branch_root(branch)

	@staticmethod
	def write_branch_root(branch: Branch) -> None:
		""" Write one branch sub-root.

		Args:
			branch (Branch): The branch.
		"""
		Tree.write(f"{ROOT_PATH}/{branch.key}/root", {
			"parent": f"{Mem.ctx.project_id}:{ROOT_PATH}/root",
			"display": {
				**Tree.display(branch.title, branch.description, branch.icon, frame="task"),
				"show_toast": False,
			},
			"criteria": {"joined": {"trigger": "minecraft:tick"}},
		})

	@staticmethod
	def write_chain(chain: Chain) -> None:
		""" Write every tier of one chain, parented in order, and the sentinel that reveals it.

		Args:
			chain (Chain): The chain.
		"""
		ns: str = Mem.ctx.project_id
		version: str = Mem.ctx.project_version
		parent: str = f"{ns}:{ROOT_PATH}/{chain.branch}/root"

		for index, tier in enumerate(chain.tiers):
			path: str = Catalog.tier_path(chain, index)
			Tree.write(path, {
				"parent": parent,
				"display": Tree.display(
					tier.title, chain.description_of(index), chain.icon_of(index), chain.frame_of(index), tier.hidden,
				),
				"criteria": Tree.score_criteria(chain.stat.objective, tier.threshold),
				"rewards": {"function": f"{ns}:v{version}/progression/adv/{chain.branch}/{chain.key}/reward_{index + 1}"},
			})
			parent = f"{ns}:{path}"

		## Without this, a fresh player sees only the first two tiers of every chain. Vanilla shows an
		## unfinished node only if it or one of its two nearest ancestors is done, so tier 3 and beyond are
		## invisible and nobody can find out what they are chasing.
		## A node with no `display` is never rendered, but `AdvancementVisibilityEvaluator` still ORs its
		## done-ness into every ancestor, so hanging one completed sentinel off the last tier lights up the
		## whole chain. It is granted by an unconditioned tick, pays nothing and says nothing.
		Tree.write(f"{ROOT_PATH}/{chain.branch}/{chain.key}_{REVEAL_SUFFIX}", {
			"parent": parent,
			"criteria": {"joined": {"trigger": "minecraft:tick"}},
		})

	@staticmethod
	def write_event(event: EventChallenge) -> None:
		""" Write one event challenge, unreachable except by command.

		Args:
			event (EventChallenge): The challenge.
		"""
		ns: str = Mem.ctx.project_id
		version: str = Mem.ctx.project_version
		Tree.write(Catalog.event_path(event), {
			"parent": f"{ns}:{ROOT_PATH}/{event.branch}/root",
			"display": Tree.display(event.title, event.description, event.icon, event.frame, event.hidden),
			"criteria": {"granted": {"trigger": "minecraft:impossible"}},
			"rewards": {"function": f"{ns}:v{version}/progression/adv/{event.branch}/reward_{event.key}"},
		})

	@staticmethod
	def write_all() -> None:
		""" Write the tab, the branches, every chain and every event challenge. """
		Tree.write_roots()
		for chain in CHAINS:
			Tree.write_chain(chain)
		for event in EVENTS:
			Tree.write_event(event)
