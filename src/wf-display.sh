#!/bin/bash
#
# Regards, the Alveare Solutions society.
#
# DISPLAY

function display_war_factory_banner () {
    figlet -f lean -w 1000 "$SCRIPT_NAME" > "${MD_DEFAULT['tmp-file']}"
    clear; echo -n "${RED}`cat ${MD_DEFAULT['tmp-file']}`${RESET}
    "
    echo -n > ${MD_DEFAULT['tmp-file']}
    return 0
}

function display_formatted_settings () {
    display_formatted_setting_conf_file
    display_formatted_setting_log_file
    display_formatted_setting_temporary_file
    display_formatted_setting_file_editor
    display_formatted_setting_language
    display_formatted_setting_target_directory
    display_formatted_setting_target_file
    display_formatted_setting_imported_directory_paths
    display_formatted_setting_imported_file_paths
    display_formatted_setting_report_directory
    display_formatted_setting_log_lines
    display_formatted_setting_silent
    display_formatted_setting_report_generator
    display_formatted_setting_auto_commit
    display_formatted_setting_safety
    return 0
}

function display_war_factory_settings () {
    display_formatted_settings | column
    echo; return 0
}

function display_formatted_setting_report_directory () {
    if [ -z "${MD_DEFAULT['report-dir']}" ]; then
        return 1
    fi
    echo "[ ${CYAN}Report Directory${RESET}    ]: ${BLUE}${MD_DEFAULT['report-dir']}${RESET}"
    return $?
}

function display_formatted_setting_conf_file () {
    if [ -z "${MD_DEFAULT['conf-file']}" ]; then
        return 1
    fi
    echo "[ ${CYAN}Conf File${RESET}           ]: ${YELLOW}${MD_DEFAULT['conf-file']}${RESET}"
    return $?
}

function display_formatted_setting_log_file () {
    if [ -z "${MD_DEFAULT['log-file']}" ]; then
        return 1
    fi
    echo "[ ${CYAN}Log File${RESET}            ]: ${YELLOW}${MD_DEFAULT['log-file']}${RESET}"
    return $?
}

function display_formatted_setting_temporary_file () {
    if [ -z "${MD_DEFAULT['tmp-file']}" ]; then
        return 1
    fi
    echo "[ ${CYAN}Temporary File${RESET}      ]: ${YELLOW}${MD_DEFAULT['tmp-file']}${RESET}"
    return $?
}

function display_formatted_setting_file_editor () {
    if [ -z "${MD_DEFAULT['file-editor']}" ]; then
        return 1
    fi
    echo "[ ${CYAN}File Editor${RESET}         ]: ${MAGENTA}${MD_DEFAULT['file-editor']}${RESET}"
    return $?
}

function display_formatted_setting_language () {
    if [ -z "${MD_DEFAULT['language']}" ]; then
        return 1
    elif [[ "${MD_DEFAULT['language']}" == 'bash' ]]; then
        echo "[ ${CYAN}Language${RESET}            ]: ${MAGENTA}${MD_DEFAULT['language']} - ${RED}Not yet supported${RESET}"
    else
        echo "[ ${CYAN}Language${RESET}            ]: ${MAGENTA}${MD_DEFAULT['language']}${RESET}"
    fi
    return $?
}

function display_formatted_setting_target_directory () {
    if [ -z "${MD_DEFAULT['target-dir']}" ]; then
        echo "[ ${RED}Target Directory${RESET}    ]: ${RED}No directory specified${RESET}"
        return 1
    fi
    echo "[ ${CYAN}Target Directory${RESET}    ]: ${BLUE}${MD_DEFAULT['target-dir']}${RESET}"
    return $?
}

function display_formatted_setting_target_file () {
    if [ -z "${MD_DEFAULT['target-file']}" ]; then
        echo "[ ${RED}Target File${RESET}         ]: ${RED}No file specified${RESET}"
        return 1
    fi
    echo "[ ${CYAN}Target File${RESET}         ]: ${YELLOW}${MD_DEFAULT['target-file']}${RESET}"
    return $?
}

function display_formatted_setting_imported_directory_paths () {
    if [ -z "${MD_IMPORTS['directory-paths']}" ]; then
        echo "[ ${RED}Imported Dir Paths${RESET}  ]: ${RED}No target directory paths imported${RESET}"
        return 1
    fi
    echo "[ ${CYAN}Imported Dir Paths${RESET}  ]: ${YELLOW}${MD_IMPORTS['directory-paths']}${RESET}"
    return $?
}

function display_formatted_setting_imported_file_paths () {
    if [ -z "${MD_IMPORTS['file-paths']}" ]; then
        echo "[ ${RED}Imported File Paths${RESET} ]: ${RED}No target file paths imported${RESET}"
        return 1
    fi
    echo "[ ${CYAN}Imported File Paths${RESET} ]: ${YELLOW}${MD_IMPORTS['file-paths']}${RESET}"
    return $?
}

function display_formatted_setting_log_lines () {
    if [ -z "${MD_DEFAULT['log-lines']}" ]; then
        return 1
    fi
    echo "[ ${CYAN}Log Lines${RESET}           ]: ${WHITE}${MD_DEFAULT['log-lines']}${RESET}"
    return $?
}

function display_formatted_setting_silent () {
    if [ -z "${MD_DEFAULT['silent']}" ]; then
        return 1
    fi
    echo "[ ${CYAN}Silent${RESET}              ]: `format_flag_colors ${MD_DEFAULT['silent']}`"
    return $?
}

function display_formatted_setting_report_generator () {
    if [ -z "${MD_DEFAULT['report']}" ]; then
        return 1
    fi
    echo "[ ${CYAN}Report Generator${RESET}    ]: `format_flag_colors ${MD_DEFAULT['report']}`"
    return $?
}

function display_formatted_setting_auto_commit () {
    if [ -z "${MD_DEFAULT['autocommit']}" ]; then
        return 1
    fi
    echo "[ ${CYAN}Auto Commit${RESET}         ]: `format_flag_colors ${MD_DEFAULT['autocommit']}`"
    return $?
}

function display_formatted_setting_safety () {
    if [ -z "$MD_SAFETY" ]; then
        return 1
    fi
    echo "[ ${CYAN}Safety${RESET}              ]: `format_flag_colors $MD_SAFETY`"
    return $?
}

