#!/usr/bin/env bash
# Verify the scan-to-project package required by cross-platform novel scan tasks.
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "usage: $0 BOOK_DIR [TARGET_WORDS] [MAX_CHAPTERS]" >&2
  exit 2
fi

book_dir="$1"
target_words="${2:-8万}"
max_chapters="${3:-10}"

required=(
  "README.md"
  "简介.md"
  "大纲.md"
  "正文计划.md"
  "金手指.md"
  "世界观.md"
  "人物关系.md"
  "伏笔铺垫.md"
  "封面生图提示词.md"
)

missing=0
for f in "${required[@]}"; do
  if [[ ! -s "$book_dir/$f" ]]; then
    echo "MISSING_OR_EMPTY: $f"
    missing=1
  fi
done

# Scan evidence may be titled either way across old/new workflows.
if [[ ! -s "$book_dir/扫书感悟.md" && ! -s "$book_dir/扫榜拆书报告.md" ]]; then
  echo "MISSING_OR_EMPTY: 扫书感悟.md or 扫榜拆书报告.md"
  missing=1
fi

if [[ -s "$book_dir/正文计划.md" ]]; then
  if ! grep -Eq "$target_words|80000|80,000" "$book_dir/正文计划.md"; then
    echo "MISSING_WORD_TARGET_IN_正文计划.md: $target_words"
    missing=1
  fi
  if ! grep -Eq "不超过[[:space:]]*$max_chapters|<= ?$max_chapters|${max_chapters}[[:space:]]*章" "$book_dir/正文计划.md"; then
    echo "MISSING_CHAPTER_CAP_IN_正文计划.md: $max_chapters"
    missing=1
  fi
fi

if [[ -s "$book_dir/大纲.md" ]]; then
  if ! grep -Eq "$target_words|80000|80,000" "$book_dir/大纲.md"; then
    echo "MISSING_WORD_TARGET_IN_大纲.md: $target_words"
    missing=1
  fi
  if ! grep -Eq "不超过[[:space:]]*$max_chapters|<= ?$max_chapters|${max_chapters}[[:space:]]*章" "$book_dir/大纲.md"; then
    echo "MISSING_CHAPTER_CAP_IN_大纲.md: $max_chapters"
    missing=1
  fi
fi

if [[ $missing -ne 0 ]]; then
  exit 1
fi

echo "OK: scan project package complete: $book_dir"
