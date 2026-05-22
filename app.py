import importlib.util
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
PROTOTYPE_DIR = ROOT_DIR / "prototype"
PROTOTYPE_APP = PROTOTYPE_DIR / "app.py"

if str(PROTOTYPE_DIR) not in sys.path:
    sys.path.insert(0, str(PROTOTYPE_DIR))

spec = importlib.util.spec_from_file_location("prototype_app", PROTOTYPE_APP)
if spec is None or spec.loader is None:
    raise ImportError(f"Could not load prototype app from {PROTOTYPE_APP}")

prototype_app = importlib.util.module_from_spec(spec)
sys.modules["prototype_app"] = prototype_app
spec.loader.exec_module(prototype_app)

app = prototype_app.app
