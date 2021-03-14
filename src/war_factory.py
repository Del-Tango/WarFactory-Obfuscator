#!/usr/bin/python3
#
# Regards, the Alveare Solutions society.
#
import pysnooper
import datetime
import os
import re
import json
import optparse
import logging

from wf_parser.wf_python_parser import WFPythonParser
from wf_scrambler.wf_python_scrambler import WFPythonScrambler

# SETUP FIELDS

SCRIPT_NAME = 'WarFactory'
VERSION = 'Citadel Station'
LOG_FILE_PATH = ''
LOG_FORMAT = '[ %(asctime)s ] %(name)s [ %(levelname)s ] - %(filename)s - '\
    '%(lineno)d: %(funcName)s - %(message)s'
DATETIME_FORMAT = '%d-%m-%Y %H:%M:%S'
GENERATE_REPORTS = 'off' #(on | off)
SILENT = 'off' #(on | off)
SAFETY = 'on' #(on | off)
REPORT_DIRECTORY = ''
LANGUAGE = 'python' #(python | bash)
TARGET_PATHS = {
    'file': list(),
    'directory': list(),
}
YES = 'on' #(on | off)

# LOGGING

def log_init(log_name=__name__):
    log = logging.getLogger(log_name)
    try:
        log.setLevel(logging.DEBUG)
        file_handler = logging.FileHandler(LOG_FILE_PATH, 'a')
        formatter = logging.Formatter(LOG_FORMAT, DATETIME_FORMAT)
        file_handler.setFormatter(formatter)
        log.addHandler(file_handler)
    except:
        pass
    return log

log = log_init(SCRIPT_NAME)

# FETCHERS

def fetch_ultimatum_from_user(message):
    log.debug('')
    yes_answers = ['y', 'Y', 'yes', 'YES', 'Yes']
    no_answers = ['n', 'N', 'no', 'NO', 'No']
    while True:
        if YES == 'on':
            return True
        ultimatum = input(message + ' Y/N> ')
        if ultimatum not in yes_answers and ultimatum not in no_answers:
            stdout_msg('')
            warning_invalid_user_input(ultimatum)
        elif ultimatum in yes_answers:
            return True
        elif ultimatum in no_answers:
            return False

def fetch_file_content_as_string(file_path, line_range):
    log.debug('')
    try:
        file_obj = open(os.path.abspath(file_path))
    except Exception as e:
        stdout_msg('[ NOK ]: Could not open file ({}).'.format(file_path))
        return
    file_content_string = ""
    # [ NOTE ]: Scan current file line range
    for line_number, line in enumerate(file_obj):
        if line_number >= line_range[0] and line_number < line_range[1]:
            file_content_string += line
    file_obj.close()
    return file_content_string

def fetch_number_of_lines_in_file(file_path):
    try:
        return len(open(str(file_path)).readlines())
    except Exception as e:
        stdout_msg(
            '[ NOK ]: Could not fetch file ({}) line count.'.format(file_path)
        )
        return 0

# SETTERS
# CHECKERS

def check_directory_exists(dir_path):
    return os.path.isdir(dir_path)

def check_safety_flag_on():
    log.debug('')
    stdout_msg('[ INFO ]: {} safety flag is ({}).'.format(
        SCRIPT_NAME, SAFETY
    ))
    return SAFETY == 'on'

def check_silent_flag_on():
    log.debug('')
    stdout_msg('[ INFO ]: {} silent flag is ({}).'.format(
        SCRIPT_NAME, SILENT
    ))
    return SILENT == 'on'

def check_dazzle_reports_flag_on():
    log.debug('')
    stdout_msg('[ INFO ]: {} Dazzle reports are ({}).'.format(
        SCRIPT_NAME, GENERATE_REPORTS
    ))
    return GENERATE_REPORTS == 'on'

# UPDATERS
# CREATORS

def create_file(file_path, content=''):
    log.debug('')
    try:
        with open(file_path, 'w') as f:
            f.write(content)
    except Exception as e:
        return False
    return file_path

