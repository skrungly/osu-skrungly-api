FROM python:3.13-slim

RUN apt update && apt install --no-install-recommends -y curl zstd libfontconfig libx11-6 \
    && rm -rf /var/lib/apt/lists/*

RUN curl -L -O https://github.com/hwsmm/cosutrainer/releases/download/0.15/cosu-trainer-bin.tar.zst
RUN tar --zstd -xvf cosu-trainer-bin.tar.zst ./cosu-trainer-x86_64.AppImage
RUN ./cosu-trainer-x86_64.AppImage --appimage-extract

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "app:app", "-b", "0.0.0.0:80"]
