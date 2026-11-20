"""Record the small shared reporting environment, separate from locked environments for case runs."""
import importlib.metadata as meta,json,platform,sys
from pathlib import Path
R=Path(__file__).resolve().parent
pkgs=['beautifulsoup4','Markdown','pandas','numpy','requests','scikit-learn','PyMuPDF','websocket-client','pyarrow']
d=dict(python=sys.version.split()[0],os=platform.system()+' '+platform.release(),packages={p:meta.version(p) for p in pkgs},browser='Chrome headless via CDP',case_environments='Each experiment retains its own version evidence, independently of the reporting interpreter.')
(R/'state/environment.json').write_text(json.dumps(d,indent=2),'utf8')

