#!/bin/bash
#
# Regards, the Alveare Solutions society.
#
# CREATORS

function create_war_factory_menu_controllers () {
    create_main_menu_controller
    create_war_room_menu_controller
    create_log_viewer_menu_cotroller
    create_settings_menu_controller
    done_msg "${BLUE}$SCRIPT_NAME${RESET} controller construction complete."
    return 0
}

function create_war_room_menu_controller () {
    create_menu_controller "$WAR_ROOM_CONTROLLER_LABEL" \
        "${RED}$WAR_ROOM_CONTROLLER_DESCRIPTION${RESET}" \
        "$WAR_ROOM_CONTROLLER_OPTIONS"
    return $?
}

function create_main_menu_controller () {
    create_menu_controller "$MAIN_CONTROLLER_LABEL" \
        "${CYAN}$MAIN_CONTROLLER_DESCRIPTION${RESET}" "$MAIN_CONTROLLER_OPTIONS"
    return $?
}

function create_log_viewer_menu_cotroller () {
    create_menu_controller "$LOGVIEWER_CONTROLLER_LABEL" \
        "${CYAN}$LOGVIEWER_CONTROLLER_DESCRIPTION${RESET}" \
        "$LOGVIEWER_CONTROLLER_OPTIONS"
    return $?
}

function create_settings_menu_controller () {
    create_menu_controller "$SETTINGS_CONTROLLER_LABEL" \
        "${CYAN}$SETTINGS_CONTROLLER_DESCRIPTION${RESET}" \
        "$SETTINGS_CONTROLLER_OPTIONS"

    info_msg "Setting ${CYAN}$SETTINGS_CONTROLLER_LABEL${RESET} extented"\
        "banner function ${MAGENTA}display_war_factory_settings${RESET}..."
    set_menu_controller_extended_banner "$SETTINGS_CONTROLLER_LABEL" \
        'display_war_factory_settings'

    return 0
}

