#!/usr/bin/env python3
"""Compare current OpenAPI spec vs an older one and output structural metrics.

Usage:
  python diff_specs.py --current sdk/openapi.json --old dev-tools/local-debug/old-openapi.json

Metrics reported:
 - File size (bytes), line count
 - openapi version, info.version, description length
 - server count, tag count
 - path count, operation count
 - schema count, total schema property count
 - counts of anyOf/oneOf/allOf occurrences
 - count of decimal format fields
 - longest operation description length
 - list of added/removed top-level path keys
"""
import argparse
import json
from pathlib import Path
from typing import Dict, Any, Iterable


def load(path: Path) -> Dict[str, Any]:
    with path.open('r', encoding='utf-8') as f:
        return json.load(f)


def file_stats(path: Path):
    text = path.read_text(encoding='utf-8')
    return {
        'bytes': path.stat().st_size,
        'lines': text.count('\n') + 1
    }


def iter_schemas(root: Dict[str, Any]) -> Iterable[Dict[str, Any]]:
    comps = root.get('components', {})
    schemas = comps.get('schemas', {})
    for schema in schemas.values():
        yield schema


def walk(node: Any):
    if isinstance(node, dict):
        yield node
        for v in node.values():
            yield from walk(v)
    elif isinstance(node, list):
        for item in node:
            yield from walk(item)


def collect_metrics(spec: Dict[str, Any], path: Path):
    stats = file_stats(path)
    info = spec.get('info', {})
    description = info.get('description', '') or ''
    servers = spec.get('servers', [])
    tags = spec.get('tags', [])
    paths = spec.get('paths', {})
    operations = 0
    for p in paths.values():
        if isinstance(p, dict):
            for method in p.keys():
                if method.lower() in {'get', 'post', 'put', 'delete', 'patch', 'options', 'head'}:
                    operations += 1

    schemas = list(iter_schemas(spec))
    schema_property_count = 0
    for s in schemas:
        if isinstance(s, dict) and 'properties' in s and isinstance(s['properties'], dict):
            schema_property_count += len(s['properties'])

    any_of = one_of = all_of = decimal_fmt = 0
    longest_op_desc = 0
    for node in walk(spec):
        if 'anyOf' in node:
            any_of += 1
        if 'oneOf' in node:
            one_of += 1
        if 'allOf' in node:
            all_of += 1
        if node.get('format') == 'decimal':
            decimal_fmt += 1
        # operation description heuristic
        if 'description' in node and isinstance(node['description'], str):
            dlen = len(node['description'])
            if dlen > longest_op_desc:
                longest_op_desc = dlen

    return {
        'file_bytes': stats['bytes'],
        'file_lines': stats['lines'],
        'openapi_version': spec.get('openapi'),
        'info_version': info.get('version'),
        'info_description_length': len(description),
        'servers_count': len(servers),
        'tags_count': len(tags),
        'paths_count': len(paths),
        'operations_count': operations,
        'schemas_count': len(schemas),
        'schema_property_count': schema_property_count,
        'anyOf_count': any_of,
        'oneOf_count': one_of,
        'allOf_count': all_of,
        'decimal_format_fields': decimal_fmt,
        'longest_operation_description_length': longest_op_desc,
        'path_keys': set(paths.keys()),
    }


def diff_sets(a: set, b: set):
    return {
        'added': sorted(list(b - a)),
        'removed': sorted(list(a - b)),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--current', required=True, type=Path)
    parser.add_argument('--old', required=True, type=Path)
    args = parser.parse_args()

    current_spec = load(args.current)
    old_spec = load(args.old)
    cur_metrics = collect_metrics(current_spec, args.current)
    old_metrics = collect_metrics(old_spec, args.old)
    path_diff = diff_sets(old_metrics['path_keys'], cur_metrics['path_keys'])

    print('== Spec Metrics Comparison ==')
    for key in [
        'file_bytes','file_lines','openapi_version','info_version','info_description_length',
        'servers_count','tags_count','paths_count','operations_count','schemas_count',
        'schema_property_count','anyOf_count','oneOf_count','allOf_count','decimal_format_fields',
        'longest_operation_description_length']:
        print(f"{key}: old={old_metrics[key]} current={cur_metrics[key]} delta={cur_metrics[key]-old_metrics[key] if isinstance(cur_metrics[key], (int,float)) and isinstance(old_metrics[key], (int,float)) else 'n/a'}")

    print('\nPath differences:')
    print(f"  Added ({len(path_diff['added'])}):")
    for p in path_diff['added'][:25]:
        print(f"    + {p}")
    if len(path_diff['added']) > 25:
        print('    ...')
    print(f"  Removed ({len(path_diff['removed'])}):")
    for p in path_diff['removed'][:25]:
        print(f"    - {p}")
    if len(path_diff['removed']) > 25:
        print('    ...')

if __name__ == '__main__':
    main()
