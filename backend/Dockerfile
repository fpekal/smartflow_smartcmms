from ubuntu:latest as build

run apt update && apt install -y python3 python3-pip python3-venv gcc libpq-dev curl jq libreoffice build-essential wget
run wget https://ftp.gnu.org/gnu/gawk/gawk-5.3.2.tar.gz && \
    tar -xzf gawk-5.3.2.tar.gz && \
    cd gawk-5.3.2 && \
    ./configure && \
    make && \
    make install && \
    cd .. && \
    rm -rf gawk-5.3.2 gawk-5.3.2.tar.gz # nie ma tej wersji gawka na niczym :)
run curl -LO https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
run apt-get install -y ./google-chrome-stable_current_amd64.deb
run rm google-chrome-stable_current_amd64.deb
workdir /app
copy . .
run /bin/bash -c "python3 -m venv . && source ./bin/activate && pip install -r ./backend/requirements.txt"

cmd ["/bin/bash", "-c", "source ./bin/activate && flask --app ./backend/main.py run --debug"]





from ubuntu:latest as test

run apt update && apt install -y jq libreoffice build-essential wget
run wget https://ftp.gnu.org/gnu/gawk/gawk-5.3.2.tar.gz && \
    tar -xzf gawk-5.3.2.tar.gz && \
    cd gawk-5.3.2 && \
    ./configure && \
    make && \
    make install && \
    cd .. && \
    rm -rf gawk-5.3.2 gawk-5.3.2.tar.gz # nie ma tej wersji gawka na niczym :)
workdir /tests
copy . .

cmd ["/tests/backend/tests/run_tests.sh"]
