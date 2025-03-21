from ubuntu:latest as build

run apt update && apt install -y g++ make
copy . .
run g++ -o backend main.cpp

cmd ["./backend"]





from ubuntu:latest as test

cmd ["true"]
