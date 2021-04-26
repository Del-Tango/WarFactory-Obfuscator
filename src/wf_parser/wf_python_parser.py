#!/usr/bin/python3
#
# Regards, the Alveare Solutions society.
#
#import pysnooper
import datetime
import os
import re
import json
import logging
import pysnooper

log = logging.getLogger(__name__)


class WFPythonParser(object):

    def __init__(self, *args, **kwargs):
        global log
        self.silent = kwargs.get('silent', True)
        self.silent_errors = kwargs.get('silent_errors', True)
        self.silent_warnings = kwargs.get('silent_warnings', True)
        self.file_path = kwargs.get('file_path', str())
        self.dazzle_report = kwargs.get('dazzle_report', False)
        self.report_file_path = kwargs.get('report_file_path', str())
        self.content = self.build_content_details()
        self.timestamp = None
        self.last_comment = self.build_last_comment_details()
        self.last_variable = self.build_last_variable_details()
        self.last_function = self.build_last_function_details()
        self.last_class = self.build_last_class_details()
        if kwargs.get('log_name'):
            log = logging.getLogger(kwargs['log_name'])

    # DUNDERS

    def __str__(self, *arg, **kwargs):
        log.debug('')
        response = self.fetch_parser_values()
        response.update({'object': 'WFPythonParser'})
        return str(response)

    # FETCHERS

    def fetch_dazzle_report_file_path(self):
        log.debug('')
        return self.report_file_path

    def fetch_parser_values(self):
        log.debug('')
        return self.__dict__

    def fetch_line_identation_level(self, file_line):
        log.debug('')
        level, segmented_line = 0, list(file_line)
        for character in segmented_line:
            if character != ' ':
                break
            level += 1
        return level

    def fetch_python_comment_regex(self):
        log.debug('')
        return '^\s{0,}#'

    def fetch_python_variable_declaration_regex(self):
        log.debug('')
        return "^(self\.|\s{0,}|' '){1,}[a-zA-Z0-9_]{1,} ="

    def fetch_python_function_declaration_regex(self):
        log.debug('')
        return '^\s{0,}def '

    def fetch_python_class_declaration_regex(self):
        log.debug('')
        return '^\s{0,}class '

    def fetch_number_of_lines_in_file(self, file_path):
        log.debug('')
        try:
            return len(open(str(file_path)).readlines())
        except Exception as e:
            self.error_could_not_fetch_file_line_count(file_path, e)
            return 0

    # SETTERS

    def set_dazzle_file_path(self, file_path):
        log.debug('')
        if not self.check_file_exists(file_path):
            return self.error_invalid_dazzle_report_file_path(file_path)
        self.report_file_path = file_path
        return True

    def set_last_scan_timestamp(self, timestamp):
        log.debug('')
        self.timestamp = timestamp
        return True

    def set_content_details(self, details):
        log.debug('')
        if not self.check_valid_content_map(details):
            return self.error_invalid_content_map(details, self.content)
        self.content = details
        return True

    def set_last_comment_details(self, details):
        log.debug('')
        if not self.check_valid_comment_map(details):
            return self.error_invalid_comment_map(details, self.last_comment)
        self.last_comment = details
        return True

    def set_last_variable_details(self, details):
        log.debug('')
        if not self.check_valid_variable_map(details):
            return self.error_invalid_variable_map(details, self.last_variable)
        self.last_variable = details
        return True

    def set_last_function_details(self, details):
        log.debug('')
        if not self.check_valid_function_map(details):
            return self.error_invalid_function_map(details, self.last_function)
        self.last_function = details
        return True

    def set_last_class_details(self, details):
        log.debug('')
        if not self.check_valid_class_map(details):
            return self.error_invalid_class_map(details, self.last_class)
        self.last_class = details
        return True

    def set_file_path(self, file_path):
        log.debug('')
        if not self.check_file_exists(file_path):
            return self.warning_file_does_not_exist(file_path)
        self.file_path = file_path
        return True

    # CHECKERS

    def check_dazzle_report_flag(self):
        log.debug('')
        return self.dazzle_report

    def check_file_line_contains(self, line):
        log.debug('')
        checkers = {
            'comment': self.check_line_commented(line),
            'class': self.check_line_has_declared_class(line),
            'function': self.check_line_has_declared_function(line),
            'variable': self.check_line_has_declared_variable(line),
        }
        contains = []
        for item in checkers:
            if not checkers[item]:
                continue
            contains.append(item)
        if len(contains) > 1:
            if 'function' in contains and 'variable' in contains \
                    and len(contains) == 2:
                return 'function'
            if 'class' in contains and 'variable' in contains \
                    and len(contains) == 2:
                return 'class'
        return False if not contains else contains[0]

    #@pysnooper.snoop()
    def check_code_declaration(self, line):
        log.debug('')
        word, words, level, whitespace = '', [], 0, 0
        for index in range(0,len(line)):
            character = line[index]
            if character == ' ':
                if word:
                    words.append(word)
                word = ''
                whitespace += 1
                continue
            elif not word and not words and whitespace:
                level = whitespace
            word += character
        if word:
            words.append(word)
        return {
            'words': words,
            'whitespaces': whitespace,
            'level': level,
            'class': self.check_class_declaration(words),
            'function': self.check_function_declaration(words),
            'variable': self.check_variable_declaration(words),
        }

