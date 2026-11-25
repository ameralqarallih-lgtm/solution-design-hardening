"""Read-only, line-based risk candidate scanner. Not a defect detector or language parser."""
import argparse, json, re, os, stat
from pathlib import Path
# Stable rule names allow several patterns to map to one catalog entry.
# Language/format gating reduces obvious cross-language false positives.
RULES = [
 ('dirty-read','SDP-025',r'\bNOLOCK\b|\bREAD\s+UNCOMMITTED\b','Check whether this read participates in a correctness invariant.',{'.sql','.cs','.java'}),
 ('fanout-map','SDP-122',r'Promise\.all\s*\([^\n]*\.map\s*\(','Check whether input size and concurrency are bounded.',{'.js','.ts','.jsx','.tsx'}),
 ('auto-ack','SDP-065',r'\b(?:auto_ack|autoAck)\s*[:=]\s*(?:true|True)\b','Check acknowledgment timing and delivery requirements.',{'.py','.js','.ts','.cs','.java','.yaml','.yml'}),
 ('sensitive-log','SDP-135',r'\b(?:log|logger|console)\.(?:info|debug|log|error|warning)\s*\([^\n]*(?:password|access_token|authorization)','Check whether sensitive data is logged; do not print its value.',None),
 ('blocking-dotnet','SDP-141',r'\.GetAwaiter\(\)\.GetResult\(\)|\bThread\.Sleep\(','Check blocking calls on request or worker paths.',{'.cs'}),
 ('unbounded-queue','SDP-044',r'\b(?:CreateUnbounded\s*(?:<[^>]+>)?\s*\(|asyncio\.Queue\(\s*(?:maxsize\s*=\s*0)?\s*\)|new\s+LinkedBlockingQueue\s*<[^>]*>\s*\(\s*\))','Verify producer admission, queue bounds and overflow behavior.',{'.cs','.py','.java'}),
 ('no-http-timeout','SDP-042',r'\btimeout\s*=\s*None\b|\bTimeout\.InfiniteTimeSpan\b','Check caller deadline, cancellation and resource bounds.',{'.py','.cs'}),
 ('unlimited-prefetch','SDP-044',r'\b(?:prefetch_count|prefetchCount)\s*[:=]\s*0\b|\.prefetch\(\s*0\s*\)','Verify whether unlimited prefetch is intentional and consumer memory is bounded.',{'.py','.js','.ts','.yaml','.yml','.cs'}),
 ('requeue-always','SDP-057',r'\b(?:basic_nack|basic_reject)\s*\([^\n]*requeue\s*=\s*True\b|\.nack\([^\n]*,\s*true\s*\)','Check poison-message handling, attempt limits and redrive.',{'.py','.js','.ts'}),
 ('process-lock','SDP-030',r'\b(?:threading\.Lock|asyncio\.Lock|SemaphoreSlim|ReentrantLock)\s*\(','Check whether this lock protects shared cross-instance state; process-local locks may be sufficient for local state.',{'.py','.cs','.java'}),
 ('runtime-migration','SDP-140',r'\.Database\.Migrate(?:Async)?\s*\(|\bsequelize\.sync\s*\(','Check replica startup paths and migration ownership; framework migration locking may already protect execution.',{'.cs','.js','.ts'}),
 ('force-schema-sync','SDP-138',r'\.sync\s*\([^\n]*\b(?:force|alter)\s*:\s*true\b','If used in schema synchronization, verify data safety and mixed-version compatibility.',{'.js','.ts'}),
 ('floating-image','SDP-137',r'^\s*image\s*:\s*[\'\"]?[^\s\'\"#]+:latest(?:[\s\'\"#]|$)','Check whether deployment pins a verified immutable artifact elsewhere.',{'.yaml','.yml'}),
 ('short-termination','SDP-117',r'\bterminationGracePeriodSeconds\s*:\s*[0-5]\b','Compare drain, shutdown, commit and acknowledgment deadlines; a short grace can be intentional.',{'.yaml','.yml'}),
 ('unbounded-metric-label','SDP-146',r'\b(?:WithLabels|labels|WithLabelValues)\s*\([^\n]*(?:user_id|userId|request_id|requestId|trace_id|traceId)','Check metric dimension cardinality and whether values are bounded.',{'.cs','.py','.go','.java','.js','.ts'}),
 ('blind-offset-commit','SDP-065',r'\b(?:enable_auto_commit|enable\.auto\.commit|enableAutoCommit)\s*[\'\"]?\s*[:=]\s*(?:true|True)\b','Verify offset commit timing against durable effect and client semantics.',{'.py','.js','.ts','.java','.yaml','.yml','.properties'}),
 ('infinite-retry','SDP-087',r'\b(?:RetryForever(?:Async)?|WaitAndRetryForever(?:Async)?)\s*\(','Check outer deadline, cancellation and retry budget.',{'.cs'}),
]
# Do not inspect arbitrary secret/config files or generated content.
SKIP={'.git','node_modules','vendor','bin','obj','.venv','venv','dist','build','__pycache__','target','coverage'}
EXT={'.cs','.java','.ts','.js','.jsx','.tsx','.py','.sql','.go','.rb','.yaml','.yml','.properties','.rs','.php','.kt'}
COMPILED=[(name,pid,re.compile(pattern,re.I),hint,suffixes) for name,pid,pattern,hint,suffixes in RULES]

def scan(root):
    root=Path(root).resolve()
    for base, dirs, files in os.walk(root,followlinks=False):
        dirs[:]=sorted(d for d in dirs if d not in SKIP and not d.startswith('.') and not (Path(base)/d).is_symlink())
        for f in sorted(files):
            p=Path(base)/f
            suffix=p.suffix.lower()
            if f.startswith('.') or re.search(r'(^|[._-])(secrets?|credentials?|private[-_]key|env)([._-]|$)',f,re.I): continue
            if p.is_symlink() or suffix not in EXT: continue
            try:
                info=p.stat()
                if not stat.S_ISREG(info.st_mode) or info.st_size>1024*1024: continue
                lines=p.read_text(encoding='utf-8').splitlines()
            except (OSError,UnicodeError): continue
            for n,line in enumerate(lines,1):
                for name,pid,pattern,hint,suffixes in COMPILED:
                    if (suffixes is None or suffix in suffixes) and pattern.search(line):
                        yield {'rule_id':name,'problem_id':pid,'file':p.relative_to(root).as_posix(),'line':n,'status':'Requires Verification','hint':hint}
if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument('root',type=Path); a=parser.parse_args()
    if not a.root.is_dir(): parser.error('root must be a directory')
    print(json.dumps(list(scan(a.root)),indent=2))
