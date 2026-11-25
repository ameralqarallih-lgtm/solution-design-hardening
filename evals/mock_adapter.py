"""Synthetic transport smoke test only; never a coding-agent evaluation."""
import json
from pathlib import Path
if __name__=='__main__':
    assert Path('prompt.txt').is_file()
    print(json.dumps({'response':'SYNTHETIC ADAPTER SMOKE TEST - no model invoked.', 'activation':'unknown'}))