#   @pysnooper.snoop()
    def check_class_declaration(self, words):
        log.debug('')
        search_cls = self.search_class_declaration(words)
        response = {
            'class_found': search_cls.get('class_found', False),
            'class_index': search_cls.get('class_index', 0),
            'class_name': search_cls.get('class_name', ''),
            'seen_words': search_cls.get('seen_words', []),
        }
        if not isinstance(response['class_index'], int):
            log.debug('Class declaration: ({})'.format(response))
            return response
        response['end_index'] = None if \
            not isinstance(response['class_index'], int) \
            else self.search_class_end_index(words, response['class_index'])
        search_argument = self.search_code_arguments(
            words, response['class_index'], response['end_index']
        )
        response['seen_words'] += search_argument['seen_words']
        response['args'] = search_argument.get('args', [])
        response['kwargs'] = search_argument.get('kwargs', [])
        log.debug('Class declaration: ({})'.format(response))
        return response

#   @pysnooper.snoop()
    def check_function_declaration(self, words):
        log.debug('')
        search_fnc = self.search_function_declaration(words)
        response = {
            'function_found': search_fnc.get('function_found', False),
            'function_index': search_fnc.get('function_index', 0),
            'function_name': search_fnc.get('function_name', ''),
            'seen_words': search_fnc.get('seen_words', []),
        }
        if not isinstance(response['function_index'], int):
            log.debug('Function declaration: ({})'.format(response))
            return response
        response['end_index'] = None if \
            not isinstance(response['function_index'], int) \
            else self.search_function_end_index(words, response['function_index'])
        search_argument = self.search_code_arguments(
            words, response['function_index'], response['end_index']
        )
        response['seen_words'] += search_argument['seen_words']
        response['args'] = search_argument.get('args', [])
        response['kwargs'] = search_argument.get('kwargs', [])
        log.debug('Function declaration: ({})'.format(response))
        return response

    def check_variable_declaration(self, words):
        log.debug('')
        search_var = self.search_variable_declaration(words)
        response = {
            'variable_found': search_var.get('variable_found', False),
            'variable_index': search_var.get('variable_index', 0),
            'variable_name': search_var.get('variable_name', ''),
            'seen_words': search_var.get('seen_words', []),
        }
        if not isinstance(response['variable_index'], int):
            return response
        response['end_index'] = None if \
            not isinstance(response['variable_index'], int) \
            else self.search_variable_end_index(words, response['variable_index'])
        return response

    def check_valid_content_map(self, content_map):
        log.debug('')
        valid_map = self.build_content_details()
        for item in valid_map:
            if item not in content_map:
                return False
        return True

    def check_valid_comment_map(self, comment_map):
        log.debug('')
        valid_map = self.build_last_comment_details()
        for item in valid_map:
            if item not in comment_map:
                return False
        return True

    def check_valid_variable_map(self, variable_map):
        log.debug('')
        valid_map = self.build_last_variable_details()
        for item in valid_map:
            if item not in variable_map:
                return False
        return True

    def check_valid_function_map(self, function_map):
        log.debug('')
        valid_map = self.build_last_function_details()
        for item in valid_map:
            if item not in function_map:
                return False
        return True

    def check_valid_class_map(self, class_map):
        log.debug('')
        valid_map = self.build_last_class_details()
        for item in valid_map:
            if item not in class_map:
                return False
        return True

    def check_file_exists(self, file_path):
        log.debug('')
        return os.path.isfile(file_path)

    def check_line_commented(self, file_line):
        log.debug('')
        regex = self.fetch_python_comment_regex()
        try:
            check = re.search(regex, file_line, re.IGNORECASE)
        except Exception as e:
            return self.error_could_not_check_if_line_commented(
                file_line, regex, e
            )
        return False if not check else True

    def check_line_has_declared_variable(self, file_line):
        log.debug('')
        regex = self.fetch_python_variable_declaration_regex()
        try:
            check = re.search(regex, file_line, re.IGNORECASE)
        except Exception as e:
            return self.error_could_not_check_if_line_has_declared_variable(
                file_line, regex, e
            )
        return False if not check else True

    def check_line_has_declared_function(self, file_line):
        log.debug('')
        regex = self.fetch_python_function_declaration_regex()
        try:
            check = re.search(regex, file_line, re.IGNORECASE)
        except Exception as e:
            return self.error_could_not_check_if_line_has_declared_function(
                file_line, regex, e
            )
        return False if not check else True

    def check_line_has_declared_class(self, file_line):
        log.debug('')
        regex = self.fetch_python_class_declaration_regex()
        try:
            check = re.search(regex, file_line, re.IGNORECASE)
        except Exception as e:
            return self.error_cold_not_check_if_line_has_declared_class(
                file_line, regex, e
            )
        return False if not check else True

    # UPDATERS

