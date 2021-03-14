#!/bin/bash
#
# Regards, the Alveare Solutions society.
#
# SETTERS

function set_programming_language () {
    local PROLANG="$1"
    if [[ "$PROLANG" != 'python' ]] && [[ "$PROLANG" != 'bash' ]]; then
        error_msg "Unsupported programming language (${RED}$PROLANG${RESET})."\
            "Defaulting to (${MAGENTA}python${RESET})."
        MD_DEFAULT['language']='python'
        return 1
    fi
    MD_DEFAULT['language']="$PROLANG"
    return 0
}

function set_target_file () {
    local FILE_PATH="$1"
    check_file_exists "$FILE_PATH"
    if [ $? -ne 0 ]; then
        error_msg "File (${RED}$FILE_PATH${RESET}) does not exist."
        return 1
    fi
    MD_DEFAULT['target-file']="$FILE_PATH"
    return 0
}

function set_target_directory () {
    local DIR_PATH="$1"
    check_directory_exists "$DIR_PATH"
    if [ $? -ne 0 ]; then
        error_msg "Directory (${RED}$DIR_PATH${RESET}) does not exist."
        return 1
    fi
    MD_DEFAULT['target-dir']="$DIR_PATH"
    return 0
}

function set_report_directory () {
    local DIR_PATH="$1"
    check_directory_exists "$DIR_PATH"
    if [ $? -ne 0 ]; then
        error_msg "Directory (${RED}$DIR_PATH${RESET}) does not exist."
        return 1
    fi
    MD_DEFAULT['report-dir']="$DIR_PATH"
    return 0
}

function set_report_flag () {
    local REPORT="$1"
    if [[ "$REPORT" != 'on' ]] && [[ "$REPORT" != 'off' ]]; then
        error_msg "Invalid report flag value (${RED}$REPORT${RESET})."\
            "Defaulting to (${GREEN}ON${RESET})."
        MD_DEFAULT['report']='on'
        return 1
    fi
    MD_DEFAULT['report']="$REPORT"
    return 0
}

function set_autocommit_flag () {
    local AUTOCOMMIT="$1"
    if [[ "$AUTOCOMMIT" != 'on' ]] && [[ "$AUTOCOMMIT" != 'off' ]]; then
        error_msg "Invalid autocommit flag value (${RED}$AUTOCOMMIT${RESET})."\
            "Defaulting to (${RED}OFF${RESET})."
        MD_DEFAULT['autocommit']='off'
        return 1
    fi
    MD_DEFAULT['autocommit']="$AUTOCOMMIT"
    return 0
}
