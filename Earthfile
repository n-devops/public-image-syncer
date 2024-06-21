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

all:
    # BUILD +teamcity-agent
    BUILD +elasticsearch

sync:
    FROM scratch