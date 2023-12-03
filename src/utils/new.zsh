#!/usr/bin/env zsh

AOC_DIR="${HOME}/Projekte/advent.of.code/advent-of-code"
TEMPLATE="${AOC_DIR}/src/utils/template.py"

AOC_CLI_BIN="${HOME}/.cargo/bin/aoc"
YEAR=${YEAR:=$(date +%Y)}
DAY=${DAY:=$(date +%d)}

work_dir="${AOC_DIR}/src/${YEAR}/day${DAY}"
mkdir -p "${work_dir}" && cd "${work_dir}" || exit 1
cp -i "${TEMPLATE}" "${work_dir}/p1.py"

target_seconds=$(date --date "${YEAR}-12-${DAY} 00:00 UTC-5" +%s)

## testing:
#target_seconds=$(( $(date +%s) + 5 ))

###
### Wait for the target time
###
print -P "%F{blue}Target: ${target_seconds}%f"

while : ; do {
  current_seconds=$(date +%s)
  (( current_seconds + 3 > target_seconds )) && break
  echo -en "\r$(date +%s.%N)"
  sleep 0.5
}; done

print -P "\n\n%F{red}%BGet ready!!!%b%f"

while (( $(date +%s) <=  target_seconds )); do {
  current_seconds=$(date +%s)
  (( current_seconds >= target_seconds )) && break
  echo -en "\r$(date +%s.%N)"
  sleep .01
}; done

print -P "\n\n%F{blue}Starting at %B$(date +%s.%N)%b%f\n"

###
### Download the puzzle
###

max_error_counter=0
while (( max_error_counter < 5 )); do {
  if ${AOC_CLI_BIN} download --year "$YEAR" --day "$DAY" --overwrite ; then {
    print -P "%F{green}Puzzle downloaded%f"
    break
  }; else {
    print -P "%F{red}Error downloading puzzle%f"
    (( max_error_counter++ ))
    sleep .1
  }; fi
}; done

if (( max_error_counter >= 5 )); then {
  print -P "%F{red}Too many errors. Exiting.%f"
  exit 1
}; fi

if pcre2grep -Me '(?:[`]{3}[\n\s]*)([^`]+)(?:[`]{3})' -m1 --output '$1' "${work_dir}/puzzle.md" ; then {
  print -P "%F{green}Example found%f"

  print -P "%F{blue}Extracting example:%f"
  pcre2grep -Me '(?:[`]{3}[\n\s]*)([^`]+)(?:[`]{3})' -m1 --output '$1' \
    "${work_dir}/puzzle.md" >| "${work_dir}/example"

  print -P "%F{blue}Example:%f"
  cat "${work_dir}/example"
}; else {
  print -P "%F{red}No example found%f"
}; fi

print -P "\n%F{green}Have fun!%f"