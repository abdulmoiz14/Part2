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
**Containers logs**
![Screenshot (24)](https://user-images.githubusercontent.com/65711565/227139615-657a66f4-dd8c-4500-93b0-416abbcfd32f.png)

