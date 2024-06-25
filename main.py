import yaml

from shared_function import to_private_registry

if __name__ == '__main__':
    with open("config/images.yaml", 'r') as file:
        content = file.read().splitlines()

    writeLines = []
    # 合并 config/build-images.yaml
    with open("config/build-images.yaml", "r") as f:
        writeLines.extend(f.read().splitlines())
        writeLines.append("")

    tempLines = []
    for line in content:
        line = line.strip()
        if line and not line.startswith("#"):
            tempLines.append(line)
        else:
            if tempLines:
                i = to_private_registry(tempLines)
                writeLines.extend(i)
            writeLines.append(line)
            tempLines = []

    if tempLines:
        i = to_private_registry(tempLines)
        writeLines.extend(i)

    # 覆盖generate/images.yaml
    with open("generate/images.yaml", 'w') as file:
        file.write('\n'.join(writeLines))