def create_command_line_parser():
    log.debug('')
    parser = optparse.OptionParser(
        '%prog \ \n'
        '   -f <file-path                            value-(/file/path1.py,/file/path2.py)> \\\n'
        '   -d <directory-path                       value-(/dir/path/py-package1,/dir/path/py-package2)> \\\n'
        '   -l <log-file-path                        value-(/file/path.log)> \\\n'
        '   -R <report-file-path    implies-(-r on)  value-(/file/path.dazzle)> \\\n'
        '   -L <language                             value-(python | bash)> \\\n'
        '   -s <silent-stdout-flag                   value-(on | off)> \\\n'
        '   -r <report-flag                          value-(on | off)> \\\n'
        '   -S <safety-flag                          value-(on | off)> \\\n'
        '   -y <yes-flag                             value-(on | off)>'
    )
    return parser

def create_war_factory_parser(**kwargs):
    log.debug('')
    parser = WFPythonParser(
        file_path=kwargs.get('file_path', str()),
        log_name=kwargs.get('log_name', __name__),
        silent=kwargs.get('silent', True),
        silent_warnings=kwargs.get('silent', True),
        silent_errors=kwargs.get('silent', True),
        dazzle_report=kwargs.get('dazzle_report', False),
        report_file_path=kwargs.get('report_file_path', str()),
    )
    if not parser:
        return error_could_not_create_war_factory_parser(parser, kwargs)
    else:
        stdout_msg("[ OK ]: Spawned {} {} parser.".format(
            SCRIPT_NAME, LANGUAGE
        ))
    return parser

def create_war_factory_scrambler(**kwargs):
    log.debug('')
    scrambler = WFPythonScrambler(
        file_path=kwargs.get('file_path', str()),
        log_name=kwargs.get('log_name', __name__),
        parsed_content={},
        silent=kwargs.get('silent', True),
        silent_warnings=kwargs.get('silent', True),
        silent_errors=kwargs.get('silent', True),
        safety=kwargs.get('safety', True),
        dazzle_report=kwargs.get('dazzle_report', False),
        report_file_path=kwargs.get('report_file_path', str())
    )
    if not scrambler:
        return error_could_not_create_war_factory_scrambler(scrambler, kwargs)
    else:
        stdout_msg("[ OK ]: Spawned {} {} obfuscator.".format(
            SCRIPT_NAME, LANGUAGE
        ))
    return scrambler

# PROCESSORS

def process_yes_argument(parser, options):
    log.debug('')
    global YES
    flag = options.yes
    if flag == None:
        stdout_msg(
            '[ WARNING ]: No YES flag provided. '
            'Defaulting to ({}).'.format(YES)
        )
        return False
    YES = flag
    stdout_msg(
        '[ OK ]: YES flag setup ({}).'.format(YES)
    )
    return YES

def process_silent_flag_argument(parser, options):
    log.debug('')
    global SILENT
    flag = options.silent_flag
    if flag == None:
        stdout_msg(
            '[ WARNING ]: No silent flag provided. '
            'Defaulting to ({}).'.format(SILENT)
        )
        return False
    SILENT = flag
    stdout_msg(
        '[ OK ]: Silent flag setup ({}).'.format(SILENT)
    )
    return SILENT

def process_safety_flag_argument(parser, options):
    log.debug('')
    global SAFETY
    flag = options.safety_flag
    if flag == None:
        stdout_msg(
            '[ WARNING ]: No safety flag provided. '
            'Defaulting to ({}).'.format(SAFETY)
        )
        return False
    SAFETY = flag
    stdout_msg(
        '[ OK ]: Safety flag setup ({}).'.format(SAFETY)
    )
    return SAFETY

def process_report_flag_argument(parser, options):
    log.debug('')
    global GENERATE_REPORTS
    flag = options.report_flag
    if flag == None:
        stdout_msg(
            '[ WARNING ]: No report flag provided. '
            'Defaulting to ({}).'.format(GENERATE_REPORTS)
        )
        return False
    GENERATE_REPORTS = flag
    stdout_msg(
        '[ OK ]: Report flag setup ({}).'.format(GENERATE_REPORTS)
    )
    return GENERATE_REPORTS

def process_directory_path_argument(parser, options):
    log.debug('')
    global TARGET_PATHS
    dir_paths = options.directory_path
    if dir_paths == None:
        stdout_msg(
            '[ WARNING ]: No directory path provided. '
            'Defaulting to ({}).'.format(TARGET_PATHS['directory'])
        )
        return False
    TARGET_PATHS['directory'] += [
        dr_path for dr_path in dir_paths.split(',')
        if dr_path not in TARGET_PATHS['directory']
    ]
    stdout_msg(
        '[ OK ]: Directory path setup ({}).'.format(dir_paths)
    )
    return TARGET_PATHS['directory']

