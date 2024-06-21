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
    FROM jetbrains/teamcity-agent:$tag
    USER root
    RUN apt-get update -y \
        # node
        && curl -fsSL https://deb.nodesource.com/setup_18.x |  bash - \
        && apt-get install nodejs wget unzip jq -y \
        # standard-version
        && npm i -g standard-version \
        && npm i -g commit-and-tag-version \
        # maven
        && apt-get install maven -y --no-install-recommends \
        # gradle
        && mkdir /opt/gradle \
        && wget -P /opt/gradle https://services.gradle.org/distributions/gradle-8.7-bin.zip \
        && unzip /opt/gradle/gradle-8.7-bin.zip -d /opt/gradle \
        && rm -rf /opt/gradle/gradle-8.7-bin.zip \
        # 清理缓存
        && apt-get clean && rm -rf /var/lib/apt/lists/*
    # gradle 环境变量
    ENV GRADLE_HOME=/opt/gradle/gradle-8.7
    ENV PATH=$PATH:$GRADLE_HOME/bin
    SAVE IMAGE --push docker.io/talk9/jetbrains_teamcity-agent:$tag

teamcity-agent:
    BUILD +teamcity-agent-common --tag='2024.03'
    BUILD +teamcity-agent-common --tag='2024.03.1'
    BUILD +teamcity-agent-common --tag='2024.03.2'

elasticsearch-762:
    FROM elasticsearch:7.6.2
    RUN sh -c "/bin/echo -e y | sh /usr/share/elasticsearch/bin/elasticsearch-plugin install https://github.com/KennFalcon/elasticsearch-analysis-hanlp/releases/download/v7.6.2/elasticsearch-analysis-hanlp-7.6.2.zip"
    SAVE IMAGE --push docker.io/talk9/library_elasticsearch:7.6.2

all:
    BUILD +teamcity-agent
    BUILD +elasticsearch-762

sync:
    RUN echo "运行sync"