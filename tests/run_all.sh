#!/usr/bin/env bash
set -euo pipefail

# ---------- Config ----------
LOG="tests/results.log"
HM_DIR="hamming74"
CRC_DIR="crc32"

# ---------- Helpers ----------
trim(){ echo "$1" | tr -d '[:space:]\r-'; }

compile(){
  g++ -std=c++17 -O2 -o "$HM_DIR/sender" "$HM_DIR/sender.cpp"
  g++ -std=c++17 -O2 -o "$CRC_DIR/receiver" "$CRC_DIR/receiver.cpp"
}

run_hamming_block () {
  local title="$1" file="$2"
  echo -e "\n=== Hamming (7,4) – $title ===" | tee -a "$LOG"
  while IFS= read -r line || [ -n "$line" ]; do
    [[ -z "$line" || "$line" == \#* ]] && continue
    IFS='>' read -r f1 f2 f3 _ <<< "$line"
    local msg=$(trim "$f1")
    local ok=$(trim "$f2")
    local err=$(trim "$f3")
    local out
    out=$(python3 "$HM_DIR/receiver.py" <<< "$err")
    printf "msg=%s ok=%s err=%s -> %s\n" "$msg" "$ok" "$err" "$out" | tee -a "$LOG"
  done < "$file"
}

run_crc_block () {
  local title="$1" file="$2"
  echo -e "\n=== CRC-32 – $title ===" | tee -a "$LOG"
  while IFS= read -r line || [ -n "$line" ]; do
    [[ -z "$line" || "$line" == \#* ]] && continue
    IFS='>' read -r _ _ f3 _ <<< "$line"
    local err=$(trim "$f3")
    local out
    out=$(echo "$err" | "./$CRC_DIR/receiver")
    printf "err_frame=%s -> %s\n" "$err" "$out" | tee -a "$LOG"
  done < "$file"
}

# ---------- Start ----------
: > "$LOG"
compile

# ----- Hamming: sin error -----
echo "=== Hamming (7,4) – SIN error ===" | tee -a "$LOG"
while IFS= read -r m || [ -n "$m" ]; do
  [[ -z "$m" || "$m" == \#* ]] && continue
  code=$(./"$HM_DIR"/sender <<< "$m")
  out=$(python3 "$HM_DIR/receiver.py" <<< "$code")
  printf "msg=%s code=%s -> %s\n" "$m" "$code" "$out" | tee -a "$LOG"
done < tests/messages.txt

# ----- Hamming: 1 error & 2+ errores -----
run_hamming_block "1 error"  "tests/hamming_1err.txt"
run_hamming_block "2+ errores" "tests/hamming_2err.txt"

# ----- CRC: sin error -----
echo -e "\n=== CRC-32 – SIN error ===" | tee -a "$LOG"
while IFS= read -r m || [ -n "$m" ]; do
  [[ -z "$m" || "$m" == \#* ]] && continue
  frame=$(python3 "$CRC_DIR/sender.py" <<< "$m")
  out=$(echo "$frame" | "./$CRC_DIR/receiver")
  printf "msg=%s frame=%s -> %s\n" "$m" "$frame" "$out" | tee -a "$LOG"
done < tests/messages.txt

# ----- CRC: 1 error & 2+ errores -----
run_crc_block "1 error"  "tests/crc_1err.txt"
run_crc_block "2+ errores" "tests/crc_2err.txt"

echo -e "\nListo. Resultados en $LOG"