FROM nvidia/opengl:1.0-glvnd-devel-ubuntu18.04 

ENV DOCKER_USER user

RUN apt-get update -y && apt-get install -y \
    vim \
    tmux \
    git \
    wget \
    lsb-release \
    lsb-core \
    tmux \
    vim \
    build-essential \
    g++ \
    sudo

# config sshd
# set user ros and sudo
RUN adduser --gecos "ROS User" --home /home/$DOCKER_USER --disabled-password $DOCKER_USER && \
    usermod -a -G dialout $DOCKER_USER && \
    echo "$DOCKER_USER ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/99_aptget

RUN chown -R $DOCKER_USER:$DOCKER_USER /home/$DOCKER_USER/

# switch to user ros, but the HOME is still /, not /home/ros
USER $DOCKER_USER

# cd /home/ros default
WORKDIR /home/$DOCKER_USER


# must run /sbin/my_init with root user
#ENTRYPOINT [ "setuser", "user"]
#CMD ["bash"]
#CMD ["tmux"]