def process_file_path_argument(parser, options):
    log.debug('')
    global TARGET_PATHS
    file_paths = options.file_path
    if file_paths == None:
        stdout_msg(
            '[ WARNING ]: No file path provided. '
            'Defaulting to ({}).'.format(TARGET_PATHS['file'])
        )
        return False
    TARGET_PATHS['file'] += [
        fl_path for fl_path in file_paths.split(',')
        if fl_path not in TARGET_PATHS['file']
    ]
    stdout_msg(
        '[ OK ]: File path setup ({}).'.format(file_paths)
    )
    return TARGET_PATHS['file']

def process_report_directory_argument(parser, options):
    log.debug('')
    global REPORT_DIRECTORY
    dir_path = options.report_directory
    if dir_path == None:
        stdout_msg(
            '[ WARNING ]: No report directory path provided. '
            'Defaulting to ({}).'.format(REPORT_DIRECTORY)
        )
        return False
    REPORT_DIRECTORY = dir_path
    stdout_msg(
        '[ OK ]: Report directory path setup ({}).'.format(REPORT_DIRECTORY)
    )
    return REPORT_DIRECTORY

def process_log_file_path_argument(parser, options):
    global LOG_FILE_PATH
    global log
    log.debug('')
    file_path = options.log_file_path
    if file_path == None:
        stdout_msg(
            '[ WARNING ]: No log file path provided. '
            'Defaulting to ({}).'.format(LOG_FILE_PATH)
        )
        return False
    LOG_FILE_PATH = file_path
    log = log_init(log_name=SCRIPT_NAME)
    stdout_msg(
        '[ OK ]: Log file path setup ({}).'.format(LOG_FILE_PATH)
    )
    return LOG_FILE_PATH

def process_language_argument(parser, options):
    log.debug('')
    global LANGUAGE
    lang = options.language
    if lang == None:
        stdout_msg(
            '[ WARNING ]: No programming language provided. '
            'Defaulting to ({}).'.format(LANGUAGE)
        )
        return False
    LANGUAGE = lang
    stdout_msg(
        '[ OK ]: Programming language setup ({}).'.format(LANGUAGE)
    )
    return LANGUAGE

def process_command_line_options(parser):
    (options, args) = parser.parse_args()
    # [ NOTE ]: If you trully want to be covert, process silent_flag first
    processed = {
        'silent_flag': process_silent_flag_argument(parser, options),
        'safety_flag': process_safety_flag_argument(parser, options),
        'report_flag': process_report_flag_argument(parser, options),
        'directory_path': process_directory_path_argument(parser, options),
        'file_path': process_file_path_argument(parser, options),
        'report_directory': process_report_directory_argument(parser, options),
        'log_file_path': process_log_file_path_argument(parser, options),
        'language': process_language_argument(parser, options),
        'yes': process_yes_argument(parser, options),
    }
    return processed

# GENERAL

def generate_dazzle_report_file_name(file_path):
    log.debug('')
    file_name = os.path.basename(file_path)
    timestamp = datetime.datetime.now().strftime(DATETIME_FORMAT.replace(' ', '-'))
    suffix = 'dazzle'
    report_file_name = timestamp + '-' + file_name.strip(',py') + suffix
    return report_file_name

# SEARCH

def search_shell_files_in_directory(path):
    shell_files, file_list = [], os.listdir(path)
    for file_name in file_list:
        # [ NOTE ]: Check if file is a directory
        if os.path.isdir(path + "/" + file_name):
            # [ NOTE ]: Recursive call to search() for each directory in path
            shell_files.extend(search(path + "/" + file_name))
        # [ NOTE ]: Check for python files by extension
        elif file_name[-3:] == ".sh":
            shell_files.append(path + "/" + file_name)
    return shell_files

#@pysnooper.snoop()
def search_python_files_in_directory(path):
    python_files, file_list = [], os.listdir(path)
    for file_name in file_list:
        # [ NOTE ]: Check if file is a directory
        if os.path.isdir(path + "/" + file_name):
            # [ NOTE ]: Recursive call to search() for each directory in path
            python_files.extend(search(path + "/" + file_name))
        # [ NOTE ]: Check for python files by extension
        elif file_name[-3:] == ".py":
            python_files.append(path + "/" + file_name)
    return python_files

