#!/usr/bin/env bash
# Download all People's Education Press (人教版) elementary math PDF textbooks
# Source: https://github.com/TapXWorld/ChinaTextbook/tree/master/小学/数学/人教版
set -euo pipefail

DEST_DIR="$(cd "$(dirname "$0")/.." && pwd)/小学数学-人教版"
mkdir -p "$DEST_DIR"
cd "$DEST_DIR"

API_URL="https://api.github.com/repos/TapXWorld/ChinaTextbook/contents/小学/数学/人教版"

echo "Fetching file list from GitHub API..."
TMP_JSON="$(mktemp)"
curl -fsSL "$API_URL" -o "$TMP_JSON"

NUM_FILES=$(jq 'length' "$TMP_JSON")
echo "Found $NUM_FILES files. Starting downloads..."
echo

urlencode() {
  python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1], safe=':/'))" "$1"
}

i=0
while IFS=$'\t' read -r name url size; do
  i=$((i+1))
  size_mb=$(awk -v s="$size" 'BEGIN{printf "%.1f", s/1048576}')
  printf "[%2d/%d] %s (%s MB)\n" "$i" "$NUM_FILES" "$name" "$size_mb"
  if [ -f "$name" ]; then
    actual_size=$(stat -c%s "$name" 2>/dev/null || stat -f%z "$name")
    if [ "$actual_size" = "$size" ]; then
      echo "        already exists, skipping."
      continue
    fi
  fi
  encoded_url=$(urlencode "$url")
  for attempt in 1 2 3 4; do
    if curl -fL --retry 0 --connect-timeout 30 --max-time 600 -o "$name.part" "$encoded_url"; then
      mv "$name.part" "$name"
      break
    fi
    sleep_time=$((2 ** (attempt + 1)))
    echo "        attempt $attempt failed, retrying in ${sleep_time}s..."
    sleep "$sleep_time"
    if [ "$attempt" = 4 ]; then
      echo "        FAILED to download $name"
      rm -f "$name.part"
      exit 1
    fi
  done
done < <(jq -r '.[] | [.name, .download_url, .size] | @tsv' "$TMP_JSON")

rm -f "$TMP_JSON"
echo
echo "All done. Files saved to: $DEST_DIR"
ls -lh "$DEST_DIR"
