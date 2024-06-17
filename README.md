# public-image-syncer

公共镜像同步器, 同步公共镜像

## 同步器
image-syncer-v1.5.4
https://github.com/AliyunContainerService/image-syncer

## 同步过程

1. 利用GitHub Action同步镜像至阿里云北京站
2. 利用Teamcity同步镜像至私服, 注意: 使用main.py 生成配置文件 images.yaml -> generate_image.yml

## 项目结构

* [auth.yaml](images.yaml): 正在使用的认证配置
* [images.yaml](images.yaml): GitHub 公共镜像拉取配置
* [generate_image.yml](generate_image.yml): 根据 GitHub调用`main.py`生成的私服镜像拉取配置
* [main.py](main.py): 使用python 进行配置生成

## 镜像库映射规则描述

1. docker.io镜像, 官方镜像放在library项目下, 非官方镜像放在相应的项目下
    1. 官方镜像: 如 docker.io/nginx:1.17.4 -> docker-hosted.nstl-dev.com/library/nginx:1.17.4
    2. 三方镜像: 如 docker.io/adoptopenjdk/openjdk11:latest -> docker-hosted.nstl-dev.com/adoptopenjdk/openjdk11:latest
2. ghcr.io镜像, 映射至仓库ghcr.io项目下, 如: ghcr.io/kube-vip/kube-vip:v0.5.0 ->
   docker-hosted.nstl-dev.com/ghcr.io/kube-vip/kube-vip:v0.5.0
3. k8s 镜像特殊处理:
    1. 映射至私有仓库google_containers项目下, 如: registry.k8s.io/kube-proxy:v1.28.0 ->
       docker-hosted.nstl-dev.com/google_containers/kube-proxy:v1.28.0
    2. coredns特殊处理, coredns镜像/coredns/coredns路径变为/coredns打平映射, 如: registry.k8s.io/coredns/coredns:
       v1.8.6 -> docker-hosted.nstl-dev.com/google_containers/coredns:v1.8.6
    3. kubeadm 使用时 --image-repository docker-hosted.nstl-dev.com/google_containers