import os
import shutil
import subprocess
import tempfile
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile

COSU_TRAINER_TIMEOUT = 60
COSU_TRAINER_BIN = os.environ.get(
    "COSU_TRAINER_BIN", shutil.which("cosu-trainer")
)


def regenerate_osz_with_rates(osz_buffer, diff_file, rates):
    if not COSU_TRAINER_BIN:
        raise FileNotFoundError("unable to locate cosu-trainer")

    # start by preparing a temp map dir for cosu-trainer
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        diff_path = temp_path / diff_file

        with ZipFile(osz_buffer) as osz:
            osz.extractall(temp_path)

        for rate in rates:
            try:
                subprocess.run(
                    [COSU_TRAINER_BIN, diff_path, rate],
                    timeout=COSU_TRAINER_TIMEOUT,
                    check=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )

            except subprocess.TimeoutExpired:
                raise RuntimeError("cosu-trainer took too long!")

            except subprocess.CalledProcessError as e:
                raise RuntimeError(f"cosu-trainer failed! [{e.returncode}]")

        modified_osz_buffer = BytesIO()
        with ZipFile(modified_osz_buffer, "w") as modified_osz:
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    modified_osz.write(Path(root) / file, file)

    modified_osz_buffer.seek(0)
    return modified_osz_buffer
