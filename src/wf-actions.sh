#!/bin/bash
#
# Regards, the Alveare Solutions society.
#
# ACTIONS

function action_war_factory_help () {
    echo; info_msg "Select cargo script to view instructions for:
    "
    CLI_CARGO=`fetch_selection_from_user "Help" ${!MD_CARGO[@]}`
    if [ $? -ne 0 ]; then
        return 1
    fi
    ${MD_CARGO[$CLI_CARGO]} --help
    return $?
}

function action_view_dazzle_reports () {
    DAZZLE_REPORTS=(
    `fetch_all_directory_content "${MD_DEFAULT['report-dir']}" | \
        grep '.dazzle'`
    )
    echo; info_msg "Select dazzle report to inspect or (${MAGENTA}Back${RESET})
    "
    REPORT=`fetch_selection_from_user 'Report' "${DAZZLE_REPORTS[@]}"`
    if [ $? -ne 0 ]; then
        echo; info_msg "Aborting action."
        return 1
    fi
    ${MD_DEFAULT['file-editor']} "${MD_DEFAULT['report-dir']}/${REPORT}"
    return $?
}

function action_start_war_factory () {
    echo; info_msg "Powering On ${BLUE}$SCRIPT_NAME${RESET}...
    "
    WF_ARGUMENTS="`format_war_factory_cli_argument_string`"
    ${MD_CARGO['war-factory']} $WF_ARGUMENTS
    EXIT_CODE=$?
    if [ $EXIT_CODE -ne 0 ]; then
        warning_msg "Software failure!"
    else
        info_msg "Powering Off ${RED}$SCRIPT_NAME${RESET}."
    fi
    return 0
}

function action_set_programming_language () {
    SUPPORTED_LANGS=( 'python' 'bash' )
    echo; info_msg "Select programming language or (${MAGENTA}Back${RESET}).
    "
    NEW_LANGUAGE=`fetch_selection_from_user 'Language' ${SUPPORTED_LANGS[@]}`
    if [ $? -ne 0 ]; then
        echo; info_msg "Aborting action."
        return 1
    fi
    set_programming_language "$NEW_LANGUAGE"
    EXIT_CODE=$?
    echo; if [ $EXIT_CODE -ne 0 ]; then
        nok_msg "Something went wrong."\
            "Could not set language (${RED}$NEW_LANGUAGE${RESET})."
    else
        ok_msg "Successfully set language (${GREEN}$NEW_LANGUAGE${RESET})."
    fi
    return $EXIT_CODE
}

function action_set_dazzle_report_directory () {
    echo; info_msg "Type absolute directory path or (${MAGENTA}.back${RESET})."
    while :
    do
        DIR_PATH=`fetch_data_from_user 'DirPath'`
        if [ $? -ne 0 ]; then
            echo; info_msg "Aborting action."
            return 1
        fi
        check_directory_exists "$DIR_PATH"
        if [ $? -ne 0 ]; then
            warning_msg "Directory (${RED}$DIR_PATH${RESET}) does not exists."
            echo; continue
        fi; break
    done
    set_report_directory "$DIR_PATH"
    EXIT_CODE=$?
    echo; if [ $EXIT_CODE -ne 0 ]; then
        nok_msg "Something went wrong."\
            "Could not set (${RED}$DIR_PATH${RESET}) as"\
            "(${BLUE}$SCRIPT_NAME${RESET}) dazzle report directory."
    else
        ok_msg "Successfully set dazzle report directory (${GREEN}$DIR_PATH${RESET})."
    fi
    return $EXIT_CODE
}

function action_set_target_directory () {
    echo; info_msg "Type absolute directory path or (${MAGENTA}.back${RESET})."
    while :
    do
        DIR_PATH=`fetch_data_from_user 'DirPath'`
        if [ $? -ne 0 ]; then
            echo; info_msg "Aborting action."
            return 1
        fi
        check_directory_exists "$DIR_PATH"
        if [ $? -ne 0 ]; then
            warning_msg "Directory (${RED}$DIR_PATH${RESET}) does not exists."
            echo; continue
        fi; break
    done
    set_target_directory "$DIR_PATH"
    EXIT_CODE=$?
    echo; if [ $EXIT_CODE -ne 0 ]; then
        nok_msg "Something went wrong."\
            "Could not set (${RED}$DIR_PATH${RESET}) as"\
            "(${BLUE}$SCRIPT_NAME${RESET}) target directory."
    else
        ok_msg "Successfully set target directory (${GREEN}$DIR_PATH${RESET})."
    fi
    return $EXIT_CODE
}

