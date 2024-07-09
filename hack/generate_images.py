import collections
from collections import OrderedDict

import yaml

if __name__ == '__main__':
    with open("./config/transfer-mappings.yaml", "r") as f:
        transferMappings = yaml.load(f, Loader=yaml.FullLoader)
    with open("./config/builder-mappings.yaml", "r") as f:
        builderMappings = yaml.load(f, Loader=yaml.FullLoader)

    transferDict = collections.OrderedDict()
    privateDict = collections.OrderedDict()

    # 自构建的镜像
    for k, v in builderMappings.items():
        privateDict[k] = v["private"]

    # 公共镜像
    with open("./config/transfer-images.yaml", "r") as f:
        transferImages = yaml.load(f, Loader=yaml.FullLoader)

    for publicImage in transferImages:
        repository = publicImage.split(":")[0]
        tag = publicImage.split(":")[1]

        if repository not in transferMappings:
            raise ValueError("transfer-mappings.yaml 映射中没有此仓库的配置: " + repository)

        transferRepository = transferMappings[repository]["transfer"]
        privateRepository = transferMappings[repository]["private"]

        transferDict[publicImage] = transferRepository
        privateDict[transferRepository + ":" + tag] = privateRepository

    transferLines = []
    for k, v in transferDict.items():
        transferLines.append(f'"{k}": "{v}"')
    # 覆盖transfer-images.yaml
    with open("transfer-images.yaml", 'w') as file:
        file.write('\n'.join(transferLines))

    privateLines = []
    for k, v in privateDict.items():
        privateLines.append(f'"{k}": "{v}"')
    # 覆盖private-images.yaml
    with open("private-images.yaml", 'w') as file:
        file.write('\n'.join(privateLines))
