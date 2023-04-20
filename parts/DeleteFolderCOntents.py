import os
import glob


def delete(path):
    try:
        files = glob.glob(path)
        for f in files:
            os.remove(f)
    except WindowsError as e:
        print(f"ERROR: {e}")
