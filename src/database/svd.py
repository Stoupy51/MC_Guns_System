
# Imports
from ..config.stats import SVD, add_item


# Main function should return a database
def main() -> None:

    # Add svd
    add_item("svd", stats=SVD, model_path="auto")
    add_item("svd_zoom", stats=SVD, model_path="auto")
    add_item("svd_1", stats=SVD, model_path="auto")
    add_item("svd_1_zoom", stats=SVD, model_path="auto")
    add_item("svd_2", stats=SVD, model_path="auto")
    add_item("svd_2_zoom", stats=SVD, model_path="auto")
    add_item("svd_3", stats=SVD, model_path="auto")
    add_item("svd_3_zoom", stats=SVD, model_path="auto")
    add_item("svd_4", stats=SVD, model_path="auto")
    add_item("svd_4_zoom", stats=SVD, model_path="auto")

