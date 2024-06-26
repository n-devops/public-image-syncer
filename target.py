import sys

from shared_function import to_private_registry

if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise ValueError("必须传递参数")
    issueNumber = sys.argv[1]
    image = sys.argv[2]
    targetImage = sys.argv[2]

    if targetImage.startswith("docker.io/library/"):
        targetImage = targetImage.replace("docker.io/library/", "docker.io/", 1)

    # registry.k8s.io
    if targetImage.startswith("registry.k8s.io/"):
        targetImage = "registry.cn-beijing.aliyuncs.com/" + image.replace("registry.k8s.io/", "nstl_google_containers/",
                                                                          1)
        # 如果包含/coredns/coredns, 则替换成/coredns
        if "/coredns/coredns" in targetImage:
            targetImage = targetImage.replace("/coredns/coredns", "/coredns", 1)
    else:
        if targetImage.startswith("docker.elastic.co/"):
            targetImage = targetImage.replace("docker.elastic.co/elasticsearch/elasticsearch",
                                              "docker.io/elasticsearch", 1)
            targetImage = targetImage.replace("docker.elastic.co/logstash/logstash",
                                              "docker.io/logstash", 1)
            targetImage = targetImage.replace("docker.elastic.co/kibana/kibana",
                                              "docker.io/kibana", 1)
            targetImage = targetImage.replace("docker.elastic.co/beats/filebeat",
                                              "docker.io/filebeat", 1)
        # targetImage 替换 / 为 _
        targetImage = targetImage.replace("/", "_")
        targetImage = "registry.cn-beijing.aliyuncs.com/public-image-mirror/" + targetImage

    # targetImage 删除:xx 后缀
    targetImage = targetImage.split(":")[0]

    str = '"' + image + '":\n  - ' + targetImage
    strArr = str.split('\n')

    registry = to_private_registry(strArr)
    registry.append('\n')

    # 覆盖generate/images.yaml
    with open("temp_images.yaml", 'w') as file:
        file.write(str)

    with open(f"target_images_{issueNumber}.yaml", 'w') as file:
        file.write('\n'.join(registry))
