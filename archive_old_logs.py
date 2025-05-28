import os
import shutil
import gzip
import time

LOG_DIR = "/var/log/myapp"
ARCHIVE_DIR = os.path.join(LOG_DIR, "archive")

os.makedirs(ARCHIVE_DIR, exist_ok=True)

seven_days_ago = time.time() - (7 * 86400)

for filename in os.listdir(LOG_DIR):
    file_path = os.path.join(LOG_DIR, filename)

    if os.path.isfile(file_path) and filename.endswith(".log"):
        file_mtime = os.path.getmtime(file_path)

        if file_mtime < seven_days_ago:
            with open(file_path, 'rb') as f_in:
                with gzip.open(file_path + '.gz', 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)

            os.remove(file_path)

            shutil.move(file_path + '.gz', ARCHIVE_DIR)
            shutil.move(file_path + '.gz', ARCHIVE_DIR)
