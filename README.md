# Assignment 1
# Part 2: Docker Containers with Commands
## Step 1

**first make directory for part 2**
```
mkdir Part2
cd Part2
```
**Pull the image from dockerhub**
```
docker pull abdulmoiz1443/finance_flask:latest
```
## Step 2
**Run the docker container.**
```
docker run -it -e API_KEY=123 finance_flask
```
**Containers logs** <br />
![Screenshot (24)](https://user-images.githubusercontent.com/65711565/227146566-6c23938e-f68b-45fa-8cc9-ad778c1d1d0c.png)

## Step 3
### using docker different commands.
### 'docker ps' command to list all running containers
```
docker ps 
```
**Output** <br />
![Screenshot (26)](https://user-images.githubusercontent.com/65711565/227149604-a81c32cc-e3e4-42d6-991f-2a0d6a31b346.png)
### 'docker stop' command to stop a running container
```
docker stop c6574625a79a
```
**Output** <br />
c6574625a79a
### 'docker rm' command to remove a stopped container
```
docker rm 574625a79a
```
**varify the existance of container**
```
docker ps -a
```
![Screenshot (27)](https://user-images.githubusercontent.com/65711565/227153265-93c04320-82a5-46b5-9f96-00bf8b0fc2e8.png)

**Output**<br />
c6574625a79a