function action_set_target_file () {
    echo; info_msg "Type absolute file path or (${MAGENTA}.back${RESET})."
    while :
    do
        FILE_PATH=`fetch_data_from_user 'FilePath'`
        if [ $? -ne 0 ]; then
            echo; info_msg "Aborting action."
            return 1
        fi
        check_file_exists "$FILE_PATH"
        if [ $? -ne 0 ]; then
            warning_msg "File (${RED}$FILE_PATH${RESET}) does not exists."
            echo; continue
        fi; break
    done
    set_target_file "$FILE_PATH"
    EXIT_CODE=$?
    echo; if [ $EXIT_CODE -ne 0 ]; then
        nok_msg "Something went wrong."\
            "Could not set (${RED}$FILE_PATH${RESET}) as"\
            "(${BLUE}$SCRIPT_NAME${RESET}) target file."
    else
        ok_msg "Successfully set target file (${GREEN}$FILE_PATH${RESET})."
    fi
    return $EXIT_CODE
}

function action_set_autocommit_on () {
    echo; fetch_ultimatum_from_user \
        "${YELLOW}Are you sure about this? Y/N${RESET}"
    if [ $? -ne 0 ]; then
        echo; info_msg "Aborting action."
    fi
    set_autocommit_flag 'on'
    EXIT_CODE=$?
    echo; if [ $EXIT_CODE -ne 0 ]; then
        nok_msg "Something went wrong."\
            "Could not set (${RED}$SCRIPT_NAME${RESET}) autocommit flag"\
            "to (${RED}ON${RESET})."
    else
        ok_msg "Succesfully set (${BLUE}$SCRIPT_NAME${RESET}) autocommit flag"\
            "to (${GREEN}ON${RESET})."
    fi
    return $EXIT_CODE
}

function action_set_autocommit_off () {
    echo; fetch_ultimatum_from_user \
        "${YELLOW}Are you sure about this? Y/N${RESET}"
    if [ $? -ne 0 ]; then
        echo; info_msg "Aborting action."
    fi
    set_autocommit_flag 'off'
    EXIT_CODE=$?
    echo; if [ $EXIT_CODE -ne 0 ]; then
        nok_msg "Something went wrong."\
            "Could not set (${RED}$SCRIPT_NAME${RESET}) autocommit flag"\
            "to (${RED}OFF${RESET})."
    else
        ok_msg "Succesfully set (${BLUE}$SCRIPT_NAME${RESET}) autocommit flag"\
            "to (${RED}OFF${RESET})."
    fi
    return $EXIT_CODE
}

function action_set_report_on () {
    echo; fetch_ultimatum_from_user \
        "${YELLOW}Are you sure about this? Y/N${RESET}"
    if [ $? -ne 0 ]; then
        echo; info_msg "Aborting action."
    fi
    set_report_flag 'on'
    EXIT_CODE=$?
    echo; if [ $EXIT_CODE -ne 0 ]; then
        nok_msg "Something went wrong."\
            "Could not set (${RED}$SCRIPT_NAME${RESET}) report flag"\
            "to (${RED}ON${RESET})."
    else
        ok_msg "Succesfully set (${BLUE}$SCRIPT_NAME${RESET}) report flag"\
            "to (${GREEN}ON${RESET})."
    fi
    return $EXIT_CODE
}

function action_set_report_off () {
    echo; fetch_ultimatum_from_user \
        "${YELLOW}Are you sure about this? Y/N${RESET}"
    if [ $? -ne 0 ]; then
        echo; info_msg "Aborting action."
    fi
    set_report_flag 'off'
    EXIT_CODE=$?
    echo; if [ $EXIT_CODE -ne 0 ]; then
        nok_msg "Something went wrong."\
            "Could not set (${RED}$SCRIPT_NAME${RESET}) report flag"\
            "to (${RED}OFF${RESET})."
    else
        ok_msg "Succesfully set (${BLUE}$SCRIPT_NAME${RESET}) report flag"\
            "to (${RED}OFF${RESET})."
    fi
    return $EXIT_CODE
}

function action_edit_directory_paths () {
    if [ -z "${MD_IMPORTS['directory-paths']}" ]; then
        echo; warning_msg "No file imported."
        return 0
    fi
    action_edit_imported_file 'directory-paths'
    return $?
}

function action_edit_file_paths () {
    if [ -z "${MD_IMPORTS['file-paths']}" ]; then
        echo; warning_msg "No file imported."
        return 0
    fi
    action_edit_imported_file 'file-paths'
    return $?
}

function action_import_file_paths () {
    action_import_file 'file-paths'
    return $?
}

function action_import_directory_paths () {
    action_import_file 'directory-paths'
    return $?
}


