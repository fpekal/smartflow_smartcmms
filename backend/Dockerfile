from ubuntu:latest as build

run apt update && apt install -y python3 python3-pip python3-venv
workdir /app
copy . .
run /bin/bash -c "python3 -m venv . && source ./bin/activate && pip install -r ./backend/requirements.txt"

cmd ["/bin/bash", "-c", "source ./bin/activate && python3 backend/main.py"]





from ubuntu:latest as test

cmd ["true"]
