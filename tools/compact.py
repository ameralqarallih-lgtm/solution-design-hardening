"""Compact, line-oriented rendering of tool JSON for agent context. Python 3 standard library."""
import json


def _value(v):
    if isinstance(v, (dict, list)):
        return json.dumps(v, separators=(',', ':'), ensure_ascii=False)
    return str(v)


def _item(d):
    return ' '.join(f'{k}={_value(v)}' for k, v in d.items() if v not in (None, '', [], {}))


def render(data, prefix=''):
    """One line per scalar, per list item and per nested key; drops empty values. Nothing is truncated."""
    lines = []
    if isinstance(data, list):
        lines.append(f'{prefix or "items"}: {len(data)}')
        for x in data:
            lines.append('- ' + (_item(x) if isinstance(x, dict) else _value(x)))
        return lines
    for k, v in data.items():
        key = f'{prefix}{k}'
        if isinstance(v, dict):
            if v and all(not isinstance(x, (dict, list)) for x in v.values()):
                lines.append(f'{key}: {_item(v)}')
            elif v:
                lines.extend(render(v, key + '.'))
        elif isinstance(v, list):
            if v:
                lines.extend(render(v, key))
        elif v not in (None, ''):
            lines.append(f'{key}: {v}')
    return lines


def emit(data, compact):
    print('\n'.join(render(data)) if compact else json.dumps(data, indent=2))
