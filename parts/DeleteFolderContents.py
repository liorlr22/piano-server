import os


def delete(path):
    try:
        for f in os.listdir(path):
            os.remove(os.path.join(path, f))
    except WindowsError as e:
        print(f"ERROR: {e}")


if __name__ == '__main__':
    delete("opt-cropped")