#   @pysnooper.snoop()
    def update_content(self, values):
        log.debug('')
        if not values.get('type'):
            return False
#           return self.error_unknown_content_type(values)
        updaters = {
            'comment': self.update_comment_map,
            'variable': self.update_variable_map,
            'function': self.update_function_map,
            'class': self.update_class_map,
        }
        if values['type'] not in updaters:
            return self.error_invalid_content_type(
                values, list(updaters.keys())
            )
        content_type, parent = values['type'], values.get('parent')
        del values['type']
        if not parent:
            return updaters[content_type](values)
        elif parent in ['class', 'function']:
            return updaters[parent](values)
        return updaters[content_type](values)

    def update_variable_map(self, variable_map):
        log.debug('')
        if not self.check_valid_variable_map(variable_map):
            return self.error_invalid_variable_map(variable_map)
        self.content['variables'].update({
            variable_map['name']: variable_map
        })
        return True

    def update_comment_map(self, comment_map):
        log.debug('')
        if not self.check_valid_comment_map(comment_map):
            return self.error_invalid_comment_map(comment_map)
        self.content['comments'].update({
            comment_map['line']: comment_map,
        })
        return True

    def update_function_map(self, function_map):
        log.debug('')
        if not self.check_valid_function_map(function_map):
            return self.error_invalid_function_map(function_map)
        self.content['functions'].update({
            function_map['name']: function_map
        })
        return True

