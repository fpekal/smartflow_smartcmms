from ubuntu:latest as build

run apt update && apt install -y g++ make
copy . .
run g++ -o backend main.cpp

cmd ["./backend"]





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
