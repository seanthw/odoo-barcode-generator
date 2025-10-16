import sys
import os
import re

def update_manifest_version(version):
    manifest_path = '__manifest__.py'
    if not os.path.exists(manifest_path):
        print(f"Error: {manifest_path} not found.")
        sys.exit(1)

    with open(manifest_path, 'r') as f:
        content = f.read()

    # Use a regular expression to find and replace the version string.
    # This is safer than simple string replacement.
    new_content, count = re.subn(
        r"('version'\s*:\s*)" + "'[^']+'",
        f"\1'{version}'",
        content,
        count=1
    )

    if count == 0:
        # If 'version' key is not found, try to add it after 'name'.
        new_content, count = re.subn(
            r"('name'\s*:\s*'[^']+',)",
            f"\1\n    'version': '{version}',",
            content,
            count=1
        )
        if count == 0:
            print("Error: 'name' key not found in __manifest__.py, could not add 'version'.")
            sys.exit(1)

    with open(manifest_path, 'w') as f:
        f.write(new_content)

    print(f"Successfully updated __manifest__.py to version {version}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python update_manifest_version.py <new_version>")
        sys.exit(1)
    
    new_version = sys.argv[1]
    update_manifest_version(new_version)