#   @pysnooper.snoop()
    def update_class_map(self, class_map):
        log.debug('')
        if not self.check_valid_class_map(class_map):
            return self.error_invalid_class_map(class_map)
        self.content['classes'].update({
            class_map['name']: class_map
        })
        return True

    # BUILDERS

    def build_content_details(self, values=None):
        log.debug('')
        details = {
            'comments': dict(),
            'variables': dict(),
            'functions': dict(),
            'classes': dict(),
        }
        if isinstance(values, dict):
            details.update(values)
        return details

    def build_last_comment_details(self, values=None):
        log.debug('')
        details = {
            'body': str(),
            'line': int(),
            'level': int(),
            'content': list(),
        }
        if isinstance(values, dict):
            details.update(values)
        return details

    def build_last_variable_details(self, values=None):
        log.debug('')
        details = {
            'name': str(),
            'value': str(),
            'line': int(),
            'level': int(),
            'body': str(),
            'content': list(),
        }
        if isinstance(values, dict):
            details.update(values)
        return details

    def build_last_function_details(self, values=None):
        log.debug('')
        details = {
            'name': str(),
            'body': str(),
            'start_line': int(),
            'stop_line': int(),
            'function_index': int(),
            'end_index': int(),
            'level': int(),
            'variables': dict(),
            'functions': dict(),
            'comments': dict(),
            'classes': dict(),
            'content': list(),
            'args': list(),
            'kwargs': list(),
            'whitespace': int(),
        }
        if isinstance(values, dict):
            details.update(values)
        return details

    def build_last_class_details(self, values=None):
        log.debug('')
        details = {
            'name': str(),
            'body': str(),
            'start_line': int(),
            'stop_line': int(),
            'class_index': int(),
            'end_index': int(),
            'level': int(),
            'variables': dict(),
            'functions': dict(),
            'classes': dict(),
            'comments': dict(),
            'content': list(),
            'args': list(),
            'kwargs': list(),
            'whitespace': int(),
        }
        if isinstance(values, dict):
            details.update(values)
        return details

    # SEARCHERS

    def search_variable_declaration(self, words):
        log.debug('')
        variable_found, variable_index = False, None
        variable_name, seen_words = '', []
        for index in range(0,len(words)):
            word = words[index]
            if variable_found:
                seen_words.append(word)
                break
            if '=' in word and len(seen_words) in (0, 1):
                variable_found = True
                variable_index = index-1 if len(word) == 1 else index
                for character in words[variable_index]:
                    if character == '=':
                        break
                    variable_name += character
            seen_words.append(word)
        return {
            'variable_found': variable_found,
            'variable_index': variable_index,
            'variable_name': variable_name,
            'seen_words': seen_words,
        }

#   @pysnooper.snoop()
    def search_function_declaration(self, words):
        log.debug('')
        function_found, function_index = False, None
        function_name, seen_words = '', []
        for index in range(0,len(words)):
            word = words[index]
            if function_found:
                seen_words.append(word)
                break
            if word == 'def' and not seen_words:
                function_found, function_index = True, index
                for character in words[function_index+1]:
                    if character == '(':
                        break
                    function_name += character
            if not word:
                continue
            seen_words.append(word)
        return {
            'function_found': function_found,
            'function_index': function_index,
            'function_name': function_name,
            'seen_words': seen_words,
        }

    def search_class_declaration(self, words):
        log.debug('')
        class_found, class_index = False, None
        class_name, seen_words = '', []
        for index in range(0,len(words)):
            word = words[index]
            if class_found:
                seen_words.append(word)
                break
            if word == 'class' and not seen_words:
                class_found, class_index = True, index
                for character in words[class_index+1]:
                    if character == '(':
                        break
                    class_name += character
            seen_words.append(word)
        return {
            'class_found': class_found,
            'class_index': class_index,
            'class_name': class_name,
            'seen_words': seen_words,
        }

    def search_variable_end_index(self, words, variable_index=0):
        log.debug('')
        return len(words) - 1

#   @pysnooper.snoop()
    def search_function_end_index(self, words, function_index=0):
        log.debug('')
        declaration_end, end_index = '):', None
        for word_index in range(0, len(words)):
            if word_index < function_index:
                continue
            for char_index in range(0, len(words[word_index])):
                character = words[word_index][char_index]
                if char_index == len(words[word_index])-1:
                    break
                if character + words[word_index][char_index+1] == declaration_end:
                    end_index = word_index
                    break
            if not end_index:
                continue
            break
        return end_index

#   @pysnooper.snoop()
    def search_class_end_index(self, words, class_index=0):
        log.debug('')
        declaration_end, end_index = '):', None
        for word_index in range(0, len(words)):
            if word_index < class_index:
                continue
            for char_index in range(0, len(words[word_index])):
                character = words[word_index][char_index]
                if char_index == len(words[word_index])-1:
                    break
                if character + words[word_index][char_index+1] == declaration_end:
                    end_index = word_index
                    break
            if not end_index:
                continue
            break
        return end_index

