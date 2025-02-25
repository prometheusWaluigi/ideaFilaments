import os

def scan_large_files(directory, size_limit_mb=5):
    """
    Scans a directory for files exceeding the size limit.

    :param directory: The root directory to scan.
    :param size_limit_mb: Size limit in MB (default is 5MB).
    """
    size_limit_bytes = size_limit_mb * 1024 * 1024
    large_files = []

    print(f"Scanning '{directory}' for files over {size_limit_mb}MB...\n")

    for root, _, files in os.walk(directory):
        for file in files:
            try:
                file_path = os.path.join(root, file)
                file_size = os.path.getsize(file_path)

                if file_size > size_limit_bytes:
                    large_files.append((file_path, file_size / (1024 * 1024)))  # size in MB

            except PermissionError:
                print(f"⚠️ Permission denied: {file_path}")
            except FileNotFoundError:
                print(f"⚠️ File not found (might be a broken link): {file_path}")
            except Exception as e:
                print(f"⚠️ Error reading {file_path}: {e}")

    if large_files:
        print("\n🚨 Large files found:")
        for path, size in large_files:
            print(f"- {path} → {size:.2f} MB")
    else:
        print("\n✅ No large files found above the threshold.")

# 🔥 Replace with your target directory and size limit if needed
if __name__ == "__main__":
    target_directory = r"C:\path\to\your\repo"  # Change this to your repo path
    scan_large_files(target_directory, size_limit_mb=5)  # Set size limit in MB
