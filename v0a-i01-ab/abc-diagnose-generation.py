"""Read-only reproduction of combined inventory derivation failure."""
from pathlib import Path
import importlib.util,os,sys
path=Path.cwd()/'tools/generate_test_inventory.py'
spec=importlib.util.spec_from_file_location('combined_inventory_diagnostic',path)
module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module;spec.loader.exec_module(module)
request=module._GovernanceInventoryPublication(Path.cwd(),Path(os.environ['PONTIUS_GIT']))
module._derive_inventory_publication(request)
