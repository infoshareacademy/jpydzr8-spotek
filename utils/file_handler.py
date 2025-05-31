import shutil
import os

def save_attachment(source_path):
    filename = os.path.basename(source_path)
    target_path = os.path.join("uploads", filename)
    shutil.copy(source_path, target_path)
    return target_path
