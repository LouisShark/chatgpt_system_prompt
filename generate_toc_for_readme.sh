#!/bin/bash

generate_toc() {
    local dir=$1
    local base_dir=$(pwd)

    for file in "$dir"/*; do
        if [ -d "$file" ]; then
            local dir_name=$(basename "$file")
            echo "- $dir_name"
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

generate_toc .
