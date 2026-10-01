""" Upload the built zips to a GitHub release, using the credentials in ~/stewbeet/credentials.yml. """
# pyright: reportUnknownVariableType=false
# Imports
from beet import ProjectConfig
from stewbeet import JsonDict
from stewbeet.continuous_delivery import load_credentials, upload_to_github
from stewbeet.utils import get_project_config

# Get credentials and the beet configuration
credentials: dict[str, str] = load_credentials("~/stewbeet/credentials.yml")
cfg: ProjectConfig = get_project_config()

# Upload to GitHub
github_config: JsonDict = {
	"project_name": "MC_Guns_System",
	"version": cfg.version,
	"build_folder": cfg.output,
	"endswith": [".zip"]
}
upload_to_github(credentials, github_config)

