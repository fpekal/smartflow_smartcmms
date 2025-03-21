from ubuntu:latest

run apt update && apt install -y g++ make
copy . .
run g++ -o backend main.cpp

cmd ["./backend"]
