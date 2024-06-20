VERSION 0.8

# jetbrains
teamcity-agent:
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