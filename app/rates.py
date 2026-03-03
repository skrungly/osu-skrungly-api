import os
import shutil
import subprocess
import tempfile
import time
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile

from app import app, celery
from app.utils import fetch_beatmap_osz

COSU_TRAINER_TIMEOUT = int(os.environ.get("COSU_TRAINER_TIMEOUT", 120))
COSU_TRAINER_BIN = os.environ.get(
    "COSU_TRAINER_BIN", shutil.which("cosu-trainer")
)


def _run_cosu_trainer(task, diff_path, rates, index):
    current_rate = rates[index]

    proc_args = [
        COSU_TRAINER_BIN,
        diff_path,
        current_rate,
        "af",
        "of",
    ]

    started_at = time.time()
    proc = subprocess.Popen(
        proc_args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    def _raise_on_timeout_or_error():
        if time.time() - started_at > COSU_TRAINER_TIMEOUT:
            proc.kill()
            raise RuntimeError("cosu-trainer took too long!")

        if proc.poll():
            raise RuntimeError(f"cosu-trainer failed! [{proc.returncode}]")

    while proc.poll() is None:
        output = b""
        while (char := proc.stdout.read(1)) != b"\r":
            _raise_on_timeout_or_error()
            output += char

        progress = 0.0
        percent = output.rstrip(b"%")
        if percent.isdigit() and int(percent) <= 100:
            progress = (1 + index + int(percent) / 100) / (len(rates) + 1)

        task.update_state(
            state="PROGRESS",
            meta={
                "current": progress,
                "total": 1.0,
                "status": f"generating {current_rate}"
            }
        )

        _raise_on_timeout_or_error()


@celery.task(bind=True)
def generate_osz_with_rates(self, map_info, rates=None):
    if rates and not COSU_TRAINER_BIN:
        raise FileNotFoundError("unable to locate cosu-trainer")

    self.update_state(
        state="PROGRESS",
        meta={
            "current": 0.0,
            "total": 1.0,
            "status": "downloading .osz file"
        }
    )

    osz_buffer = fetch_beatmap_osz(map_info["set_id"])
    if osz_buffer is None:
        raise RuntimeError("unable to fetch map from any mirrors")

    osz_name = "{set_id} {artist} - {title}.osz".format(**map_info)
    task_dir = app.osz_dir / self.request.id
    task_dir.mkdir()

    osz_path = task_dir / osz_name
    result_path = Path("/") / osz_path.relative_to(app._data_dir)

    if not rates:
        with open(osz_path, "wb") as osz_file:
            osz_file.write(osz_buffer.getbuffer())

        return {
            "current": 1.0,
            "total": 1.0,
            "status": "saved .osz file",
            "result": str(result_path)
        }

    # if user wants rates, we're not done yet.
    self.update_state(
        state="PROGRESS",
        meta={
            "current": 1 / (len(rates) + 1),
            "total": 1.0,
            "status": "retrieved .osz file"
        }
    )

    # start by preparing a temp map dir for cosu-trainer
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        diff_path = temp_path / map_info["filename"]

        with ZipFile(osz_buffer) as osz:
            osz.extractall(temp_path)

        for i, rate in enumerate(rates):
            _run_cosu_trainer(self, diff_path, rates, i)

            self.update_state(
                state="PROGRESS",
                meta={
                    "current": (2 + i) / (len(rates) + 1),
                    "total": 1.0,
                    "status": f"generated {rate}"
                }
            )

        modified_osz_buffer = BytesIO()
        with ZipFile(modified_osz_buffer, "w") as modified_osz:
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    modified_osz.write(Path(root) / file, file)

        with open(osz_path, "wb") as osz_file:
            osz_file.write(modified_osz_buffer.getbuffer())

        return {
            "current": 1.0,
            "total": 1.0,
            "status": "generated modified .osz file",
            "result": str(result_path)
        }
