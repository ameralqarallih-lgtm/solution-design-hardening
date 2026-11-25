"""Read-only heuristic candidate scanner; not a defect detector. No network or dependencies."""
import argparse, json, re, os
from pathlib import Path
RULES=[('SDP-025',r'\bNOLOCK\b','Check whether this read participates in a correctness invariant.'),('SDP-122',r'Promise\.all\s*\([^\n]*\.map\s*\(','Check whether input size and concurrency are bounded.'),('SDP-065',r'\b(?:auto_ack|autoAck)\s*[:=]\s*(?:true|True)\b','Check acknowledgment timing and delivery requirements.'),('SDP-135',r'\b(?:log|logger|console)\.(?:info|debug|log|error)\s*\([^\n]*(?:password|access_token|authorization)','Check whether sensitive data is logged; do not print its value.'),('SDP-141',r'\.GetAwaiter\(\)\.GetResult\(\)|\bThread\.Sleep\(','Check blocking calls on request or worker paths.')]
SKIP={'.git','node_modules','vendor','bin','obj','.venv','venv','dist','build','__pycache__'}
EXT={'.cs','.java','.ts','.js','.py','.sql','.go','.rb','.yaml','.yml'}
def scan(root):
    for base, dirs, files in os.walk(root,followlinks=False):
        dirs[:]=sorted(d for d in dirs if d not in SKIP and not d.startswith('.') and not (Path(base)/d).is_symlink())
        for f in sorted(files):
            p=Path(base)/f
            if p.is_symlink() or p.suffix not in EXT: continue
            try:
                if p.stat().st_size>1024*1024: continue
                lines=p.read_text(encoding='utf-8').splitlines()
            except (OSError,UnicodeError): continue
            for n,line in enumerate(lines,1):
                for id,pattern,hint in RULES:
                    if re.search(pattern,line,re.I): yield {'problem_id':id,'file':str(p.relative_to(root)),'line':n,'status':'Requires Verification','hint':hint}
if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument('root',type=Path); a=parser.parse_args()
    if not a.root.is_dir(): parser.error('root must be a directory')
    print(json.dumps(list(scan(a.root.resolve())),indent=2))
