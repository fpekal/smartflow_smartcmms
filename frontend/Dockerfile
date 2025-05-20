from ubuntu:latest as build

run apt update && apt install -y npm
workdir /app
copy . .
workdir /app/frontend
run npm install

cmd ["npm", "run", "dev", "--", "--host"]
