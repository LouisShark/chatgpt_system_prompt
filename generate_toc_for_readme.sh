#!/bin/bash

generate_toc() {
    local dir=$1
    local base_dir=$(pwd)
    local exclude_dir="knowledge"  # 设置要排除的目录名称

    for file in "$dir"/*; do
        # 获取文件或目录的基本名称
        local name=$(basename "$file")

        # 如果是要排除的目录，则跳过
        if [ "$name" == "$exclude_dir" ]; then
            continue
        fi

        if [ -d "$file" ]; then
            echo "- $name"
            echo "  $(generate_toc "$file")"
        elif [ -f "$file" ] && [[ $file == *.md ]]; then
            local title=$(basename "$file" .md)
            # Replace Windows incompatible characters with '_'
            local safe_title=$(echo "$title" | sed 's/[<>:："\/\\|?*]/_/g')
            # Rename the source file with the safe_title
            mv "$file" "$dir/$safe_title.md"
            # Create a relative link
            local relative_link="${dir#$base_dir/}/$safe_title.md"
            # Manually encode only spaces and other few characters if needed
            local encoded_link=$(echo "$relative_link" | sed 's/ /%20/g; s/"//g')
            echo "  - [$safe_title]($encoded_link)"
        fi
    done
}

# 清空现有的 TOC.md 文件内容
> TOC.md

# 生成目录并将其写入 TOC.md
generate_toc . >> TOC.md
