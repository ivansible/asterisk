#!/bin/bash
#set -x

HITS=${HACKER_HITS:-100}
LOGFILE="{{ log_file }}"
BLOCKFILE="{{ block_file }}"
DEFACTION="--{{ default_action }}"

get_hackers() {
    grep -F InvalidPassword "$LOGFILE"{,.0,.1} 2>/dev/null |
    cut -d, -f9 |
    cut -d/ -f3 |
    sort |
    uniq -c |
    awk -v "HITS=${HITS}" '($1>HITS){print $1,$2}' |
    sort -nr
}

update_ferm() {
    HACKERS="$(get_hackers |grep -Ev '^ *$')"
    ADD_LIST="$(echo "$HACKERS" | awk '{print $2}' |sort -u)"
    OLD_LIST="$(awk '/asterisk/{print $1}' "$BLOCKFILE" 2>/dev/null |sort -u)"
    NEW_LIST="$(echo -e "${OLD_LIST}\n${ADD_LIST}" |grep -Ev '^ *$|^ *#' |sort -u)"

    if [ "$OLD_LIST" != "$NEW_LIST" ]; then
        echo -e "new asterisk hackers:\n${HACKERS}"
        # shellcheck disable=SC2086
        ferm-ctl -c "asterisk" add hosts.block $ADD_LIST
    fi
}

case "${1:-$DEFACTION}" in
    -s|--show)  get_hackers ;;
    -f|--ferm)  update_ferm ;;
    *)  echo "usage: $0 [--show] [--ferm]" ;;
esac
