#!/bin/bash
#
# Regards, the Alveare Solutions society.
#
# LOADERS

function load_war_factory_config () {
    load_war_factory_script_name
    load_war_factory_prompt_string
    load_war_factory_safety
    load_settings_war_factory_default
    load_war_factory_logging_levels
    load_war_factory_cargo
    load_war_factory_import
    load_war_factory_dependencies
}

function load_apt_dependencies () {
    local DEPENDENCY_SET=( $@ )
    for dependency in ${DEPENDENCY_SET[@]}; do
        check_item_in_set "$dependency" ${MD_APT_DEPENDENCIES[@]}
        if [ $? -eq 0 ]; then
            continue
        fi
        MD_APT_DEPENDENCIES=( ${MD_APT_DEPENDENCIES[@]} $dependency )
    done
    return 0
}

function load_war_factory_dependencies () {
    echo "${WF_PIP3_DEPENDENCIES[@]}"
    load_apt_dependencies ${WF_APT_DEPENDENCIES[@]}
    load_pip3_dependencies ${WF_PIP3_DEPENDENCIES[@]}
    return $?
}

function load_war_factory_safety () {
    load_safety $WF_SAFETY
    return $?
}

function load_war_factory_prompt_string () {
    load_prompt_string "$WF_PS3"
    return $?
}

function load_war_factory_logging_levels () {
    load_logging_levels ${WF_LOGGING_LEVELS[@]}
    return $?
}

function load_war_factory_cargo () {
    for war_factory_cargo in ${!WF_CARGO[@]}; do
        load_cargo \
            "$war_factory_cargo" ${WF_CARGO[$war_factory_cargo]}
    done
    return $?
}

function load_settings_war_factory_default () {
    for war_factory_setting in ${!WF_DEFAULT[@]}; do
        load_default_setting \
            "$war_factory_setting" ${WF_DEFAULT[$war_factory_setting]}
    done
    return $?
}

function load_settings_war_factory_import () {
    for war_factory_import in ${!WF_IMPORTS[@]}; do
        war_factory_import \
            "$war_factory_import" ${WF_IMPORTS[$war_factory_import]}
    done
    return $?
}

function load_war_factory_script_name () {
    load_script_name "$WF_SCRIPT_NAME"
    return $?
}

# SETUP

function war_factory_project_setup () {
    lock_and_load
    load_war_factory_config
    create_war_factory_menu_controllers
    setup_war_factory_menu_controllers
}

function setup_war_factory_menu_controllers () {
    setup_war_factory_dependencies
    setup_main_menu_controller
    setup_log_viewer_menu_controller
    setup_settings_menu_controller
    setup_war_room_menu_controller
    done_msg "${BLUE}$SCRIPT_NAME${RESET} controller setup complete."
    return 0
}

# SETUP DEPENDENCIES

function setup_war_factory_dependencies () {
    apt_install_dependencies
    pip3_install_dependencies
    return $?
}

# WAR ROOM MENU SETUP

function setup_war_room_menu_controller () {
    setup_war_room_menu_option_start_war_factory
    setup_war_room_menu_option_view_dazzle_reports
    setup_war_room_menu_option_help
    setup_war_room_menu_option_back
    done_msg "(${CYAN}$WAR_ROOM_CONTROLLER_LABEL${RESET}) controller"\
        "option binding complete."
    return 0
}

function setup_war_room_menu_option_start_war_factory () {
    setup_menu_controller_action_option \
        "$WAR_ROOM_CONTROLLER_LABEL"  "Start-War-Factory" \
        'action_start_war_factory'
    return $?
}

function setup_war_room_menu_option_view_dazzle_reports () {
    setup_menu_controller_action_option \
        "$WAR_ROOM_CONTROLLER_LABEL"  "View-Dazzle-Reports" \
        'action_view_dazzle_reports'
    return $?
}

function setup_war_room_menu_option_help () {
    setup_menu_controller_action_option \
        "$WAR_ROOM_CONTROLLER_LABEL"  "Help" 'action_war_factory_help'
    return $?
}

function setup_war_room_menu_option_back () {
    setup_menu_controller_action_option \
        "$WAR_ROOM_CONTROLLER_LABEL"  "Back" 'action_back'
    return $?
}

# MAIN MENU SETUP

# TODO - Uncomment
function setup_main_menu_controller () {
    setup_main_menu_option_war_factory
    setup_main_menu_option_log_viewer
    setup_main_menu_option_control_panel
#   setup_main_menu_option_self_destruct
    setup_main_menu_option_back
    done_msg "${CYAN}$MAIN_CONTROLLER_LABEL${RESET} controller option"\
        "binding complete."
    return 0
}

