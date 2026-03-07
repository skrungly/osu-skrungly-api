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


def _run_cosu_trainer(task, diff_path, rates, index, log_file):
    current_rate = rates[index]

    proc_args = [
        COSU_TRAINER_BIN,
        diff_path,
        current_rate,
        "af",
        "of",
    ]

    log_file.write(f"==> {proc_args}\n\n".encode())

    started_at = time.time()
    proc = subprocess.Popen(
        proc_args,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )

    prev_line = None
    next_line = bytearray()

    task.update_state(
        state="PROGRESS",
        meta={
            "current": index / len(rates),
            "total": 1.0,
            "status": f"generating {current_rate}"
        }
    )

    while proc.poll() is None:
        if time.time() - started_at > COSU_TRAINER_TIMEOUT:
            proc.kill()
            raise RuntimeError("cosu-trainer took too long!")

        # read one character per iteration to keep it predictable
        char = proc.stdout.read(1)

        if char == b"%" and next_line.isdigit():
            progress = int(next_line) / 100
            task.update_state(
                state="PROGRESS",
                meta={
                    "current": (index + progress) / len(rates),
                    "total": 1.0,
                    "status": f"generating {current_rate}"
                }
            )

        elif char == b"\r":
            char = b"\n"

        next_line += char

        if char == b"\n":
            # only log lines that differ from the last, because
            # cosu-trainer repeats a *lot* of progress updates
            if next_line != prev_line:
                log_file.write(next_line)
                prev_line = next_line.copy()

            next_line.clear()

    log_file.write(b"\n")

    if proc.poll():
        raise RuntimeError(f"cosu-trainer failed! [{proc.returncode}]")


def _find_diff_file(mapset_path, map_id):
    for diff_path in mapset_path.glob("*.osu"):
        with open(diff_path) as diff_file:
            for line in diff_file:
                if not line.startswith("BeatmapID"):
                    continue

                if line.strip().endswith(map_id):
                    return diff_path

                break


@celery.task(bind=True)
def generate_osz_with_rates(self, map_info, rates=None):
    if rates and not COSU_TRAINER_BIN:
        raise FileNotFoundError("unable to locate cosu-trainer")

    self.update_state(
        state="PROGRESS",
        meta={
            "current": None,
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
            "current": 0.0,
            "total": 1.0,
            "status": "retrieved .osz file"
        }
    )

    log_dir = app.log_dir / "rates"
    log_dir.mkdir(exist_ok=True)
    log_path = log_dir / f"{self.request.id}.log"

    # start by preparing a temp map dir for cosu-trainer
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        with ZipFile(osz_buffer) as osz:
            osz.extractall(temp_path)

        diff_path = _find_diff_file(temp_path, str(map_info['id']))
        if diff_path is None:
            raise FileNotFoundError("unable to find .osu file for map?")

        with open(log_path, "wb") as log_file:
            for i, rate in enumerate(rates):
                _run_cosu_trainer(self, diff_path, rates, i, log_file)

                self.update_state(
                    state="PROGRESS",
                    meta={
                        "current": (1 + i) / len(rates),
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
