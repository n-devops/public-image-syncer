#!/usr/bin/env bash

# 使用命令行参数指定的文件名
file=$1

# 使用命令行参数指定的镜像名
image=$2

/**
 * 检查给定的镜像名是否被文件中列出的允许项所包含。
 * 
 * 参数:
 * $1 - 文件名，包含允许的镜像名列表。
 * $2 - 需要检查的镜像名。
 * 
 * 返回值:
 * 0 - 如果镜像名被允许。
 * 1 - 如果镜像名不被允许。
 */
function check_allows() {
    local file=$1
    local image=$2
    while read line; do
        # 检查是否为通配符**允许，表示匹配任何子目录中的镜像
        if [[ "${line}" == *"**" ]]; then
            if [[ "${image}" == "${line%\*\*}"* ]]; then
                return 0
            fi
        # 检查是否为通配符*允许，表示匹配同级目录中的镜像
        elif [[ "${line}" == *"*" ]]; then
            if [[ "${image}" == "${line%\*}"* ]]; then
                if [[ "${image#"${line%\*}"}" != *"/"* ]]; then
                    return 0
                fi
            fi
        # 检查是否为精确匹配允许
        elif [[ "${line}" == "${image%\:*}" ]]; then
            return 0
        fi
    done <"${file}"

    return 1
}

# 调用函数，检查镜像是否被允许
check_allows "${file}" "${image}"