function setup_main_menu_option_self_destruct () {
    setup_menu_controller_action_option \
        "$MAIN_CONTROLLER_LABEL"  "Self-Destruct" 'action_self_destruct'
    return $?
}

function setup_main_menu_option_war_factory () {
    setup_menu_controller_menu_option \
        "$MAIN_CONTROLLER_LABEL"  "War-Room" \
        "$WAR_ROOM_CONTROLLER_LABEL"
    return $?
}

function setup_main_menu_option_log_viewer () {
    setup_menu_controller_menu_option \
        "$MAIN_CONTROLLER_LABEL"  "Log-Viewer" \
        "$LOGVIEWER_CONTROLLER_LABEL"
    return $?
}

function setup_main_menu_option_control_panel () {
    setup_menu_controller_menu_option \
        "$MAIN_CONTROLLER_LABEL"  'Control-Panel' \
        "$SETTINGS_CONTROLLER_LABEL"
    return $?
}

function setup_main_menu_option_back () {
    setup_menu_controller_action_option \
        "$MAIN_CONTROLLER_LABEL"  'Back' 'action_back'
    return $?
}

# LOG VIEWER MENU SETUP

function setup_log_viewer_menu_controller () {
    setup_log_viewer_menu_option_display_tail
    setup_log_viewer_menu_option_display_head
    setup_log_viewer_menu_option_display_more
    setup_log_viewer_menu_option_clear_log_file
    setup_log_viewer_menu_option_back
    done_msg "${CYAN}$LOGVIEWER_CONTROLLER_LABEL${RESET} controller option"\
        "binding complete."
    return 0
}

function setup_log_viewer_menu_option_clear_log_file () {
    setup_menu_controller_action_option \
        "$LOGVIEWER_CONTROLLER_LABEL"  'Clear-Log' 'action_clear_log_file'
    return $?
}

function setup_log_viewer_menu_option_display_tail () {
    setup_menu_controller_action_option \
        "$LOGVIEWER_CONTROLLER_LABEL"  'Display-Tail' 'action_log_view_tail'
    return $?
}

function setup_log_viewer_menu_option_display_head () {
    setup_menu_controller_action_option \
        "$LOGVIEWER_CONTROLLER_LABEL"  'Display-Head' 'action_log_view_head'
    return $?
}

function setup_log_viewer_menu_option_display_more () {
    setup_menu_controller_action_option \
        "$LOGVIEWER_CONTROLLER_LABEL"  'Display-More' 'action_log_view_more'
    return $?
}

function setup_log_viewer_menu_option_back () {
    setup_menu_controller_action_option \
        "$LOGVIEWER_CONTROLLER_LABEL"  'Back' 'action_back'
    return $?
}

# SETTINGS MENU SETUP

function setup_settings_menu_controller () {
    setup_settings_menu_option_set_safety_off
    setup_settings_menu_option_set_safety_on
    setup_settings_menu_option_set_temporary_file
    setup_settings_menu_option_set_log_file
    setup_settings_menu_option_set_log_lines
    setup_settings_menu_option_set_file_editor
    setup_settings_menu_option_set_silent_on
    setup_settings_menu_option_set_silent_off
    setup_settings_menu_option_install_dependencies
    setup_settings_menu_option_back
    setup_settings_menu_option_set_report_on
    setup_settings_menu_option_set_report_off
    setup_settings_menu_option_set_autocommit_on
    setup_settings_menu_option_set_autocommit_off
    setup_settings_menu_option_import_directory_paths
    setup_settings_menu_option_import_file_paths
    setup_settings_menu_option_edit_directory_paths
    setup_settings_menu_option_edit_file_paths
    setup_settings_menu_option_set_report_directory
    setup_settings_menu_option_set_language
    setup_settings_menu_option_set_target_file
    setup_settings_menu_option_set_target_directory
    done_msg "${CYAN}$SETTINGS_CONTROLLER_LABEL${RESET} controller option"\
        "binding complete."
    return 0
}

function setup_settings_menu_option_set_target_file () {
    setup_menu_controller_action_option \
        "$SETTINGS_CONTROLLER_LABEL" 'Set-Target-File' \
        'action_set_target_file'
    return $?
}

function setup_settings_menu_option_set_target_directory () {
    setup_menu_controller_action_option \
        "$SETTINGS_CONTROLLER_LABEL" 'Set-Target-Directory' \
        'action_set_target_directory'
    return $?
}

