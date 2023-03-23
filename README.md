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
### 1. 'docker ps' command to list all running containers
```
docker ps 
```
**Output** <br />
![Screenshot (26)](https://user-images.githubusercontent.com/65711565/227149604-a81c32cc-e3e4-42d6-991f-2a0d6a31b346.png)
### 2. 'docker stop' command to stop a running container
```
docker stop c6574625a79a
```
**Output** <br />
c6574625a79a
### 3. 'docker rm' command to remove a stopped container
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

### 4. 'docker logs' command to view the logs of a container
```
docker logs ec1713e3f7fd
```
**Output** <br />
![Screenshot (28)](https://user-images.githubusercontent.com/65711565/227154974-5745b77a-cf58-4dc6-8c63-a715b94d7463.png)

### 5. 'docker inspect' command to view the details of a container
```
docker inspect finance_flask
```
**Output** <br />
![Screenshot (29)](https://user-images.githubusercontent.com/65711565/227155543-aeac09c2-7bf2-462a-b6d4-b37cec610265.png)

### 6. 'docker exec' command to execute a command inside a running container

**changing value of env of a running container**
```
docker exec -e API_KEY=345 ec1713e3f7fd env
```

**Output** <br />
![Screenshot (30)](https://user-images.githubusercontent.com/65711565/227160508-2fe1ae75-9c2b-464b-911d-13b210ffd1fa.png)

### 7. 'docker attach' command to attach to a running container
```
docker attach ec1713e3f7fd
```

### 8. 'docker commit' command to create a new image from a container
```
docker commit ef8f745129be abdulmoiz1443/finance_flask:latest
```
**Output** <br />
![Screenshot (31)](https://user-images.githubusercontent.com/65711565/227167395-90560368-2765-4797-bab1-1e57ffb3f460.png)

### 9. 'docker cp' command to copy files/folders between the container and the host

**Coping requirements.txt from container to current directory of host**
```
docker cp ef8f745129be:requirements.txt .
```
**Output** <br />
![Screenshot (32)](https://user-images.githubusercontent.com/65711565/227170400-a6b747cf-cab9-49db-8ec6-912b36dbea67.png)

### 10. 'docker stats' command to view the resource usage of containers

```
docker stats
```
**Output**<br />
![Screenshot (33)](https://user-images.githubusercontent.com/65711565/227171554-17b3118f-f4a8-44c6-b7c5-561f24c60201.png)

### 11. 'docker top' command to view the running processes inside a container
```
docker top ef8f745129be
```
**Output** <br />
![Screenshot (34)](https://user-images.githubusercontent.com/65711565/227172436-f99ca6e7-3b5e-4d23-918c-fdf69f72034c.png)

### 12. 'docker start' command to start a stopped container
```
docker start ef8f745129be
```
**Output** <br />
![Screenshot (35)](https://user-images.githubusercontent.com/65711565/227173704-bda52056-f993-4b3e-9579-5b5968735320.png)
### 13. 'docker pause' command to pause a running container
```
docker pause ef8f745129be
```
**Output** <br />
![Screenshot (36)](https://user-images.githubusercontent.com/65711565/227174590-f2ccdb18-78b6-42d6-8a1c-522ac79d9ea7.png)

### 14. 'docker unpause' command to unpause a paused container
```
docker unpause ef8f745129be
```
**Output** <br />
![Screenshot (37)](https://user-images.githubusercontent.com/65711565/227175123-9bddb76e-8d7d-4fac-a6c3-439b3b75e3ff.png)

### 15. 'docker rename' command to rename a container
```
docker rename ef8f745129be Finance
```
**Output** <br />
![Screenshot (38)](https://user-images.githubusercontent.com/65711565/227175841-7627dea2-3553-44a8-85ed-590c836b11f6.png)
