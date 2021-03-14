#!/bin/bash
#
# Regards, the Alveare Solutions society.
#
# INSTALLERS

function action_install_dependencies () {
   apt_install_dependencies
   pip3_install_dependencies
   return $?
}