function setup_settings_menu_option_set_language () {
    setup_menu_controller_action_option \
        "$SETTINGS_CONTROLLER_LABEL" 'Set-Language' \
        'action_set_programming_language'
    return $?
}

function setup_settings_menu_option_set_report_on () {
    setup_menu_controller_action_option \
        "$SETTINGS_CONTROLLER_LABEL" 'Set-Report-ON' \
        'action_set_report_on'
    return $?
}

function setup_settings_menu_option_set_report_off () {
    setup_menu_controller_action_option \
        "$SETTINGS_CONTROLLER_LABEL" 'Set-Report-OFF' \
        'action_set_report_off'
    return $?
}

function setup_settings_menu_option_set_autocommit_on () {
    setup_menu_controller_action_option \
        "$SETTINGS_CONTROLLER_LABEL" 'Set-AutoCommit-ON' \
        'action_set_autocommit_on'
    return $?
}

function setup_settings_menu_option_set_autocommit_off () {
    setup_menu_controller_action_option \
        "$SETTINGS_CONTROLLER_LABEL" 'Set-AutoCommit-OFF' \
        'action_set_autocommit_off'
    return $?
}

function setup_settings_menu_option_import_directory_paths () {
    setup_menu_controller_action_option \
        "$SETTINGS_CONTROLLER_LABEL" 'Import-Directory-Paths' \
        'action_import_directory_paths'
    return $?
}

function setup_settings_menu_option_import_file_paths () {
    setup_menu_controller_action_option \
        "$SETTINGS_CONTROLLER_LABEL" 'Import-File-Paths' \
        'action_import_file_paths'
    return $?
}

function setup_settings_menu_option_edit_directory_paths () {
    setup_menu_controller_action_option \
        "$SETTINGS_CONTROLLER_LABEL" 'Edit-Directory-Paths' \
        'action_edit_directory_paths'
    return $?
}

function setup_settings_menu_option_edit_file_paths () {
    setup_menu_controller_action_option \
        "$SETTINGS_CONTROLLER_LABEL" 'Edit-File-Paths' \
        'action_edit_file_paths'
    return $?
}

function setup_settings_menu_option_set_report_directory () {
    setup_menu_controller_action_option \
        "$SETTINGS_CONTROLLER_LABEL" 'Set-Report-Directory' \
        'action_set_dazzle_report_directory'
    return $?
}

function setup_settings_menu_option_set_silent_on () {
    setup_menu_controller_action_option \
        "$SETTINGS_CONTROLLER_LABEL" 'Set-Silent-ON' \
        'action_set_silent_flag_on'
    return $?
}

function setup_settings_menu_option_set_silent_off () {
    setup_menu_controller_action_option \
        "$SETTINGS_CONTROLLER_LABEL" 'Set-Silent-OFF' \
        'action_set_silent_flag_off'
    return $?
}

function setup_settings_menu_option_set_safety_on () {
    setup_menu_controller_action_option \
        "$SETTINGS_CONTROLLER_LABEL" 'Set-Safety-ON' \
        'action_set_safety_on'
    return $?
}

function setup_settings_menu_option_set_safety_off () {
    setup_menu_controller_action_option \
        "$SETTINGS_CONTROLLER_LABEL" 'Set-Safety-OFF' \
        'action_set_safety_off'
    return $?
}

function setup_settings_menu_option_set_file_editor () {
    setup_menu_controller_action_option \
        "$SETTINGS_CONTROLLER_LABEL" 'Set-File-Editor' \
        'action_set_file_editor'
    return $?
}

function setup_settings_menu_option_set_temporary_file () {
    setup_menu_controller_action_option \
        "$SETTINGS_CONTROLLER_LABEL" 'Set-Temporary-File' \
        'action_set_temporary_file'
    return $?
}

function setup_settings_menu_option_set_log_file () {
    setup_menu_controller_action_option \
        "$SETTINGS_CONTROLLER_LABEL" 'Set-Log-File' \
        'action_set_log_file'
    return $?
}

function setup_settings_menu_option_set_log_lines () {
    setup_menu_controller_action_option \
        "$SETTINGS_CONTROLLER_LABEL" 'Set-Log-Lines' \
        'action_set_log_lines'
    return $?
}

function setup_settings_menu_option_install_dependencies () {
    setup_menu_controller_action_option \
        "$SETTINGS_CONTROLLER_LABEL" 'Install-Dependencies' \
        'action_install_dependencies'
    return $?
}

function setup_settings_menu_option_back () {
    setup_menu_controller_action_option \
        "$SETTINGS_CONTROLLER_LABEL" 'Back' 'action_back'
    return $?
}

#
