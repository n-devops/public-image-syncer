import yaml

def to_private_registry(tempLines):
    tempStr = '\n'.join(tempLines)
    ymlData = yaml.safe_load(tempStr)
    writeLines = []
    for k, v in ymlData.items():
        split = k.split(":", 1)
        originalImageAddress = split[0]

        if len(split) != 2:
            raise ValueError("split长度不为2")

        for vv in v:
            writeLines.append(f"{vv}:{split[1]}:")
            if originalImageAddress.startswith("docker.io/"):
                # 如果是docker.io/xxx/xxx 格式
                image_address_split = originalImageAddress.split("/")
                # 如果长度为2, 代表是官方的镜像, 在中间增加 library
                if len(image_address_split) == 2:
                    originalImageAddress = f"library/{image_address_split[1]}"
                else:
                    # 删除 docker.io/
                    originalImageAddress = originalImageAddress.replace("docker.io/", "", 1)
            if originalImageAddress.startswith("registry.k8s.io/"):
                originalImageAddress = originalImageAddress.replace("registry.k8s.io/", "google_containers/", 1)
                # originalImageAddress如果包含/coredns/coredns, 则替换成/coredns
                if "/coredns/coredns" in originalImageAddress:
                    originalImageAddress = originalImageAddress.replace("/coredns/coredns", "/coredns", 1)
            if originalImageAddress.startswith("docker.elastic.co/"):
                originalImageAddress = originalImageAddress.replace("docker.elastic.co/elasticsearch/elasticsearch",
                                                                    "library/elasticsearch", 1)
                originalImageAddress = originalImageAddress.replace("docker.elastic.co/logstash/logstash",
                                                                    "library/logstash", 1)
                originalImageAddress = originalImageAddress.replace("docker.elastic.co/kibana/kibana",
                                                                    "library/kibana", 1)
                originalImageAddress = originalImageAddress.replace("docker.elastic.co/beats/filebeat",
                                                                    "library/filebeat", 1)
            writeLines.append(f"  - docker-hosted.nstl-dev.com/{originalImageAddress}")
    return writeLines