# utils/export_zip.py
import zipfile
from io import BytesIO
import os


def create_zip_output(folder_path):
    zip_buffer = BytesIO()

    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                zip_file.write(file_path, arcname=filename)

    zip_buffer.seek(0)
    return zip_buffer.read()
