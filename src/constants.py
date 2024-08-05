from pathlib import Path

MAIN_DOC_URL = "https://docs.python.org/3/"
PEP_DOC_URL = "https://peps.python.org/"
BASE_DIR = Path(__file__).parent
DATETIME_FORMAT = "%Y-%m-%d_%H-%M-%S"
EXPECTED_STATUS = {
    "A": ("Active", "Accepted"),
    "D": ("Deferred",),
    "F": ("Final",),
    "P": ("Provisional",),
    "R": ("Rejected",),
    "S": ("Superseded",),
    "W": ("Withdrawn",),
    "": ("Draft", "Active"),
}
NUMBER_OF_PEP = {
    ("Active", "Accepted"): 0,
    ("Deferred",): 0,
    ("Final",): 0,
    ("Provisional",): 0,
    ("Rejected",): 0,
    ("Superseded",): 0,
    ("Withdrawn",): 0,
    ("Draft", "Active"): 0,
}
