1) build docker
```
source ./build.bash
```
2) run docker
```
source ./run.bash
```
3) Start Docker
```
sudo docker start ubuntu_mbzirc2020
```
4) execute docker
```
xhost+
docker exec -it ubuntu_mbzirc2020 bash
```
5) Inside docker execute commands from 
https://mrs.felk.cvut.cz/gitlab/uav/uav_core

Be careful that after reboot there will be problems with execution of ~/.bashrc and after the boot the mouse pointer is a *black* cross so it is not possible to see it unless you move it above the window.

Be aware that doker sees your file system and you can work with the files from your filesystem while executing them inside docker.
