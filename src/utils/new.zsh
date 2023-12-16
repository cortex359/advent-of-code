#!/usr/bin/env zsh

AOC_DIR="${${PWD%/utils}%/src}"
TEMPLATE="${AOC_DIR}/src/utils/template.py"
AOC_CLI_BIN="$(whence aoc)"

if [[ "${${${PWD%/utils}%/src}:t}" != "advent-of-code" ]]; then {
    print -Pu2 "%F{red}[ERROR] AOC_DIR is expected to point to a dir named %Badvent-of-code%b but was %B${AOC_DIR}%b.%f"
    print -Pu2 "%F{red}Aborting.%f"
    exit 1
}; fi
if [[ ! -s ${TEMPLATE} ]]; then {
    print -Pu2 "%F{red}[ERROR] TEMPLATE=%B${TEMPLATE}%b not found or empty.%f"
    exit 2
}; fi
if [[ ! -x ${AOC_CLI_BIN} ]]; then {
    print -Pu2 "%F{red}[ERROR] aoc-cli was not found.%f"
    exit 3
}; fi


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
if (( target_seconds > $(date +%s) )); then {
    print -P "🎄 %F{blue}Waiting until $(date -d @${target_seconds} +'%A, den %d. %B %Y, %X Uhr %Z')%f"

    ### Waiting phase 1
    while : ; do {
        current_seconds=$(date +%s)
        time_left=$(( target_seconds - current_seconds ))
        (( time_left < 3 )) && break
        print -P "\r\r%F{blue}%B${time_left}%b seconds%f"
        sleep 0.5
    }; done

    ### Waiting phase 2
    print -P "\n\n%F{red}%BGet ready!!!%b%f"
    while (( $(date +%s) <=  target_seconds )); do {
        current_seconds=$(date +%s)
        (( current_seconds >= target_seconds )) && break
        echo -en "\r$(date +%s.%N)"
        sleep .01
    }; done
}; fi


print -P "\n\n%F{blue}Starting at %B$(date +'%A, den %d. %B %Y, %X Uhr %Z. %s.%N')%b%f\n"

###
### Download the puzzle
###
max_error_counter=0
max_errors=5
while (( max_error_counter <= max_errors )); do {
    if ${AOC_CLI_BIN} download --year "${YEAR}" --day "${DAY}" --overwrite ; then {
        print -P "%F{green}[OK] Puzzle downloaded.%f"
        break
    }; else {
        waiting_for=$(( 0.1 + max_error_counter * 0.2 ))
        (( max_error_counter++ ))
        print -Pu2 "%F{red}[ERROR] Could not download puzzle. ${max_error_counter}/${max_errors}%f"
        print -Pu2 "%F{red}[ERROR] Waiting for %B${waiting_for}%b seconds before trying again.%f"
        sleep ${waiting_for}
    }; fi
}; done

if (( max_error_counter >= max_errors )); then {
    print -Pu2 "%F{red}[ERROR] Oh fuck! Too many errors. Exiting.%f"
    exit 4
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

print -P "\n🎄 %F{green}Have fun!%f 🎄"