#   @pysnooper.snoop()
    def search_code_arguments(self, words, start_index, end_index):
        log.debug('')
        seen_words, args, kwargs = [], [], []
        if not end_index:
            end_index = len(words) - 1
        for index in range(start_index+1, end_index+1):
            word = words[index]
            if not word:
                continue
            arg_builder, is_arg, is_kwarg = '', False, False
            if '=' in word:
                arg_builder = word.split('=')[0]
                is_kwarg = True
            if '(' in word:
                if not arg_builder:
                    arg_builder = word.split('(')[1]
                else:
                    arg_builder = arg_builder.split('(')[1]
            if ',' in word:
                if not arg_builder:
                    arg_builder = word.strip(',')
                else:
                    arg_builder = arg_builder.strip(',')
            if ')' in word:
                if not arg_builder:
                    arg_builder = word.split(')')[0]
                else:
                    arg_builder = arg_builder.split(')')[0]
            if not is_kwarg:
                is_arg = True
            if is_arg:
                args.append(arg_builder)
                seen_words.append(arg_builder)
                continue
            kwargs.append(arg_builder)
            seen_words.append(arg_builder)
        return {
            'seen_words': seen_words,
            'args': args,
            'kwargs': kwargs,
        }

    # SCANNERS

#   @pysnooper.snoop()
    def scan_function_body(self, file_line, start_line_number,
                           following_lines, details):
        log.debug('')
        function_body, stop_line = details['body'], start_line_number
        content = details['content']
        for index in range(len(following_lines)):
            if index == 0:
                stop_line += 1
                continue
            line = following_lines[index]
            level = self.fetch_line_identation_level(line)
            if not level or level <= details.get('level', 0):
                break
            content.append(line)
            function_body += line + '\n'
            stop_line += 1
            details = self.handle_nested_code_block_scan(
                following_lines[index], stop_line, following_lines[index:],
                details, parent='function',
                levels=[item for item in range(0, 13)]
            )
        if details.get('name') == '__init__':
            details['parent_variables'] = details.get('variables', {})
        details.update({
            'body': function_body,
            'stop_line': stop_line - 1,
            'content': content,
        })
        return details

    def scan_class_body(self, file_line, start_line_number,
                        following_lines, details):
        log.debug('')
        class_body, stop_line = details['body'], start_line_number
        content = details['content']
        for index in range(len(following_lines)):
            if index == 0:
                stop_line += 1
                continue
            line = following_lines[index]
            level = self.fetch_line_identation_level(line)
            if not level or level <= details.get('level', 0):
                if len(line) > 0:
                    break
            content.append(line)
            class_body += line + '\n'
            stop_line += 1
            details = self.handle_nested_code_block_scan(
                following_lines[index], stop_line, following_lines[index:],
                details, parent='class', levels=[item for item in range(0, 5)]
            )
        details.update({
            'body': class_body,
            'stop_line': stop_line - 1,
            'content': content,
        })
        return details

    def scan_file_lines(self, file_path, empty_lines=True):
        log.debug('')
        with open(file_path, 'r') as f:
            result = [
                sanitized_line for sanitized_line in (
                    line.rstrip("\n") for line in f
                )
            ]
            if not empty_lines:
                result = [item for item in result if item]
        return result

    # GENERAL

