import yaml

# 读取./config/transfer-mappings.yaml, 生成allows.txt
if __name__ == '__main__':
    # 读取./config/transfer-mappings.yaml, 转换成ymlData
    with open("./config/transfer-mappings.yaml", "r") as f:
        ymlData = yaml.load(f, Loader=yaml.FullLoader)

    writeLines = []
    if ymlData is None:
        raise ValueError("config/transfer-mappings.yaml 不存在")

    # 遍历ymlData.public, 生成generate/allows.txt
    for k, v in ymlData.items():
        writeLines.append(k)

    writeLines.append('\n')

    with open(f"allows.txt", 'w') as file:
        file.write('\n'.join(writeLines))