# PARSERS

def add_command_line_parser_options(parser):
    parser.add_option(
        '-S', dest='safety_flag', type='string',
        help='{} safety flag (on | off).'.format(SCRIPT_NAME)
    )
    parser.add_option(
        '-s', dest='silent_flag', type='string',
        help='STDOUT silence flag (on | off).'
    )
    parser.add_option(
        '-r', dest='report_flag', type='string',
        help='Dazzle report generator flag (on | off).'
    )
    parser.add_option(
        '-f', dest='file_path', type='string',
        help='Python file to dazzle.'
    )
    parser.add_option(
        '-d', dest='directory_path', type='string',
        help='Directory in which to search for python files to dazzle.'
    )
    parser.add_option(
        '-l', dest='log_file_path', type='string',
        help='{} log file path.'.format(SCRIPT_NAME)
    )
    parser.add_option(
        '-L', dest='language', type='string',
        help='Programming language.'
    )
    parser.add_option(
        '-R', dest='report_directory', type='string',
        help='{} dazzle report directory.'.format(SCRIPT_NAME)
    )
    parser.add_option(
        '-y', dest='yes', type='string',
        help='YES - Switch for automatic user commit.'
    )
    return parser

#@pysnooper.snoop()
def parse_command_line_arguments():
    parser = create_command_line_parser()
    add_parser_options = add_command_line_parser_options(parser)
    return process_command_line_options(parser)

def stdout_msg(message):
    log.debug('')
    if SILENT == 'on':
        return False
    print(message)
    return True

# HANDLERS

# TODO
def handle_bash_file_obfuscate(file_path, parser, scrambler):
    log.debug('TODO - Under construction, building...')
    return False

def handle_bash_directory_obfuscate(file_path, parser, scrambler):
    log.debug('')
    if not check_directory_exists(dir_path):
        return warning_directory_does_not_exist(dir_path)
    shell_files = search_shell_files_in_directory(dir_path)
    TARGET_PATHS['file'] += [
        sh_fl for sh_fl in shell_files if sh_fl not in TARGET_PATHS['file']
    ]
    return True

def handle_python_directory_obfuscate(dir_path, parser, scrambler):
    log.debug('')
    if not check_directory_exists(dir_path):
        return warning_directory_does_not_exist(dir_path)
    python_files = search_python_files_in_directory(dir_path)
    TARGET_PATHS['file'] += [
        py_fl for py_fl in python_files if py_fl not in TARGET_PATHS['file']
    ]
    return True

def handle_python_file_obfuscate(file_path, parser, scrambler):
    log.debug('')
    parser.cleanup()
    set_path = parser.set_file_path(file_path)
    if not set_path:
        return set_path
    dazzle_report_file_name = REPORT_DIRECTORY + '/' \
        + generate_dazzle_report_file_name(file_path)
    create_file(
        dazzle_report_file_name,
        '_____________________________________________________________________'
        '___________\n\n'
        '   Dazzle Report - {}\n'
        '_____________________________________________________________________'
        '___________\n'.format(file_path)
    )


    parser.set_dazzle_file_path(dazzle_report_file_name)
    stdout_msg('\n[ {} ]: Scanning file ({})...\n'.format(
        SCRIPT_NAME, file_path
    ))
    parser.scan()
    stdout_msg('\n[ {} ]: Parsed file ({}) content:'.format(
        SCRIPT_NAME, file_path
    ))
    parser.display_formatted_content()
    scrambler.cleanup()
    scrambler.set_dazzle_file_path(dazzle_report_file_name)
    scrambler.set_file_path(file_path)
    scrambler.set_parsed_content(parser.content)
    stdout_msg('\n[ {} ]: Obfuscating ({}) content...\n'.format(
        SCRIPT_NAME, file_path
    ))
    scrambler.start_scramblers()
    stdout_msg('[ {} ]: Scrambled ({}) content:'.format(
        SCRIPT_NAME, file_path
    ))
    scrambler.display_formatted_scrambled_content()
    stdout_msg('\n[ {} ]: Staged file ({}) state:\n'.format(
        SCRIPT_NAME, file_path
    ))
    scrambler.display_staged_scrambled_content()
    commit = fetch_ultimatum_from_user(
        '\nAre you sure you want to commit file ({}) to disk?'.format(file_path)
    )
    if not commit:
        stdout_msg('\n[ {} ]: Aborting action.'.format(SCRIPT_NAME))
        return False
    write = scrambler.write_scrambled_content_to_file(
        scrambler.fetch_file_path(),
        scrambler.fetch_scrambled_content(),
        list(scrambler.fetch_file_lines_map().values())
    )
    if not write:
        return error_could_not_scramble_file_content(file_path)
    stdout_msg('\n[ {} ]: Successfully obfuscated file ({})!\n'.format(
        SCRIPT_NAME, file_path
    ))
    return True

