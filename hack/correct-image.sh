#!/usr/bin/env bash

# 函数：guess_image
# 描述：根据输入的参数猜测并规范化Docker镜像名称。
# 参数：
#   $1 - 输入的字符串，预期为Docker镜像名称。
# 返回值：
#   如果成功规范化镜像名称，则输出规范化后的名称；如果无法规范化，则不输出任何内容。
function guess_image() {
    local image="${1}"

    # 去除镜像名称中的空格
    image="${image// /}"
    # 去除镜像名称前的路径斜杠
    image="${image#\/}"
    # 去除镜像名称后的路径斜杠
    image="${image%\/}"

    # 如果处理后的镜像名称为空，则退出函数
    if [[ -z "${image}" ]]; then
        return
    fi

    # 如果镜像名称包含registry.hub.docker.com/r/，则转换为docker.io/格式
    if [[ "${image}" == *"registry.hub.docker.com/r/"* ]]; then
        image="docker.io/${image##*registry.hub.docker.com\/r\/}"
    fi
    # 如果镜像名称包含hub.docker.com/r/，则转换为docker.io/格式
    if [[ "${image}" == *"hub.docker.com/r/"* ]]; then
        image="docker.io/${image##*hub.docker.com\/r\/}"
    fi
    # 如果镜像名称不包含路径斜杠，则添加library/前缀
    if [[ "${image}" != *"/"* ]]; then
        image="library/${image}"
    fi
    # 如果镜像名称的域名部分不包含点号，则认为是docker.io
    if [[ "${image%%/*}" != *"."* ]]; then
        image="docker.io/${image}"
    fi
    # 如果镜像名称不包含版本标签，则默认为latest
    if [[ "${image}" != *": "* ]]; then
        image="${image}:latest"
    fi
    # 如果镜像名称包含非法字符（如双斜杠或空格），则退出函数
    if [[ "${image}" == *"//"* ]] || [[ "${image}" == *" "* ]]; then
        return
    fi

    echo "${image}"
}

# 调用guess_image函数，传入命令行参数作为输入
guess_image "${1}"
