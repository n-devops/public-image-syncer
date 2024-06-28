import yaml
import sys

if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise ValueError("必须传递参数 issue image")
    issueNumber = sys.argv[1]
    image = sys.argv[2].strip()

    with open("./config/image-mappings.yaml", "r") as f:
        ymlData = yaml.load(f, Loader=yaml.FullLoader)

    mappings = ymlData['public']
    repository = image.split(":")[0]
    tag = image.split(":")[1]

    # repository是否包含repository的key
    if repository not in mappings:
        raise ValueError("规则映射中没有此仓库的配置: " + repository)

    mapping = mappings[repository]
    transferImage = mapping['transfer'] + ":" + tag
    transferImagesYaml = '"' + image + '":\n  - ' + mapping['transfer']
    privateImagesYaml = '"' + transferImage + '":\n  - ' + mapping['private']

    # 覆盖issue_images.yml
    with open("issue_images.yaml", 'w') as file:
        file.write(transferImagesYaml)

    with open(f"target_images_{issueNumber}.yaml", 'w') as file:
        file.write(privateImagesYaml)
