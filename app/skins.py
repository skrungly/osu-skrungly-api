import shutil
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile

import requests

from app import app
from app.utils import DEFAULT_SKIN_ID, DEFAULT_SKIN_URL, MAX_SKIN_SIZE


def delete_skin(skin_id):
    for path in (app.osk_dir / skin_id, app.skins_dir / skin_id):
        if path.exists():
            shutil.rmtree(path)


def save_skin(osk_buffer, file_name, skin_id):
    delete_skin(skin_id)

    skin_dir = app.skins_dir / skin_id
    skin_dir.mkdir()

    with ZipFile(osk_buffer) as osk:
        # extract the archive file-by-file
        total_size = 0
        for zipped_file in osk.infolist():
            if zipped_file.is_dir():
                continue

            total_size += zipped_file.file_size

            # do a quick check for decompression bombs
            if total_size > MAX_SKIN_SIZE:
                delete_skin(skin_id)
                # TODO: be explicit about the size limit
                raise RuntimeError("skin files exceed total size limit")

            # force all skin elements to be at the root
            zipped_file.filename = Path(zipped_file.filename).name
            osk.extract(zipped_file, Path(skin_dir))

    # we'll now also store the osk itself
    archive_dir = app.osk_dir / skin_id
    archive_dir.mkdir()

    osk_buffer.seek(0)
    with open(archive_dir / file_name, "wb") as osk_file:
        shutil.copyfileobj(osk_buffer, osk_file)


def check_for_default_skin(*, download=False):
    if (app.osk_dir / DEFAULT_SKIN_ID).exists():
        return True

    if not download or not DEFAULT_SKIN_URL:
        return False

    response = requests.get(DEFAULT_SKIN_URL)
    if not response.ok:
        return False

    save_skin(BytesIO(response.content), "default.osk", DEFAULT_SKIN_ID)
    return True
