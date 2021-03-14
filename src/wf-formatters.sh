#!/bin/bash
#
# Regards, the Alveare Solutions society.
#
# FORMATTERS

function format_war_factory_cli_argument_string () {
    FILE_PATH_SET="${MD_DEFAULT['target-file']}"
    if [ ! -z "${MD_IMPORTS['file-paths']}" ]; then
        for file_path in `cat ${MD_IMPORTS['file-paths']}`; do
            FILE_PATH_SET="${FILE_PATH_SET},${file_path}"
        done
    fi
    DIR_PATH_SET=${MD_DEFAULT['target-directory']}
    if [ ! -z "${MD_IMPORTS['directory-paths']}" ]; then
        for dir_path in `cat ${MD_IMPORTS['directory-paths']}`; do
            DIR_PATH_SET="${DIR_PATH_SET},${dir_path}"
        done
    fi
    CLI_ARGUMENTS="
        -l ${MD_DEFAULT['log-file']}
        -s ${MD_DEFAULT['silent']}
        -S $MD_SAFETY
        -y ${MD_DEFAULT['autocommit']}
        -r ${MD_DEFAULT['report']}
        -R ${MD_DEFAULT['report-dir']}
        -L ${MD_DEFAULT['language']}"
    if [ ! -z "$FILE_PATH_SET" ]; then
        CLI_ARGUMENTS="$CLI_ARGUMENTS -f $FILE_PATH_SET"
    fi
    if [ ! -z "$DIR_PATH_SET" ]; then
        CLI_ARGUMENTS="$CLI_ARGUMENTS -d $DIR_PATH_SET"
    fi
    echo "$CLI_ARGUMENTS"
    return $?
}


