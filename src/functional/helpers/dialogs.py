""" Registering a dialog and the buttons that open or run things from one. """
# Imports
import json
from typing import Any

from stewbeet import Dialog, Mem, TextComponent, set_json_encoder, write_versioned_function
from stouputils.typing import JsonDict

from .text import Text


# Classes
class Dialogs:
	""" Registering a dialog and the buttons that open or run things from one. """

	# Functions
	@staticmethod
	def btn(label: str, command: str, color: str = "yellow", hover: str = "", action: str = "suggest_command") -> str:
		""" Create a clickable button JSON component.

		Args:
			label     (str): The text to display on the button.
			command   (str): The command to run when the button is clicked.
			color     (str): The color of the button text.
			hover     (str): Optional tooltip text to show when hovering over the button.
			action    (str): The click event action type (default: "suggest_command").
		"""
		obj: TextComponent = [
			{"text": "[", "color": color, "click_event": {"action": action, "command": command}},
			label,
			"]",
		]
		if hover:
			obj[0]["hover_event"] = {"action": "show_text", "value": hover}
		return json.dumps(obj)

	@staticmethod
	def dialog_function(dialog_id: str) -> str:
		""" Return the versioned function path that opens the dialog for dialog_id.

		Kept so existing `/function <ns>:v<version>/dialogs/<id>` entry points (menu items, commands)
		still work; the function is now a one-liner that shows the registered dialog resource.
		"""
		return f"{Mem.ctx.project_id}:v{Mem.ctx.project_version}/dialogs/{dialog_id}"

	@staticmethod
	def dialog_ref(dialog_id: str) -> str:
		""" Return the resource id of a registered dialog, e.g. "mgs:v5.1.0/config".

		This is what `minecraft:show_dialog` actions point at. Navigating between menus through
		show_dialog rather than a run_command matters for more than tidiness: a run_command button
		makes the client ask the player to confirm running the command every single time.
		"""
		return f"{Mem.ctx.project_id}:v{Mem.ctx.project_version}/{dialog_id}"

	@staticmethod
	def register_dialog(dialog_id: str, data: JsonDict, wrapper: bool = True) -> None:
		""" Register a dialog as a real dialog resource under `data/<ns>/dialog/v<version>/<id>.json`.

		A thin `dialogs/<dialog_id>` function is written alongside it so every existing
		`/function .../dialogs/<id>` entry point keeps working. Note that dialog resources are loaded
		at datapack load, so editing one needs a `/reload` to take effect — unlike the inline SNBT
		form this replaces, which was rebuilt into the command every time.

		Args:
			dialog_id (str): Path within the namespace, e.g. "config" or "multiplayer/setup".
			data      (dict): The dialog structure.
			wrapper   (bool): Also write the `dialogs/<id>` opener function. Pass False when the dialog
				is only ever shown from a function that has its own guards to run first.
		"""
		ns: str = Mem.ctx.project_id
		version: str = Mem.ctx.project_version
		Mem.ctx.data[ns].dialogs[f"v{version}/{dialog_id}"] = set_json_encoder(Dialog(data))
		if wrapper:
			write_versioned_function(f"dialogs/{dialog_id}", f"dialog show @s {Dialogs.dialog_ref(dialog_id)}")

	@staticmethod
	def dialog_back_action(dialog_id: str, label: str = "◀ Back", tooltip: str = "Return to the previous menu") -> JsonDict:
		""" The `exit_action` entry that returns to another registered dialog without a confirm prompt. """
		return {
			"label": Text.split_emoji(label, color="gray"),
			"tooltip": {"text": tooltip},
			"action": {"type": "minecraft:show_dialog", "dialog": Dialogs.dialog_ref(dialog_id)},
		}

	@staticmethod
	def dialog_show_btn(dialog_reference: str, label: str, hover: str, color: str | None = None) -> JsonDict:
		""" A dialog action button that opens another registered dialog directly via show_dialog. """
		label_component: Any = Text.split_emoji(label, color=color) if color else Text.split_emoji(label)
		dialog_id: str = dialog_reference.split(":", 1)[-1]
		return {"label": label_component, "tooltip": {"text": hover}, "action": {"type": "minecraft:show_dialog", "dialog": Dialogs.dialog_ref(dialog_id)}}

	@staticmethod
	def dialog_run_btn(label: str, command: str, hover: str, color: str = "green") -> JsonDict:
		""" A dialog action button that runs a command as the clicking player via run_command. """
		return {"label": Text.split_emoji(label, color=color), "tooltip": {"text": hover}, "action": {"type": "run_command", "command": command}}

	@staticmethod
	def register_value_picker(dialog_id: str, title: str, desc: str, options: list[tuple[str, str, str, str]], back_dialog: str) -> None:
		""" Register a sub-dialog whose buttons each apply one value, then a Back button returns to back_dialog.

		Each value button is independent (no submit step), so opening the picker never resets untouched
		settings. after_action "none" keeps the picker open after a pick (requires pause=false).

		Args:
			dialog_id   (str): Path within the namespace for this picker.
			title       (str): Dialog title text.
			desc        (str): Short body description.
			options     (list): (label, command, color, hover) tuples, one per value button.
			back_dialog (str): Path within the namespace of the dialog the Back button returns to.
		"""
		actions: list[JsonDict] = [{
			"label": {"text": label, "color": color},
			"tooltip": {"text": hover},
			"action": {"type": "run_command", "command": command},
		} for label, command, color, hover in options]
		Dialogs.register_dialog(dialog_id, {
			"type": "minecraft:multi_action",
			"title": {"text": title, "color": "gold", "bold": True},
			"body": [{"type": "minecraft:plain_message", "contents": {"text": desc, "color": "gray"}}],
			"actions": actions,
			# Value pickers list options of a single setting (all the same kind) → one column reads cleaner.
			"columns": 1,
			"pause": False,
			"after_action": "none",
			"exit_action": Dialogs.dialog_back_action(back_dialog),
		})

