VERSION 0.8

# 镜像库命名规则
# 1. 官方镜像, 在默认基础上增加library作为机构名称
# 2. 机构名称, 仓库名称多个单词使用 '-' 进行连接
# 3. 机构名称与仓库名称之间使用 '_' 进行连接
# 官方镜像: nginx:latest -> registry.cn-beijing.aliyuncs.com/public-image-mirror/docker.io_library_nginx:latest
# 官方镜像: eclipse-temurin:latest -> registry.cn-beijing.aliyuncs.com/public-image-mirror/docker.io_library_eclipse-temurin:latest
# 机构镜像: jetbrains/teamcity-agent:2024.03.2 -> registry.cn-beijing.aliyuncs.com/public-image-mirror/docker.io_jetbrains_teamcity-agent

# jetbrains
teamcity-agent-common:
    ARG tag='2024.03.2'
    ARG extTag=$tag-n-ext
    FROM jetbrains/teamcity-agent:$tag
    USER root
    # 添加源地址
    RUN curl -fsSL https://deb.nodesource.com/setup_18.x |  bash - > /dev/null 2>&1 \
     && apt-get update -y > /dev/null 2>&1 \
     # 安装system node \
     && apt-get install nodejs \
     && node -v \
     # standard-version
     && npm i -g standard-version \
     && npm i -g commit-and-tag-version
     # 安装时区包
     && apt-get install -y tzdata > /dev/null 2>&1 \
     # 设置时区
     && echo $TZ > /etc/timezone \
     && ln -fs /usr/share/zoneinfo/${TZ} /etc/localtime \
     # 验证时区
     && date -R && ls -l /etc/localtime \
     # git lfs
     && apt-get install git-lfs -y \
     && apt-get install wget unzip jq -y > /dev/null 2>&1 \
     # maven
     && apt-get install maven -y --no-install-recommends > /dev/null 2>&1 \
     # gradle
     && mkdir /opt/gradle \
     && wget -P /opt/gradle https://services.gradle.org/distributions/gradle-8.7-bin.zip \
     && unzip /opt/gradle/gradle-8.7-bin.zip -d /opt/gradle > /dev/null \
     && rm -rf /opt/gradle/gradle-8.7-bin.zip \
     # yq
     && wget https://github.com/mikefarah/yq/releases/latest/download/yq_linux_amd64 -O /usr/bin/yq \
     && chmod +x /usr/bin/yq \
     # 清理缓存
     && apt-get clean && rm -rf /var/lib/apt/lists/*
    # 安装多版本node
    RUN curl -fsSL https://fnm.vercel.app/install | bash -s -- --skip-shell
    ENV PATH="/root/.local/share/fnm:$PATH"
    RUN eval "$(fnm env --use-on-cd --shell bash)" \
     && fnm install 20 \
     && fnm install 22 \
     && fnm install 24 \
     && fnm list \
     && fnm current
    # gradle 环境变量
    ENV GRADLE_HOME=/opt/gradle/gradle-8.7
    ENV PATH=$PATH:$GRADLE_HOME/bin
    SAVE IMAGE --push registry.cn-beijing.aliyuncs.com/public-image-mirror/docker.io_jetbrains_teamcity-agent:$extTag

teamcity-agent:
    BUILD +teamcity-agent-common --tag='2024.12.2'

# elasticsearch
elasticsearch-7:
    ARG tag='7.6.2'
    ARG extTag=$tag-n-ext
    FROM docker.elastic.co/elasticsearch/elasticsearch:$tag
    ENV URL_HANLP="https://github.com/KennFalcon/elasticsearch-analysis-hanlp/releases/download/v$tag/elasticsearch-analysis-hanlp-$tag.zip"
    RUN sh -c "/bin/echo -e y | sh /usr/share/elasticsearch/bin/elasticsearch-plugin install ${URL_HANLP}"
    SAVE IMAGE --push registry.cn-beijing.aliyuncs.com/public-image-mirror/docker.io_library_elasticsearch:$extTag
elasticsearch-8:
    ARG tag='8.14.2'
    ARG extTag=$tag-n-ext
    FROM docker.elastic.co/elasticsearch/elasticsearch:$tag
    ENV URL_IK="https://get.infini.cloud/elasticsearch/analysis-ik/$tag"
    RUN sh -c "sh /usr/share/elasticsearch/bin/elasticsearch-plugin install --batch ${URL_IK}" \
        && sh -c "bin/elasticsearch-plugin install --batch analysis-kuromoji" \
        && sh -c "bin/elasticsearch-plugin install --batch analysis-icu" \
        && sh -c "bin/elasticsearch-plugin install --batch analysis-nori" \
        && sh -c "bin/elasticsearch-plugin install --batch analysis-phonetic" \
        && sh -c "bin/elasticsearch-plugin install --batch analysis-smartcn" \
        && sh -c "bin/elasticsearch-plugin install --batch analysis-stempel" \
        && sh -c "bin/elasticsearch-plugin install --batch analysis-ukrainian" \
        && sh -c "bin/elasticsearch-plugin install --batch mapper-size" \
        && sh -c "bin/elasticsearch-plugin install --batch mapper-murmur3" \
        && sh -c "bin/elasticsearch-plugin install --batch mapper-annotated-text" \
        && sh -c "bin/elasticsearch-plugin install --batch repository-hdfs" \
        && sh -c "bin/elasticsearch-plugin install --batch store-smb"
    SAVE IMAGE --push registry.cn-beijing.aliyuncs.com/public-image-mirror/docker.io_library_elasticsearch:$extTag

elasticsearch:
    BUILD +elasticsearch-8 --tag='8.14.2'
    BUILD +elasticsearch-8 --tag='8.14.3'
    BUILD +elasticsearch-8 --tag='8.15.0'

# adoptopenjdk
adoptopenjdk-openjdk11-common:
    ARG tag='debian'
    ARG extTag=$tag-n-ext
    ARG skywalkingAgent='8.14.0'
    FROM adoptopenjdk/openjdk11:$tag

    #设置时区环境
    ENV TZ=Asia/Shanghai
    ENV SKYWALKING_AGENT=$skywalkingAgent
    # 指定目录进行下载
    WORKDIR /data

    RUN apt-get update > /dev/null 2>&1 \
     # 安装时区包
     && apt-get install -y tzdata > /dev/null 2>&1 \
     # 设置时区
     && echo $TZ > /etc/timezone \
     && ln -fs /usr/share/zoneinfo/${TZ} /etc/localtime \
     # 验证时区
     && date -R && ls -l /etc/localtime \
     # 安装wget tini
     && apt-get install -y wget tini > /dev/null 2>&1 \
     # 清理缓存
     && apt-get clean && rm -rf /var/lib/apt/lists/* \
     # 添加 skywalking agent 到 /data/agnet目录, eg: /data/agent/skywalking-agent.jar
     && wget -O apache-skywalking-java-agent.tgz https://archive.apache.org/dist/skywalking/java-agent/$SKYWALKING_AGENT/apache-skywalking-java-agent-$SKYWALKING_AGENT.tgz > /dev/null 2>&1 \
     && tar -zxvf apache-skywalking-java-agent.tgz > /dev/null 2>&1 \
     && mv skywalking-agent agent \
     && rm apache-skywalking-java-agent.tgz
    SAVE IMAGE --push registry.cn-beijing.aliyuncs.com/public-image-mirror/docker.io_adoptopenjdk_openjdk11:$extTag

adoptopenjdk-openjdk11:
    BUILD +adoptopenjdk-openjdk11-common --tag='debian'

# eclipse-temurin
eclipse-temurin-17-common:
    ARG tag='17-jammy'
    ARG extTag=$tag-n-ext
    ARG skywalkingAgent='9.3.0'
    FROM docker.io/library/eclipse-temurin:$tag

    #设置时区环境
    ENV TZ=Asia/Shanghai
    ENV SKYWALKING_AGENT=$skywalkingAgent
    # 指定目录进行下载
    WORKDIR /data

    RUN apt-get update > /dev/null 2>&1 \
     # 安装时区包
     && apt-get install -y tzdata > /dev/null 2>&1 \
     # 设置时区
     && echo $TZ > /etc/timezone \
     && ln -fs /usr/share/zoneinfo/${TZ} /etc/localtime \
     # 验证时区
     && date -R && ls -l /etc/localtime \
     # 安装wget tini
     && apt-get install -y wget tini > /dev/null 2>&1 \
     # 清理缓存
     && apt-get clean && rm -rf /var/lib/apt/lists/* \
     # 添加 skywalking agent 到 /data/agnet目录, eg: /data/agent/skywalking-agent.jar
     && wget -O apache-skywalking-java-agent.tgz https://archive.apache.org/dist/skywalking/java-agent/$SKYWALKING_AGENT/apache-skywalking-java-agent-$SKYWALKING_AGENT.tgz > /dev/null 2>&1 \
     && tar -zxvf apache-skywalking-java-agent.tgz > /dev/null 2>&1 \
     && mv skywalking-agent agent \
     && rm apache-skywalking-java-agent.tgz
    SAVE IMAGE --push registry.cn-beijing.aliyuncs.com/public-image-mirror/docker.io_library_eclipse-temurin:$extTag

eclipse-temurin-17:
    BUILD +eclipse-temurin-17-common --tag='17-jammy'

flink-common:
    ARG version='1.20.0'
    ARG tag=$version-scala_2.12-java17
    FROM docker.io/apache/flink:$tag

    #设置时区环境
    ENV TZ=Asia/Shanghai
    RUN apt-get update > /dev/null 2>&1 \
     # 安装时区包
     && apt-get install -y tzdata > /dev/null 2>&1 \
     # 设置时区
     && echo $TZ > /etc/timezone \
     && ln -fs /usr/share/zoneinfo/${TZ} /etc/localtime \
     # 清理缓存
     && apt-get clean && rm -rf /var/lib/apt/lists/* \
     # 创建 s3 插件目录
     && mkdir -p /opt/flink/plugins/s3-fs-presto \
     && wget -O /opt/flink/plugins/s3-fs-presto/flink-s3-fs-presto-$version.jar \
        https://repo1.maven.org/maven2/org/apache/flink/flink-s3-fs-presto/$version/flink-s3-fs-presto-$version.jar

    SAVE IMAGE --push registry.cn-beijing.aliyuncs.com/public-image-mirror/docker.io_library_flink:$tag

flink:
    BUILD +flink-common --version='1.20.0'
    BUILD +flink-common --version='1.19.1'
    BUILD +flink-common --version='1.18.1'

mongo-common:
    ARG version='3.4.24'
    ARG tag=$version
    ARG extTag=$tag-n-ext
    FROM docker.io/library/mongo:$tag

    #设置时区环境
    ENV TZ=Asia/Shanghai
    RUN apt-get update > /dev/null 2>&1 \
     # 安装时区包
     && apt-get install -y tzdata > /dev/null 2>&1 \
     # 设置时区
     && echo $TZ > /etc/timezone \
     # 清理缓存
     && apt-get clean && rm -rf /var/lib/apt/lists/*

    SAVE IMAGE --push registry.cn-beijing.aliyuncs.com/public-image-mirror/docker.io_library_mongo:$extTag

mongo:
    BUILD +mongo-common --version='3.4.24'

mycat:
    ARG version='1.5.1'
    ARG tag=$version
    FROM adoptopenjdk/openjdk11:debian

    #设置时区环境
    ENV TZ=Asia/Shanghai
 
    # 指定目录进行下载
    WORKDIR /data

    RUN apt-get update > /dev/null 2>&1 \
     # 安装时区包
     && apt-get install -y tzdata > /dev/null 2>&1 \
     # 设置时区
     && echo $TZ > /etc/timezone \
     && ln -fs /usr/share/zoneinfo/${TZ} /etc/localtime \
     # 验证时区
     && date -R && ls -l /etc/localtime \
     # 安装wget tini
     && apt-get install -y wget tini > /dev/null 2>&1 \
     # 清理缓存
     && apt-get clean && rm -rf /var/lib/apt/lists/* \
     # 下载安装mycat
     && wget -O /data/Mycat-server-linux.tar.gz \
      https://github.com/MyCATApache/Mycat-download/raw/refs/heads/master/1.5-RELEASE/Mycat-server-1.5.1-RELEASE-20161130213509-linux.tar.gz \
     && cd /data \
     && tar -zxvf Mycat-server-linux.tar.gz \
     && rm -rf /data/Mycat-server-linux.tar.gz \
     && ls -lna

    VOLUME /data/mycat/conf
    VOLUME /data/mycat/logs
    EXPOSE 8066 9066

    ENTRYPOINT ["/usr/bin/tini", "--", "/bin/sh", "-c", "/data/mycat/bin/mycat start"]

    SAVE IMAGE --push registry.cn-beijing.aliyuncs.com/public-image-mirror/docker.io_library_mycat:$tag

# python
python-common:
    ARG tag='3.13.1-bookworm'
    ARG extTag=$tag-n-ext
    FROM docker.io/library/python:$tag

    #设置时区环境
    ENV TZ=Asia/Shanghai
    # 指定目录进行下载
    WORKDIR /data

    RUN apt-get update > /dev/null 2>&1 \
     # 安装时区包
     && apt-get install -y tzdata > /dev/null 2>&1 \
     # 设置时区
     && echo $TZ > /etc/timezone \
     && ln -fs /usr/share/zoneinfo/${TZ} /etc/localtime \
     # 验证时区
     && date -R && ls -l /etc/localtime \
     # 安装wget tini
     && apt-get install -y wget tini > /dev/null 2>&1 \
     # 清理缓存
     && apt-get clean && rm -rf /var/lib/apt/lists/* \
     # 安装pdm
     && pip install -U pdm
    SAVE IMAGE --push registry.cn-beijing.aliyuncs.com/public-image-mirror/docker.io_library_python:$extTag

python-3.13:
    BUILD +python-common --tag='3.13.1-bookworm'


all:
    BUILD +teamcity-agent
    BUILD +elasticsearch
    BUILD +adoptopenjdk-openjdk11

specified:
    BUILD +teamcity-agent

sync:
    FROM scratch