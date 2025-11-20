import json
import sys
from openapi_spec_validator import validate_spec
from openapi_spec_validator.readers import read_from_filename

def validate(spec_path):
    try:
        spec_dict, _ = read_from_filename(spec_path)
        validate_spec(spec_dict)
        print(f"✅ Spec at {spec_path} is valid.")
    except Exception as e:
        print(f"❌ Validation Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate_openapi.py <path_to_spec>")
        sys.exit(1)
    validate(sys.argv[1])
