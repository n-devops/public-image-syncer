import yaml

if __name__ == '__main__':
    with open("./config/image-mappings.yaml", "r") as f:
        ymlData = yaml.load(f, Loader=yaml.FullLoader)

    publicMappings = ymlData['public']
    buildMappings = ymlData['build']

    transferLines = []
    privateLines = []

    # 自构建的镜像
    for k, v in buildMappings.items():
        privateLines.append('"' + k + '":')
        privateLines.append('  - ' + v["private"])

    # 公共镜像
    with open("./config/transfer-images.yaml", "r") as f:
        publicImages = yaml.load(f, Loader=yaml.FullLoader)
    for publicImage in publicImages:
        repository = publicImage.split(":")[0]
        tag = publicImage.split(":")[1]

        if repository not in publicMappings:
            raise ValueError("image-mappings.yaml public 映射中没有此仓库的配置: " + repository)

        transferRepository = publicMappings[repository]["transfer"]
        privateRepository = publicMappings[repository]["private"]

        transferLines.append('"' + publicImage + '":')
        transferLines.append('  - ' + transferRepository)

        privateLines.append('"' + transferRepository + ':' + tag + '":')
        privateLines.append('  - ' + privateRepository)

    # 覆盖transfer-images.yaml
    with open("transfer-images.yaml", 'w') as file:
        file.write('\n'.join(transferLines))

    # 覆盖private-images.yaml
    with open("private-images.yaml", 'w') as file:
        file.write('\n'.join(privateLines))
