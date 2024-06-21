VERSION 0.8

# 镜像库命名规则
# 1. 官方镜像, 在默认基础上增加library作为机构名称
# 2. 机构名称, 仓库名称多个单词使用 '-' 进行连接
# 3. 机构名称与仓库名称之间使用 '_' 进行连接
# 官方镜像: nginx:latest -> docker.io/talk9/library_nginx:latest
# 官方镜像: eclipse-temurin:latest -> docker.io/talk9/library_eclipse-temurin:latest
# 机构镜像: jetbrains/teamcity-agent:2024.03.2 -> docker.io/talk9/jetbrains_teamcity-agent:2024.03.2

# jetbrains
teamcity-agent-common:
    ARG tag='2024.03.2'
    ARG extTag=$tag-n-ext
    FROM jetbrains/teamcity-agent:$tag
    USER root
    RUN apt-get update -y > /dev/null 2>&1 \
        # node
        && curl -fsSL https://deb.nodesource.com/setup_18.x |  bash - > /dev/null 2>&1 \
        && apt-get install nodejs wget unzip jq -y > /dev/null 2>&1 \
        # standard-version
        && npm i -g standard-version > /dev/null 2>&1 \
        && npm i -g commit-and-tag-version > /dev/null 2>&1 \
        # maven
        && apt-get install maven -y --no-install-recommends > /dev/null 2>&1 \
        # gradle
        && mkdir /opt/gradle \
        && wget -P /opt/gradle https://services.gradle.org/distributions/gradle-8.7-bin.zip \
        && unzip /opt/gradle/gradle-8.7-bin.zip -d /opt/gradle > /dev/null \
        && rm -rf /opt/gradle/gradle-8.7-bin.zip \
        # 清理缓存
        && apt-get clean && rm -rf /var/lib/apt/lists/*
    # gradle 环境变量
    ENV GRADLE_HOME=/opt/gradle/gradle-8.7
    ENV PATH=$PATH:$GRADLE_HOME/bin
    SAVE IMAGE --push registry.cn-beijing.aliyuncs.com/public-image-mirror/docker.io_jetbrains_teamcity-agent:$extTag

teamcity-agent:
    BUILD +teamcity-agent-common --tag='2024.03'
    BUILD +teamcity-agent-common --tag='2024.03.1'
    BUILD +teamcity-agent-common --tag='2024.03.2'

# elasticsearch
elasticsearch-common:
    ARG tag='7.6.2'
    ARG extTag=$tag-n-ext
    FROM docker.elastic.co/elasticsearch/elasticsearch:$tag
    ENV URL_HANLP="https://github.com/KennFalcon/elasticsearch-analysis-hanlp/releases/download/v$tag/elasticsearch-analysis-hanlp-$tag.zip"
    RUN sh -c "/bin/echo -e y | sh /usr/share/elasticsearch/bin/elasticsearch-plugin install ${URL_HANLP}"
    SAVE IMAGE --push registry.cn-beijing.aliyuncs.com/public-image-mirror/docker.io_elasticsearch:$extTag

elasticsearch:
    BUILD +elasticsearch-common --tag='7.6.2'
    BUILD +elasticsearch-common --tag='7.10.2'

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

all:
    # BUILD +teamcity-agent
    # BUILD +elasticsearch
    BUILD +adoptopenjdk-openjdk11

sync:
    FROM scratch