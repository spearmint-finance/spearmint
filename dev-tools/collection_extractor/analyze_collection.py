#!/usr/bin/env python3
"""
Postman Collection Analyzer

Parses a Postman collection JSON file and generates a comprehensive overview report
showing all API endpoints, grouped by resource, with HTTP methods and full paths.
"""

import json
import sys
import argparse
from collections import defaultdict
from pathlib import Path


def extract_endpoints(items, path_parts=[]):
    """Recursively extract all endpoints from nested Postman item structure."""
    endpoints = []
    
    if not items:
        return endpoints
    
    for item in items:
        current_path_parts = path_parts + [item.get('name', 'Unnamed')]
        
        # Folder: has sub-items
        if 'item' in item and item['item']:
            endpoints.extend(extract_endpoints(item['item'], current_path_parts))
        # Endpoint: has a request
        elif 'request' in item:
            request = item['request']
            method = request.get('method', 'UNKNOWN')
            
            # Extract URL from various formats
            if isinstance(request.get('url'), str):
                url = request['url']
            elif isinstance(request.get('url'), dict):
                url = request['url'].get('raw', '')
            else:
                url = ''
            
            endpoints.append({
                'path': ' > '.join(current_path_parts),
                'method': method,
                'url': url,
                'name': item.get('name', 'Unnamed')
            })
    
    return endpoints


def generate_report(json_file, output_dir):
    """Parse collection and generate overview report."""
    
    json_file = Path(json_file)
    output_dir = Path(output_dir)
    
    if not json_file.exists():
        print(f"❌ Error: File not found: {json_file}")
        sys.exit(1)
    
    # Load collection
    try:
        with open(json_file, 'r', encoding='utf-8-sig') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in {json_file}: {e}")
        sys.exit(1)
    
    collection = data.get('collection', data)
    info = collection.get('info', {})
    
    collection_name = info.get('name', 'Unknown Collection')
    collection_desc = info.get('description', 'No description')
    
    # Extract endpoints
    all_endpoints = extract_endpoints(collection.get('item', []))
    
    # Group by top-level section
    grouped = defaultdict(list)
    for endpoint in all_endpoints:
        top_level = endpoint['path'].split(' > ')[0]
        grouped[top_level].append(endpoint)
    
    # ===== GENERATE TEXT REPORT =====
    report_lines = []
    report_lines.append("\n" + "=" * 110)
    report_lines.append("POSTMAN COLLECTION OVERVIEW".center(110))
    report_lines.append("=" * 110)
    report_lines.append(f"\nCollection: {collection_name}")
    report_lines.append(f"Description: {collection_desc}")
    report_lines.append(f"Total Endpoints: {len(all_endpoints)}\n")
    
    # Method summary
    method_counts = defaultdict(int)
    for ep in all_endpoints:
        method_counts[ep['method']] += 1
    
    report_lines.append("HTTP Methods:")
    for method in ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']:
        if method in method_counts:
            report_lines.append(f"  {method.ljust(8)} : {method_counts[method]:3d}")
    
    report_lines.append("\n" + "=" * 110)
    report_lines.append("ENDPOINTS BY RESOURCE".center(110))
    report_lines.append("=" * 110)
    
    # Display endpoints grouped by section
    for section in sorted(grouped.keys()):
        endpoints_in_section = grouped[section]
        report_lines.append(f"\n【 {section} 】 — {len(endpoints_in_section)} endpoint(s)")
        report_lines.append("-" * 110)
        
        # Group by method
        by_method = defaultdict(list)
        for ep in endpoints_in_section:
            by_method[ep['method']].append(ep)
        
        # Display by method
        for method in ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']:
            if method in by_method:
                for ep in sorted(by_method[method], key=lambda x: x['url']):
                    method_str = method.ljust(8)
                    url_display = ep['url'][:85] + ('...' if len(ep['url']) > 85 else '')
                    report_lines.append(f"  {method_str}  {url_display}")
    
    report_lines.append("\n" + "=" * 110 + "\n")
    
    report_text = '\n'.join(report_lines)
    
    # ===== SAVE REPORT =====
    safe_name = collection_name.replace(' ', '_').replace('/', '_').lower()
    report_file = output_dir / f"{safe_name}_overview.txt"
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report_text)
    
    print(report_text)
    print(f"✓ Report saved: {report_file}")
    
    # ===== GENERATE CSV =====
    csv_file = output_dir / f"{safe_name}_endpoints.csv"
    
    with open(csv_file, 'w', encoding='utf-8') as f:
        f.write('Section,Endpoint Name,HTTP Method,URL Path\n')
        for ep in sorted(all_endpoints, key=lambda x: (x['path'], x['method'])):
            section = ep['path'].split(' > ')[0]
            url_escaped = ep['url'].replace('"', '""')
            f.write(f'"{section}","{ep["name"]}","{ep["method"]}","{url_escaped}"\n')
    
    print(f"✓ CSV export saved: {csv_file}")


def main():
    parser = argparse.ArgumentParser(
        description='Analyze a Postman collection and generate overview reports'
    )
    parser.add_argument('-i', '--input', required=True, help='Path to collection JSON file')
    parser.add_argument('-o', '--output', default='.', help='Output directory for reports')
    
    args = parser.parse_args()
    
    generate_report(args.input, args.output)


if __name__ == '__main__':
    main()