# ACTIONS

# DISPLAY

def display_header():
    stdout_msg('''
____________________________________________________________________________

 *            *           *      {}     *           *            *
____________________________________________________v.{}_______
                   Regards, the Alveare Solutions society.
    '''.format(SCRIPT_NAME, VERSION))
    return True

# INIT

def bash_war_factory(parser, scrambler, **kwargs):
    log.debug('')
    for dir_path in TARGET_PATHS['directory']:
        handle_bash_directory_obfuscate(dir_path, parser, scrambler)
    for file_path in TARGET_PATHS['file']:
        handle_bash_file_obfuscate(file_path, parser, scrambler)
    return True

def python_war_factory(parser, scrambler, **kwargs):
    log.debug('')
    for dir_path in TARGET_PATHS['directory']:
        handle_python_directory_obfuscate(dir_path, parser, scrambler)
    for file_path in TARGET_PATHS['file']:
        handle_python_file_obfuscate(file_path, parser, scrambler)
    return True

def war_factory(parser, scrambler, **kwargs):
    log.debug('')
    handlers = {
        'python': python_war_factory,
        'bash': bash_war_factory,
    }
    if LANGUAGE not in handlers:
        return error_language_not_supported(set(handlers.keys()))
    return handlers[LANGUAGE](parser, scrambler, **kwargs)

def init_war_factory(**kwargs):
    log.debug('')
    parse_command_line_arguments()
    display_header()
    if not TARGET_PATHS['file'] and not TARGET_PATHS['directory']:
        return error_no_files_to_obfuscate(TARGET_PATHS)
    parser = create_war_factory_parser(
        log_name=kwargs.get('log_name', __name__),
        silent=True if SILENT == 'on' else False,
        dazzle_report=True if GENERATE_REPORTS == 'on' else False,
    )
    scrambler = create_war_factory_scrambler(
        log_name=kwargs.get('log_name', __name__),
        parsed_content=kwargs.get('parsed_content', dict()),
        silent=True if SILENT == 'on' else False,
        safety=True if SAFETY == 'on' else False,
        dazzle_report=True if GENERATE_REPORTS == 'on' else False,
    )
    return war_factory(parser, scrambler, **kwargs)

# WARNINGS

def warning_directory_does_not_exist(*args):
    return warning_msg(
        "Directory does not exist.", args
    )

def warning_invalid_user_input(*args):
    return warning_msg(
        'Invalid user input.', args
    )

def warning_msg(message, details):
    stdout_msg("[ WARNING ]: {} Details: {}.".format(message, details))
    return False

# ERRORS

def error_language_not_supported(*args):
    return error_msg(
        "Programming language ({}) not supported by ({}) version ({}).".format(
            LANGUAGE, SCRIPT_NAME, VERSION
        ), args
    )

def error_could_not_scramble_file_content(*args):
    return error_msg(
        "Something went wrong. Could not obfuscate file content.", args
    )

def error_no_files_to_obfuscate(*args):
    return error_msg(
        "No files provided to obfuscate.", args
    )

def error_could_not_create_war_factory_scrambler(*args):
    return error_msg(
        "Something went wrong. Could not create {} scrambler object.".format(
            SCRIPT_NAME,
        ), args
    )

def error_could_not_create_war_factory_parser(*args):
    return error_msg(
        "Something went wrong. Could not create {} parser object.".format(
            SCRIPT_NAME,
        ), args
    )

def error_msg(message, details):
    stdout_msg("[ ERROR ]: {} Details: {}.".format(message, details))
    return False


# MISCELLANEOUS

if __name__ == '__main__':

    init_war_factory(
        log_name=SCRIPT_NAME, silent=True if SILENT == 'on' else False,
        safety=True if SAFETY == 'on' else False, parsed_content={},
    )
