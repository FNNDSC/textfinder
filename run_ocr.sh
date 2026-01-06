#!/usr/bin/env bash

DIR="/home/sandip/test/US-studies"
URL="http://localhost:8000/ocr"
OUT="./results"

mkdir -p "$OUT"

# Function to process one file
process_file() {
  file="$1"
  echo "Processing: $file"

  # Save output AND print to terminal
  curl -s -X POST "$URL" \
    -F "file=@$file" | jq | tee "$OUT/$(basename "$file").json"

  echo "Done: $file"
}

export -f process_file
export URL
export OUT

# Find all DICOMs (recursively) and process in parallel
find "$DIR" -type f -name "*.dcm" | parallel -j 4 process_file {}