#   @pysnooper.snoop()
    def start_scanner(self, file_path):
        log.debug('')
        file_lines = self.scan_file_lines(file_path, empty_lines=True)
        line_number, offset, failures, successes = 0, 0, {}, {}
        self.set_last_scan_timestamp(datetime.datetime.now())
        for line in file_lines:
            line_number += 1
            if offset:
                successes.update({line_number: line})
                self.stdout_msg('Processed - ' + str(line_number) + ': ' + line)
                offset -= 1
                continue
            check = self.check_file_line_contains(line)
            handlers = {
                'comment': self.handle_process_comment,
                'variable': self.handle_process_variable,
                'function': self.handle_process_function,
                'class': self.handle_process_class,
            }
            if check not in handlers:
                self.stdout_msg('Unknown - ' + str(line_number) + ': ' + line)
                failures.update({line_number: line})
                continue
            handle = handlers[check](
                line, line_number, file_lines[line_number-1:], parent=None,
                levels=[0]
            )
            if isinstance(handle, dict) and handle.get('failed'):
                self.stdout_msg('Failed - ' + str(line_number) + ': ' + line)
                failures.update({line_number: line})
                continue
            self.update_content(handle)
            self.stdout_msg('Processed - ' + str(line_number) + ': ' + line)
            successes.update({line_number: line})
            if handle.get('stop_line', line_number) > line_number:
                offset = handle['stop_line'] - line_number - 1
        self.handle_dazzle_report(file_path, self.content, file_lines)
        self.stdout_msg(
            '\n[ DONE ]: Processed ({}/{}) lines from file ({}). '
            '({}) lines skipped.'.format(
                len(successes), line_number, file_path, len(failures)
            )
        )
        response = {
            'failed': False,
            'file_path': file_path,
            'file_lines': file_lines,
            'processed': len(successes),
            'failures': len(failures),
        }
        return response

    def stdout_msg(self, message, **kwargs):
        log.debug('')
        if self.silent:
            return False
        if kwargs.get('error'):
            log.error(message)
        elif kwargs.get('warning'):
            log.warning(message)
        else:
            log.info(message)
        print(message)
        return True

    # FILTERS

    def filter_variable_value_from_file_line(self, file_line):
        log.debug('')
        try:
            variable_value = ''.join(file_line.strip().split(' ')[2:])
        except Exception as e:
            return self.warning_could_not_filter_variable_name(file_line, e)
        return variable_value

    def filter_variable_name_from_file_line(self, file_line):
        log.debug('')
        try:
            variable_name = file_line.strip().split(' ')[0]
            if 'self.' in variable_name:
                variable_name = variable_name.split('.')[1]
        except Exception as e:
            return self.warning_could_not_filter_variable_name(file_line, e)
        return variable_name

    def filter_function_name_from_file_line(self, file_line):
        log.debug('')
        try:
            return file_line.strip().split(' ')[1].split('(')[0]
        except Exception as e:
            return self.warning_could_not_filter_function_name(file_line, e)

    def filter_class_name_from_file_line(self, file_line):
        log.debug('')
        try:
            return file_line.strip().split(' ')[1].split('(')[0]
        except Exception as e:
            return self.warning_could_not_filter_class_name(file_line, e)

    # HANDLERS

    def handle_dazzle_report(self, file_path, parsed_content, file_lines):
        log.debug('')
        if not self.check_dazzle_report_flag():
            return False
        report_file = self.fetch_dazzle_report_file_path()
        if not self.check_file_exists(report_file):
            self.stdout_msg('')
            return self.warning_dazzle_report_file_does_not_exist(report_file)
        timestamp = datetime.datetime.now().strftime('%Y-%M-%d %H:%M:%S')
        content = '\n--- (PARSER) --------------------------------------------'\
            '-----------------------\n'\
            '\n{} - [ PARSER ]: File path ({})\n'\
            '{} - [ PARSER ]: Parsed content:\n{}\n'\
            '{} - [ PARSER ]: File content ({}):\n{}\n'.format(
                timestamp, file_path, timestamp, json.dumps(
                    parsed_content, sort_keys=True, indent=4,
                    separators=(',', ': ')
                ), timestamp, file_path, '\n'.join(file_lines)
            )
        with open(report_file, 'a') as f:
            f.write(content + '\n')
        self.stdout_msg(
            '\n[ INFO ]: Generated dazzle report ({}).'.format(report_file)
        )
        return report_file

#   @pysnooper.snoop()
    def handle_nested_code_block_scan(self, file_line, start_line_number,
                                      following_lines, details, parent=None,
                                      levels=[]):
        log.debug('')
        level = self.fetch_line_identation_level(file_line)
        if len(levels) > 0 and level not in levels:
            return details
        check = self.check_file_line_contains(file_line)
        if not check:
            return details
        handlers = {
            'comment': self.handle_process_comment,
            'variable': self.handle_process_variable,
            'function': self.handle_process_function,
            'class': self.handle_process_class,
        }
        if check not in handlers:
            return details
        if check == 'comment' and parent == 'class':
            start_line_number = start_line_number - 1
        nested = handlers[check](
            file_line, start_line_number, following_lines, parent=parent,
            levels=levels
        )
        if nested.get('type'):
            del nested['type']
        if check == 'comment':
            details['comments'].update({
                nested.get('line'): nested
            })
        elif check == 'variable':
            details['variables'].update({
                nested.get('name'): nested
            })
        elif check == 'function':
            details['functions'].update({
                nested.get('name'): nested
            })
        elif check == 'class':
            details['classes'].update({
                nested.get('name'): nested
            })
        return details

