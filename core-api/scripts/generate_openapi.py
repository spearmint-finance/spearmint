"""
Script to generate OpenAPI specification JSON from the FastAPI application.
Usage: python generate_openapi.py [output_path]
"""
import json
import sys
import os
import logging
from pathlib import Path

# Add src to python path
current_dir = Path(__file__).parent.parent
sys.path.append(str(current_dir))

# Suppress logging during import to prevent polluting stdout if we print
logging.disable(logging.CRITICAL)

def generate_spec(output_path: str):
    try:
        from src.financial_analysis.api.main import app
        
        spec = app.openapi()
        
        with open(output_path, 'w') as f:
            json.dump(spec, f, indent=2)
            
        # Re-enable logging to print success
        logging.disable(logging.NOTSET)
        print(f"Successfully generated OpenAPI spec at: {output_path}")
        
    except Exception as e:
        logging.disable(logging.NOTSET)
        print(f"Error generating spec: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    output = "../sdk/openapi.json"
    if len(sys.argv) > 1:
        output = sys.argv[1]
        
    generate_spec(output)
