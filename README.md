# public-image-syncer

完成了公共镜像同步, 基于公共镜像构建, 两项功能

## 同步流程描述

![sync-pipline.png](sync-pipline.png)

1. 公共镜像同步器, 将镜像拉取到阿里云镜像仓库
2. 公共镜像构建器, 将镜像构建后推送到阿里云镜像仓库
3. Teamcity 将阿里云镜像仓库中的镜像拉取到私服

## 同步过程

1. 利用GitHub Action同步镜像或者构建镜像至阿里云北京站
2. 利用Teamcity同步镜像至私服

## 配置描述

* [auth.yaml](config/auth.yaml): 认证配置
* [transfer-images.yaml](config/transfer-images.yaml): 公共镜像同步的同步配置
* [Earthfile](Earthfile): 基于公共镜像进行构建的镜像, 构建后tag以 -n-ext 结尾
* [image-mappings.yaml](config/image-mappings.yaml): 镜像映射描述

## 镜像库映射规则描述

@formatter:off
1. docker.io镜像, 官方镜像放在library项目下, 机构镜像放在相应的机构下
    a. 官方镜像: </br>
       -> docker.io/nginx:1.17.4 </br>
       -> registry.cn-beijing.aliyuncs.com/public-image-mirror/docker.io_nginx:1.17.4 </br>
       -> docker-hosted.nstl-dev.com/library/nginx:1.17.4 </br>
    b. 机构镜像: </br>
       -> docker.io/adoptopenjdk/openjdk11:latest </br>
       -> registry.cn-beijing.aliyuncs.com/public-image-mirror/docker.io_adoptopenjdk_openjdk11:latest </br>
       -> docker-hosted.nstl-dev.com/adoptopenjdk/openjdk11:latest </br>

2. ghcr.io镜像 </br>
    a. kube-vip: </br>
       -> ghcr.io/kube-vip/kube-vip:v0.5.0 </br>
       -> registry.cn-beijing.aliyuncs.com/public-image-mirror/ghcr.io_kube-vip_kube-vip:latest </br>
       -> docker-hosted.nstl-dev.com/ghcr.io/kube-vip/kube-vip:v0.5.0 </br>

3. registry.k8s.io k8s 镜像特殊处理: </br>
    a. 映射至私有仓库google_containers项目下: </br>
       -> registry.k8s.io/kube-proxy:v1.28.0 </br>
       -> registry.cn-beijing.aliyuncs.com/nstl_google_containers/kube-proxy:v1.28.0 </br>
       -> docker-hosted.nstl-dev.com/google_containers/kube-proxy:v1.28.0  </br>
    b. coredns特殊处理, coredns镜像/coredns/coredns路径变为/coredns打平映射: </br>
       -> registry.k8s.io/coredns/coredns:latest </br>
       -> registry.cn-beijing.aliyuncs.com/nstl_google_containers/coredns:latest </br>
       -> docker-hosted.nstl-dev.com/google_containers/coredns:latest </br>
    c. kubeadm 使用时 --image-repository docker-hosted.nstl-dev.com/google_containers </br>

4. docker.elastic.co 镜像特殊处理, DockerHub上elastic的镜像不全, 只有几个最新版本的镜像: </br>
    a. elasticsearch: </br>
       -> docker.elastic.co/elasticsearch/elasticsearch  </br>
       -> registry.cn-beijing.aliyuncs.com/public-image-mirror/docker.io_library_elasticsearch  </br>
       -> docker-hosted.nstl-dev.com/library/elasticsearch </br>
    b. logstash: </br>
       -> docker.elastic.co/logstash/logstash </br>
       -> registry.cn-beijing.aliyuncs.com/public-image-mirror/docker.io_library_logstash </br>
       -> docker-hosted.nstl-dev.com/library/logstash </br>
    c. kibana: </br>
       -> docker.elastic.co/kibana/kibana </br>
       -> registry.cn-beijing.aliyuncs.com/public-image-mirror/docker.io_library_kibana </br>
       -> docker-hosted.nstl-dev.com/library/kibana </br>
    d. filebeat: </br>
       -> docker.elastic.co/beats/filebeat </br>
       -> registry.cn-beijing.aliyuncs.com/public-image-mirror/docker.io_library_filebeat </br>
       -> docker-hosted.nstl-dev.com/library/filebeat </br>

5. 自定义的公共镜像的拓展镜像, 使用[image-mappings.yaml](config/image-mappings.yaml)规则文件中的描述, 映射成相应的镜像

@formatter:on

## 同步器来自于

image-syncer-v1.5.4
https://github.com/AliyunContainerService/image-syncer

## 部分代码来自于

https://github.com/DaoCloud/public-image-mirror