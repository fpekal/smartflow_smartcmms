from ubuntu:latest as build

run apt update && apt install -y g++ make
copy . .
run make

cmd ["./backend"]





from ubuntu:latest as test

cmd ["true"]