#   @pysnooper.snoop()
    def handle_process_function(self, file_line, start_line_number,
                                    following_lines, parent=None, levels=[]):
        log.debug('')
        level = self.fetch_line_identation_level(file_line)
        if len(levels) > 0 and level not in levels:
            return {}
        check_code = self.check_function_declaration(file_line.split(' '))
        details = self.build_last_function_details({
            'name': self.filter_function_name_from_file_line(file_line),
            'start_line': start_line_number-1 if parent == 'class'
                else start_line_number,
            'stop_line': start_line_number-1 if parent == 'class'
                else start_line_number,
            'level': level,
            'body': file_line + '\n',
            'content': [file_line],
            'args': check_code.get('args', []),
            'kwargs': check_code.get('kwargs', []),
            'whitespace': len([item for item in file_line if item == ' ']),
            'function_index': check_code.get('function_index', 0),
            'end_index': check_code.get('end_index', 0),
            'parent': parent,
        })
        self.scan_function_body(
            file_line, start_line_number-1, following_lines, details
        )
        self.set_last_function_details(details)
        details.update({'type': 'function'})
        return details

    def handle_process_class(self, file_line, start_line_number, following_lines,
                             parent=None, levels=[]):
        log.debug('')
        level = self.fetch_line_identation_level(file_line)
        if len(levels) > 0 and level not in levels:
            return {}
        check_code = self.check_class_declaration(file_line.split(' '))
        details = self.build_last_class_details({
            'name': self.filter_class_name_from_file_line(file_line),
            'start_line': start_line_number,
            'stop_line': start_line_number,
            'level': level,
            'body': file_line + '\n',
            'content': [file_line],
            'args': check_code.get('args', []),
            'kwargs': check_code.get('kwargs', []),
            'whitespace': len([item for item in file_line if item == ' ']),
            'class_index': check_code.get('class_index', 0),
            'end_index': check_code.get('end_index', 0),
            'parent': parent,
        })
        self.scan_class_body(
            file_line, start_line_number, following_lines, details
        )
        self.set_last_class_details(details)
        for func_name in details.get('functions', {}):
            if details['functions'][func_name].get('parent_variables', {}):
                for var_name in details['functions'][func_name]['parent_variables']:
                    details['variables'].update({
                        var_name: details['functions'][func_name]['parent_variables'][var_name]
                    })
                del details['functions'][func_name]['parent_variables']
        details.update({'type': 'class'})
        return details

    def handle_process_comment(self, file_line, line_number, following_lines,
                               parent=None, levels=[]):
        log.debug('')
        level = self.fetch_line_identation_level(file_line)
        if len(levels) > 0 and level not in levels:
            return {}
        details = self.build_last_comment_details({
            'line': line_number,
            'body': file_line + '\n',
            'content': [file_line],
            'level': level,
            'whitespace': len([item for item in file_line if item == ' ']),
            'parent': parent,
        })
        self.set_last_comment_details(details)
        details.update({'type': 'comment'})
        return details

