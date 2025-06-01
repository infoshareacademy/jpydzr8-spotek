import shutil
import os

def save_attachment(source_path):
    filename = os.path.basename(source_path)
    target_path = os.path.join("zalaczniki", filename)
    shutil.copy(source_path, target_path)
    return target_path
