#!/usr/bin/env python3
"""Generate a minimal OpenAPI spec from the full sdk/openapi.json.

Purpose: Reduce payload size to test Postman Spec Hub publication stability.

Strategy:
 - Load existing sdk/openapi.json
 - Retain: openapi version, info (annotated), servers (if any)
 - Include only the /api/health path if present; otherwise create a basic one.
 - Omit all components to drastically shrink size unless health path references them.
 - Output written to sdk/openapi-min.json

This is intentionally lossy and not a substitute for full documentation.
"""
import json
import os
from pathlib import Path

SOURCE = Path('sdk/openapi.json')
TARGET = Path('sdk/openapi-min.json')

def load_full_spec():
    if not SOURCE.exists():
        raise SystemExit(f"Source spec not found: {SOURCE}")
    with SOURCE.open('r', encoding='utf-8') as f:
        return json.load(f)

def build_min_spec(full):
    openapi_version = full.get('openapi', '3.0.0')
    info = full.get('info', {})
    min_info = {
        'title': info.get('title', 'Spearmint API') + ' (Minimal)',
        'version': info.get('version', '0.0.0'),
        'description': 'Minimal subset for publish test. NOT FOR PRODUCTION.'
    }
    servers = full.get('servers', [])

    paths = {}
    health_key = '/api/health'
    if 'paths' in full and health_key in full['paths']:
        paths[health_key] = full['paths'][health_key]
    else:
        # Create a synthetic health path
        paths[health_key] = {
            'get': {
                'summary': 'Health check',
                'operationId': 'health_check_min',
                'responses': {
                    '200': {
                        'description': 'OK',
                        'content': {
                            'application/json': {
                                'schema': {
                                    'type': 'object',
                                    'properties': {
                                        'status': {'type': 'string'},
                                        'version': {'type': 'string'}
                                    },
                                    'required': ['status', 'version']
                                },
                                'example': {'status': 'healthy', 'version': info.get('version', '0.0.0')}
                            }
                        }
                    }
                }
            }
        }

    min_spec = {
        'openapi': openapi_version,
        'info': min_info,
        'servers': servers,
        'paths': paths,
        # Keep empty components to remain structurally valid
        'components': {
            'schemas': {}
        }
    }
    return min_spec

def write_min_spec(spec):
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    with TARGET.open('w', encoding='utf-8') as f:
        json.dump(spec, f, indent=2)
    size_bytes = TARGET.stat().st_size
    print(f"Minimal spec written to {TARGET} ({size_bytes} bytes)")

def main():
    full = load_full_spec()
    orig_size = SOURCE.stat().st_size
    min_spec = build_min_spec(full)
    write_min_spec(min_spec)
    print(f"Original size: {orig_size} bytes")

if __name__ == '__main__':
    main()