#   @pysnooper.snoop()
    def handle_process_variable(self, file_line, line_number, following_lines,
                                parent=None, levels=[]):
        log.debug('')
        level = self.fetch_line_identation_level(file_line)
        if len(levels) > 0 and level not in levels:
            return {}
        details = self.build_last_variable_details({
            'line': line_number-1 if parent in ['function', 'class']
                else line_number,
            'body': file_line + '\n',
            'name': self.filter_variable_name_from_file_line(file_line),
            'value': self.filter_variable_value_from_file_line(file_line),
            'level': level,
            'content': [file_line],
            'whitespace': len([item for item in file_line if item == ' ']),
            'parent': parent,
        })
        self.set_last_variable_details(details)
        details.update({'type': 'variable'})
        return details

    # ACTIONS

    def scan(self, file_path=None):
        log.debug('')
        if not file_path and not self.file_path:
            return self.error_no_python_file_found_to_scan(
                file_path, self.file_path
            )
        if not file_path:
            file_path = self.file_path
        return self.start_scanner(file_path)

    # CLEANERS

    def cleanup(self):
        log.debug('')
        self.clean_content()
        self.clean_last_comment()
        self.clean_last_variable()
        self.clean_last_function()
        self.clean_last_class()
        return True

    def clean_content(self):
        log.debug('')
        details = self.build_content_details()
        return self.set_content_details(details)

    def clean_last_comment(self):
        log.debug('')
        details = self.build_last_comment_details()
        return self.set_last_comment_details(details)

    def clean_last_variable(self):
        log.debug('')
        details = self.build_last_variable_details()
        return self.set_last_variable_details(details)

    def clean_last_function(self):
        log.debug('')
        details = self.build_last_function_details()
        return self.set_last_function_details(details)

    def clean_last_class(self):
        log.debug('')
        details = self.build_last_class_details()
        return self.set_last_class_details(details)

    # DISPLAY

    def display_formatted_content(self):
        log.debug('')
        return self.stdout_msg(
            json.dumps(
                self.content, sort_keys=True,
                indent=4, separators=(',', ': ')
            )
        )

    # WARNINGS

    def warning_dazzle_report_file_does_not_exist(self,  *args):
        self.warning_msg(
            'Dazzle report file does not exist.', args
        )
        return False

    def warning_could_not_filter_class_name(self,  *args):
        self.warning_msg(
            'Something went wrong. '
            'Could not filter out class name from file line.', args
        )
        return False

    def warning_could_not_filter_function_name(self,  *args):
        self.warning_msg(
            'Something went wrong. '
            'Could not filter out function name from file line.', args
        )
        return False

    def warning_could_not_filter_variable_name(self,  *args):
        self.warning_msg(
            'Something went wrong. '
            'Could not filter out variable name from file line.', args
        )
        return False

    def warning_file_does_not_exist(self,  *args):
        self.warning_msg('File does not exist.', args)
        return False

    def warning_msg(self, msg, details):
        log.warning(msg + ' Details: {}'.format(details))
        if not self.silent_warnings:
            return self.stdout_msg(
                '[ WARNING ]: {} Details: ({})'.format(msg, details)
            )
        return False

    # ERRORS

    def error_invalid_dazzle_report_file_path(self,  *args):
        self.error_msg('Invalid dazzle report file path.', args)
        return False

    def error_invalid_content_type(self,  *args):
        self.error_msg('Invalid content type.', args)
        return False

    def error_unknown_content_type(self,  *args):
        self.error_msg('Unknown content type.', args)
        return False

    def error_invalid_content_map(self,  *args):
        self.error_msg('Invalid Python file content map.', args)
        return False

    def error_invalid_variable_map(self,  *args):
        self.error_msg('Invalid Python variable declaration map.', args)
        return False

    def error_invalid_comment_map(self,  *args):
        self.error_msg('Invalid Python comment map.', args)
        return False

    def error_invalid_function_map(self,  *args):
        self.error_msg('Invalid Python function declaration map.', args)
        return False

    def error_invalid_class_map(self,  *args):
        self.error_msg('Invalid Python class declaration map.', args)
        return False

    def error_could_not_check_if_line_commented(self,  *args):
        self.error_msg('Could not check if file line is commented.', args)
        return False

    def error_could_not_check_if_line_has_declared_variable(self,  *args):
        self.error_msg(
            'Could not check if file line contains a variable declaration.', args
        )
        return False

    def error_could_not_check_if_line_has_declared_function(self,  *args):
        self.error_msg(
            'Could not check if file line contains a function declaration.', args
        )
        return False

    def error_cold_not_check_if_line_has_declared_class(self,  *args):
        self.error_msg('Could not check if file line contains a class declaration.', args)
        return False

    def error_could_not_fetch_file_line_count(self,  *args):
        self.error_msg('Could not fetch file line count.', args)
        return False

    def error_no_python_file_found_to_scan(self, *args):
        self.error_msg('No Python file found to scan!', args)
        return False

    def error_msg(self, msg, details):
        log.error(msg + ' Details: {}'.format(details))
        if not self.silent_errors:
            return self.stdout_msg(
                '[ ERROR ]: {} Details: ({})'.format(msg, details)
            )
        return False
