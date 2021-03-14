#!/usr/bin/python3
#
# Regards, the Alveare Solutions society.
#
import pysnooper
import datetime
import os
import re
import json
import logging
import random

log = logging.getLogger(__name__)


class WFPythonScrambler():
    silent = True
    silent_warnings = False
    silent_errors = False

    def __init__(self, *args, **kwargs):
        global log
        self.content = kwargs.get('parsed_content', dict())
        self.file_path = kwargs.get('file_path', str())
        self.file_lines = {} if not self.file_path \
            else self.build_file_lines_map(self.file_path)
        self.random_seq = kwargs.get('random_seq', list())
        self.scrambled_content = dict()
        self.silent = kwargs.get('silent', True)
        self.silent_warnings = kwargs.get('silent_warnings', False)
        self.silent_errors = kwargs.get('silent_errors', False)
        self.file_lines = kwargs.get('file_lines', {})
        self.safety = kwargs.get('safety', True)
        self.dazzle_report = kwargs.get('dazzle_report', True)
        self.report_file_path = kwargs.get('report_file_path', '')
        if kwargs.get('log_name'):
            log = logging.getLogger(kwargs['log_name'])
        log.debug('')

    # DUNDERS

    def __str__(self, *args, **kwargs):
        log.debug('')
        response = self.fetch_values()
        response.update({'object': 'WFPythonScrambler'})
        return str(response)

    # FETCHERS

    def fetch_dazzle_report_file_path(self):
        log.debug('')
        return self.report_file_path

    def fetch_scrambled_content(self):
        log.debug('')
        return self.scrambled_content

    def fetch_function_appearance_patterns(self, function_name):
        log.debug('')
        if not isinstance(function_name, str):
            self.error_invalid_function_name(function_name)
            return []
        patterns = [
            'self\.{}\('.format(function_name),
            '{}\('.format(function_name),
            '\.{}\('.format(function_name),
            '{},'.format(function_name),
            'self\.{},'.format(function_name),
            '\.{},'.format(function_name),
        ]
        return patterns

    def fetch_class_appearance_patterns(self, class_name):
        log.debug('')
        if not isinstance(class_name, str):
            self.error_invalid_class_name(class_name)
            return []
        patterns = [
            'self\.{}\('.format(class_name),
            '{}\('.format(class_name),
            '\.{}\('.format(class_name),
            '{},'.format(class_name),
            'self\.{},'.format(class_name),
            '\.{},'.format(class_name),
        ]
        return patterns

    def fetch_argument_appearance_patterns(self, argument_name):
        log.debug('')
        if not isinstance(argument_name, str):
            self.error_invalid_argument_name(argument_name)
            return []
        patterns = {
            ' {} ='.format(argument_name),
            '{}='.format(argument_name),
            ' = {}'.format(argument_name),
            '={}'.format(argument_name),
            '\.{} '.format(argument_name),
            '\[{}'.format(argument_name),
            '{}\]'.format(argument_name),
            '\({}'.format(argument_name),
            '\({},'.format(argument_name),
            '{}\)'.format(argument_name),
            '{},'.format(argument_name),
            ' {} '.format(argument_name),
            '{}:'.format(argument_name),
            ' {}\.'.format(argument_name),
            '{}\.'.format(argument_name),
            'if {}'.format(argument_name),
            'for {}'.format(argument_name),
            'while {}'.format(argument_name),
            'in {}'.format(argument_name),
            'not {}'.format(argument_name),
        }
        return patterns

    def fetch_variable_appearance_patterns(self, variable_name):
        log.debug('')
        if not isinstance(variable_name, str):
            self.error_invalid_variable_name(variable_name)
            return []
        patterns = {
            'self\.{} '.format(variable_name),
            'self\.{} ='.format(variable_name),
            'self\.{}='.format(variable_name),
            ' self\.{} ='.format(variable_name),
            'self\.{}\]'.format(variable_name),
            ' {} ='.format(variable_name),
            '{} ='.format(variable_name),
            '{}='.format(variable_name),
            ' = {}'.format(variable_name),
            '={}'.format(variable_name),
            '\.{} '.format(variable_name),
            '{}\. '.format(variable_name),
            '\[{}'.format(variable_name),
            '{}\]'.format(variable_name),
            '{}, '.format(variable_name),
            '{},'.format(variable_name),
            '{}\)'.format(variable_name),
            '\({}'.format(variable_name),
            ' {} '.format(variable_name),
            '{}:'.format(variable_name),
            ' {}\.'.format(variable_name),
            '{}\.'.format(variable_name),
            ' {}'.format(variable_name),
            'if {}'.format(variable_name),
            'for {}'.format(variable_name),
            'while {}'.format(variable_name),
            'in {}'.format(variable_name),
            'not {}'.format(variable_name),
        }
        return patterns

    def fetch_user_input(self, msg):
        log.debug('')
        stdin = input(msg)
        return stdin

    def fetch_file_lines_map(self):
        log.debug('')
        return self.file_lines

    def fetch_file_path(self):
        log.debug('')
        return self.file_path

    def fetch_lower_case_character_set(self):
        log.debug('')
        return 'abcdefghijklmnpqrstuvwxyz'

    def fetch_upper_case_character_set(self):
        log.debug('')
        return 'ABCDEFGHIJKLMNPQRSTUVWXYZ'

    def fetch_numeric_character_set(self):
        log.debug('')
        return '0123456789'

    def fetch_symbol_character_set(self):
        log.debug('')
        return '_'

    def fetch_random_string_character_set(self):
        log.debug('')
        return self.fetch_lower_case_character_set() \
            + self.fetch_upper_case_character_set() \
            + self.fetch_numeric_character_set() \
            + self.fetch_symbol_character_set()

    def fetch_values(self):
        log.debug('')
        return self.__dict__

    def fetch_random_seq(self):
        log.debug('')
        return self.random_seq

    # SETTERS

    def set_dazzle_file_path(self, file_path):
        log.debug('')
        if not isinstance(file_path, str) or \
                not self.check_file_exists(file_path):
            return self.error_invalid_dazzle_file_path(file_path)
        self.report_file_path = file_path
        return True

    def set_random_seq(self, random_seq):
        log.debug('')
        if not isinstance(random_seq, list):
            return self.error_invalid_random_seq(random_seq)
        self.random_seq = random_seq
        return True

    def set_scrambled_content(self, scrambled_content):
        log.debug('')
        if not isinstance(scrambled_content, dict):
            return self.error_invalid_scrambled_content_map(file_lines)
        self.scrambled_content = scrambled_content
        return True

    def set_file_lines_map(self, file_lines):
        log.debug('')
        if not isinstance(file_lines, dict):
            return self.error_invalid_file_lines_map(file_lines)
        self.file_lines = file_lines
        return True

#   @pysnooper.snoop()
    def set_parsed_content(self, content):
        log.debug('')
        if not isinstance(content, dict):
            return self.error_invalid_parsed_content_type(content)
        self.content = content
        return True

    def set_file_path(self, file_path):
        log.debug('')
        if file_path != '' and not self.check_file_exists(file_path):
            return self.warning_file_does_not_exist(file_path)
        self.file_path = file_path
        return True

    # CHECKERS

    def check_dazzle_report_flag(self):
        log.debug('')
        return self.dazzle_report

    def check_file_exists(self, file_path):
        log.debug('')
        return os.path.isfile(file_path)

    # UPDATERS

    def update_scrambled_content(self, scrambled_content):
        log.debug('')
        if not isinstance(scrambled_content, dict):
            return self.error_invalid_scrambled_content_type(scrambled_content)
        self.scrambled_content.update(scrambled_content)
        return True

    def update_random_seq(self, random_seq):
        log.debug('')
        if random_seq in self.random_seq:
            return self.warning_random_sequence_already_indexed(
                random_seq, self.random_seq
            )
        self.random_seq.append(random_seq)
        return True

    # CREATORS

#   @pysnooper.snoop()
    def create_function_argument_replacement_body(self, argument, new_name,
                                                  body, line, file_lines):
        log.debug('')
        try:
            new_body = re.sub(argument, new_name, file_lines[line], 1)
        except Exception as e:
            return body
        return new_body

#   @pysnooper.snoop()
    def create_variable_replacement_body(self, variable_name, new_name, body, line, file_lines):
        log.debug('')
        try:
            segmented = body.split('=')
            segmented[0] = re.sub(variable_name, new_name, segmented[0], 1)
            new_body = '='.join(segmented)
        except Exception as e:
            return body
        return new_body

    def create_function_replacement_body(self, function_name, new_name, body):
        log.debug('')
        first_line = body.split('\n')[0]
        try:
            first_line_replace = re.sub(function_name, new_name, first_line, 1)
            new_body = first_line_replace + '\n' + '\n'.join(body.split('\n')[1:])
        except Exception as e:
            return body
        return new_body

    def create_class_replacement_body(self, class_name, new_name, body):
        log.debug('')
        first_line = body.split('\n')[0]
        try:
            first_line_replace = re.sub(class_name, new_name, first_line, 1)
            new_body = first_line_replace + '\n' + '\n'.join(body.split('\n')[1:])
        except Exception as e:
            return body
        return new_body

    # BUILDERS

    def rebuild_file_lines_map(self):
        return self.set_file_lines_map(
            self.build_file_lines_map(self.fetch_file_path())
        )

    def build_file_lines_map(self, file_path):
        log.debug('')
        if not self.check_file_exists(file_path):
            self.error_file_does_not_exist(file_path)
        line, file_lines = 1, {}
        with open(file_path, 'r') as f:
            for content in f.readlines():
                file_lines.update({line: content})
                line += 1
        return file_lines

    # SCRAMBLERS

    def start_scramblers(self, file_path=None, parsed_content=None):
        log.debug('')
        if not file_path and not self.file_path:
            return self.error_no_file_path_found(
                file_path, self.file_path, parsed_content
            )
        elif not file_path:
            file_path = self.file_path
        if not parsed_content and not self.content:
            return self.error_no_parsed_content_found(
                parsed_content, self.content, file_path
            )
        elif not parsed_content:
            parsed_content = self.content
        scrambled_content = {
            'comments': self.start_comment_cleaner(
                file_path, parsed_content.get('comments', {})
            ),
            'variables': self.start_variable_scrambler(
                file_path, 0, len(parsed_content),
                parsed_content.get('variables', {})
            ),
            'functions': self.start_function_scrambler(
                file_path, parsed_content.get('functions', {})
            ),
            'classes': self.start_class_scrambler(
                file_path, parsed_content.get('classes', {})
            ),

        }
        scrambled_content['scrambled_content'] = self.fetch_file_lines_map()
        self.update_scrambled_content(scrambled_content)
        return scrambled_content

#   @pysnooper.snoop()
    def start_class_scrambler(self, file_path, classes, file_lines=None):
        log.debug('')
        scrambled_classes = classes.copy()
        file_lines = file_lines or self.fetch_file_lines_map()
        if not file_lines:
            self.rebuild_file_lines_map()
            file_lines = self.fetch_file_lines_map()
        if not classes:
            return scrambled_classes
        for class_name in classes:
            start_line = classes[class_name].get('start_line')
            stop_line = classes[class_name].get('stop_line')
            body = classes[class_name].get('body')
            self.stage_scrambled_file_class(
                start_line, stop_line, class_name, body, file_lines,
                scrambled_classes
            )
            args = {} if not classes[class_name].get('args') \
                else {arg: {} for arg in classes[class_name]['args']}
            kwargs = {} if not classes[class_name].get('kwargs') \
                else {arg: {} for arg in classes[class_name]['kwargs']}
            nested = {
                'functions': self.start_function_scrambler(
                    file_path, classes[class_name].get('functions', {}),
                    file_lines,
                ),
                'comments': self.start_comment_cleaner(
                    file_path, classes[class_name].get('comments', {}),
                    file_lines,
                ),
                'variables': self.start_variable_scrambler(
                    file_path, start_line, stop_line,
                    classes[class_name].get('variables', {}), file_lines,
                ),
                'classes': self.start_class_scrambler(
                    file_path, classes[class_name].get('classes', {}),
                    file_lines,
                ),
                'args': self.start_class_argument_scrambler(
                    file_path, start_line, stop_line, args, file_lines,
                ),
                'kwargs': self.start_class_argument_scrambler(
                    file_path, start_line, stop_line, kwargs, file_lines,
                ),
            }
            scrambled_classes[class_name].update(nested)
        return scrambled_classes

#   @pysnooper.snoop()
    def start_function_scrambler(self, file_path, functions, file_lines=None):
        log.debug('')
        scrambled_functions = functions.copy()
        file_lines = file_lines or self.fetch_file_lines_map()
        if not file_lines:
            self.rebuild_file_lines_map()
            file_lines = self.fetch_file_lines_map()
        if not functions:
            return scrambled_functions
        for function_name in functions:
            start_line = functions[function_name].get('start_line')
            stop_line = functions[function_name].get('stop_line')
            body = functions[function_name].get('body')
            args = {} if not functions[function_name].get('args') \
                else {arg: {} for arg in functions[function_name]['args']}
            kwargs = {} if not functions[function_name].get('kwargs') \
                else {arg: {} for arg in functions[function_name]['kwargs']}
            if '__' in function_name:
                self.stdout_msg(
                    'Skipping dunder method - {} - ({}-{}): {}'.format(
                        self.file_path, start_line, stop_line, body
                    )
                )
                functions[function_name]['skipped'] = True
            else:
                self.stage_scrambled_file_function(
                    start_line, stop_line, function_name, body, file_lines,
                    scrambled_functions
                )
            nested = {
                'comments': self.start_comment_cleaner(
                    file_path, functions[function_name].get('comments', []),
                    file_lines,
                ),
                'variables': self.start_variable_scrambler(
                    file_path, start_line, stop_line,
                    functions[function_name].get('variables', {}), file_lines,
                ),
                'args': self.start_function_argument_scrambler(
                    file_path, start_line, stop_line, args, file_lines,
                ),
                'kwargs': self.start_function_argument_scrambler(
                    file_path, start_line, stop_line, kwargs, file_lines,
                ),
                'classes': self.start_class_scrambler(
                    file_path, functions[function_name].get('classes', {}),
                    file_lines,
                ),
                'functions': self.start_function_scrambler(
                    file_path, functions[function_name].get('functions', {}),
                    file_lines,
                ),
            }
            scrambled_functions[function_name].update(nested)
            functions[function_name]['skipped'] = False
        return scrambled_functions

    def start_class_argument_scrambler(self, file_path, start_line,
                                       stop_line, arguments, file_lines=None):
        log.debug('')
        scrambled_arguments = {
            arg: {'line': start_line} for arg in arguments
        }
        file_lines = file_lines or self.fetch_file_lines_map()
        if not file_lines:
            self.rebuild_file_lines_map()
            file_lines = self.fetch_file_lines_map()
        if not arguments:
            return scrambled_arguments
        for argument in arguments:
            if argument in ('object') or '*' in argument:
                continue
            body = file_lines[start_line]
            self.stage_scrambled_file_argument(
                start_line, stop_line, argument, body,
                file_lines, scrambled_arguments
            )
        return scrambled_arguments

    def start_function_argument_scrambler(self, file_path, start_line,
                                          stop_line, arguments, file_lines=None):
        log.debug('')
        scrambled_arguments = {
            arg: {'line': start_line} for arg in arguments
        }
        file_lines = file_lines or self.fetch_file_lines_map()
        if not file_lines:
            self.rebuild_file_lines_map()
            file_lines = self.fetch_file_lines_map()
        if not arguments:
            return scrambled_arguments
        for argument in arguments:
            if argument in ('self', 'cls') or '*' in argument:
                continue
            body = file_lines[start_line]
            self.stage_scrambled_file_argument(
                start_line, stop_line, argument, body,
                file_lines, scrambled_arguments
            )
        return scrambled_arguments

#   @pysnooper.snoop()
    def start_variable_scrambler(self, file_path, start_line, stop_line,
                                 variables, file_lines=None):
        log.debug('')
        scrambled_variables = variables.copy()
        file_lines = file_lines or self.fetch_file_lines_map()
        if not file_lines:
            self.rebuild_file_lines_map()
            file_lines = self.fetch_file_lines_map()
        if not variables:
            return scrambled_variables
        for variable_name in variables:
            line = variables[variable_name].get('line')
            if line < start_line or line > stop_line:
                continue
            body = variables[variable_name].get('body')
            self.stage_scrambled_file_variable(
                line, variable_name, body, file_lines, scrambled_variables
            )
        return scrambled_variables

#   @pysnooper.snoop()
    def start_comment_cleaner(self, file_path, comments, file_lines=None):
        log.debug('')
        scrambled_comments = comments.copy()
        file_lines = file_lines or self.fetch_file_lines_map()
        if not file_lines:
            self.rebuild_file_lines_map()
            file_lines = self.fetch_file_lines_map()
        if not comments:
            return scrambled_comments
        for comment_line in comments:
            body = comments[comment_line].get('body', str())
            self.stage_cleaned_file_comment(
                comment_line, body, file_lines, scrambled_comments
            )
        return scrambled_comments

    # STAGERS

#   @pysnooper.snoop()
    def stage_scrambled_file_variable(self, line, variable_name, body,
                                      file_lines, scrambled_variables):
        log.debug('')
        random_seq = self.generate_unique_sequence()
        replacement = self.create_variable_replacement_body(
            variable_name, 'var_' + random_seq, body, line, file_lines,
        )
        self.stdout_msg(
            'Staging variable - {} - {}: {}'.format(
#           'Replaced with    - {} - {}: {}\n'.format(
                self.file_path, line, body.split('\n')[0],
#               self.file_path, line, replacement.split('\n')[0]
            )
        )
        file_lines[line] = replacement
        scrambled_variables[variable_name].update({
            'scrambled': 'var_' + random_seq,
            'appearances': self.search_variable_appearance_line_numbers(
                variable_name, line, file_lines
            ),
        })
        for line_number in scrambled_variables[variable_name]['appearances']:
            self.replace_pattern_in_file_line(
                line_number, variable_name, 'var_' + random_seq, file_lines, occurance=1
            )
        return scrambled_variables

#   @pysnooper.snoop()
    def stage_scrambled_file_argument(self, start_line, stop_line, argument, body,
                                      file_lines, scrambled_arguments):
        log.debug('')
        random_seq = self.generate_unique_sequence()
        replacement = self.create_function_argument_replacement_body(
            argument, 'arg_' + random_seq, body, start_line, file_lines
        )
        self.stdout_msg(
            'Staging function argument - {} - {}: {}\n'
            'Replaced with             - {} - {}: {}\n'.format(
                self.file_path, start_line, body.split('\n')[0],
                self.file_path, start_line, replacement.split('\n')[0]
            )
        )
        file_lines[start_line] = replacement
        scrambled_arguments[argument].update({
            'scrambled': 'arg_' + random_seq,
            'appearances': self.search_argument_appearance_line_numbers(
                argument, start_line, stop_line, file_lines
            ),
        })
        for line_number in scrambled_arguments[argument]['appearances']:
            self.replace_pattern_in_file_line(
                line_number, argument, 'arg_' + random_seq, file_lines, occurance=1
            )
        return scrambled_arguments

    def stage_cleaned_file_comment(self, line, body, file_lines,
                                   scrambled_comments):
        log.debug('')
        if '#!/' in body:
            self.stdout_msg(
                'Skipping shebang - {} - {}: {}\n'.format(
                    self.file_path, line, body.strip('\n')
                )
            )
            return file_lines
        self.stdout_msg(
            'Staging comment - {} - {}: {}\n'
            'Replaced with   - {} - {}: {}\n'.format(
                self.file_path, line, body.strip('\n'),
                self.file_path, line, ''
            )
        )
        file_lines[line] = ''
        scrambled_comments[line].update({
            'scrambled': '',
        })
        return scrambled_comments

    def stage_scrambled_file_function(self, start_line, end_line, function_name,
                                      body, file_lines, scrambled_functions):
        log.debug('')
        random_seq = self.generate_unique_sequence()
        replacement = self.create_function_replacement_body(
            function_name, 'func_' + random_seq, body
        )
        self.stdout_msg(
            'Staging function - {} - ({}-{}): \n{}\n\n'
            'Replaced with - {} - ({}-{}): \n{}\n'.format(
                self.file_path, start_line, end_line, body.split('\n')[0],
                self.file_path, start_line, end_line, replacement.split('\n')[0]
            )
        )
        file_lines[start_line] = replacement.split('\n')[0]
        scrambled_functions[function_name].update({
            'scrambled': 'func_' + random_seq,
            'appearances': self.search_function_appearance_line_numbers(
                function_name, start_line, file_lines
            ),
        })
        for line_number in scrambled_functions[function_name]['appearances']:
            self.replace_pattern_in_file_line(
                line_number, function_name, 'func_' + random_seq, file_lines
            )
        return scrambled_functions

    def stage_scrambled_file_class(self, start_line, end_line, class_name, body,
                                   file_lines, scrambled_classes):
        log.debug('')
        random_seq = self.generate_unique_sequence()
        replacement = self.create_class_replacement_body(
            class_name, 'class_' + random_seq, body
        )
        self.stdout_msg(
            'Staging class - {} - ({}-{}): \n{}\n\n'
            'Replaced with - {} - ({}-{}): \n{}\n'.format(
                self.file_path, start_line, end_line, body.split('\n')[0],
                self.file_path, start_line, end_line, replacement.split('\n')[0]
            )
        )
        file_lines[start_line] = replacement.split('\n')[0]
        scrambled_classes[class_name].update({
            'scrambled': 'class_' + random_seq,
            'appearances': self.search_class_appearance_line_numbers(
                class_name, start_line, file_lines
            ),
        })
        for line_number in scrambled_classes[class_name]['appearances']:
            self.replace_pattern_in_file_line(
                line_number, class_name, 'class_' + random_seq, file_lines
            )
        return scrambled_classes

    # SEARCHERS

#   @pysnooper.snoop()
    def search_function_appearance_line_numbers(self, function_name,
                                                declaration_line, file_lines):
        log.debug('')
        appearance_patterns = self.fetch_function_appearance_patterns(
            function_name
        )
        anti_patterns = ['def', 'class', '{} ='.format(function_name)]
        appearances = self.search_appearance_line_numbers(
            appearance_patterns, anti_patterns,
            file_lines, ignore_lines=[declaration_line]
        )
        return appearances

    def search_class_appearance_line_numbers(self, class_name,
                                             declaration_line, file_lines):
        log.debug('')
        appearance_patterns = self.fetch_class_appearance_patterns(
            class_name
        )
        anti_patterns = ['def', 'class', '{} ='.format(class_name)]
        appearances = self.search_appearance_line_numbers(
            appearance_patterns, anti_patterns,
            file_lines, ignore_lines=[declaration_line]
        )
        return appearances

#   @pysnooper.snoop()
    def search_variable_appearance_line_numbers(self, variable_name,
                                                declaration_line, file_lines):
        log.debug('')
        appearance_patterns = self.fetch_variable_appearance_patterns(
            variable_name
        )
        anti_patterns = [
            'def', 'class', 'self\.{}\('.format(variable_name),
            '_{}_'.format(variable_name), "\['{}".format(variable_name),
            "\('{}".format(variable_name),
            '[a-zA-Z_ ]{1,}' + '{}[a-zA-Z_]'.format(variable_name)
        ]
        appearances = self.search_appearance_line_numbers(
            appearance_patterns, anti_patterns,
            file_lines, ignore_lines=[declaration_line]
        )
        return appearances

#   @pysnooper.snoop()
    def search_appearance_line_numbers(self, patterns, anti_patterns,
                                       file_lines, ignore_lines=[]):
        log.debug('')
        appearances = []
        offset = 0
        for line_number in file_lines:
            if offset:
                offset -= 1
                continue
            if line_number in ignore_lines:
                continue
            for pattern in patterns:
                to_ignore = False
                if not isinstance(pattern, str):
                    self.warning_invalid_search_pattern(
                        pattern, patterns, appearances, ignore_lines
                    )
                try:
                    check = re.search(pattern, file_lines[line_number])
                    if not check or line_number in appearances:
                        continue
                    for anti_pattern in anti_patterns:
                        check_ignore = re.search(anti_pattern, file_lines[line_number])
                        if check_ignore:
                            to_ignore = True
                            offset = 1
                            break
                except Exception as e:
                    self.warning_could_not_search_for_pattern_in_file_line(
                        pattern, line_number, file_lines[line_number], e
                    )
                    continue
                if not to_ignore:
                    appearances.append(line_number)
                break
        return appearances

#   @pysnooper.snoop()
    def search_argument_appearance_line_numbers(self, argument, start_line,
                                                stop_line, file_lines, ignore_lines=[]):
        log.debug('')
        appearance_patterns = self.fetch_argument_appearance_patterns(
            argument.strip('):').strip(' ').strip(')').strip(',')
        )
        anti_patterns = ['def', 'class',]
        line_count, truncated_lines = stop_line - start_line, dict()
        current_line = start_line
        for index in range(line_count):
            truncated_lines.update({current_line: file_lines[current_line]})
            current_line += 1
        appearances = self.search_appearance_line_numbers(
            appearance_patterns, anti_patterns,
            truncated_lines, ignore_lines=[start_line]
        )
        return appearances

    # HANDLERS

    def handle_dazzle_report(self, file_path, scrambled_content, file_lines):
        log.debug('')
        if not self.check_dazzle_report_flag():
            return False
        report_file = self.fetch_dazzle_report_file_path()
        if not self.check_file_exists(report_file):
            self.stdout_msg('')
            return self.warning_dazzle_report_file_does_not_exist(report_file)
        timestamp = datetime.datetime.now().strftime('%Y-%M-%d %H:%M:%S')
        content = '--- (SCRAMBLER) -------------------------------------------'\
            '---------------------\n'\
            '\n{} - [ SCRAMBLER ]: File path ({})\n'\
            '{} - [ SCRAMBLER ]: Scrambled content:\n{}\n'\
            '{} - [ SCRAMBLER ]: Staged file ({}):\n{}\n\n'.format(
                timestamp, file_path, timestamp, json.dumps(
                    scrambled_content, sort_keys=True, indent=4,
                    separators=(',', ': ')
                ), timestamp, file_path, ''.join(file_lines)
            )
        with open(report_file, 'a') as f:
            f.write(content + '\n')
        self.stdout_msg(
            '\n[ INFO ]: Generated dazzle report ({}).'.format(report_file)
        )
        return report_file

    # GENERAL

#   @pysnooper.snoop()
    def write_scrambled_content_to_file(self, file_path, scrambled_content, file_lines):
        log.debug('')
        if self.safety:
            self.warning_safety_on(file_path, scrambled_content, file_lines)
            return file_path
        with open(file_path, 'w') as f:
            f.write(''.join(file_lines))
        self.handle_dazzle_report(file_path, scrambled_content, file_lines)
        return file_path

    def replace_pattern_in_file_line(self, line, old_pattern, new_pattern,
                                     file_lines, occurance=1):
        log.debug('')
        old_line = file_lines[line]
        try:
            new_line = re.sub(old_pattern, new_pattern, old_line, occurance)
        except Exception as e:
            return file_lines
        self.stdout_msg(
            'Replacing ({}) with ({}) on line ({})\n'
            'Old Line - {}: {}'
            'New Line - {}: {}'.format(
                old_pattern, new_pattern, line, line, old_line, line, new_line
            )
        )
        file_lines[line] = new_line
        return file_lines

    def generate_unique_sequence(self):
        stop, existing_sequences = False, self.fetch_random_seq()
        random_seq = self.random_string_generator()
        numbers = self.fetch_numeric_character_set()
        if random_seq in existing_sequences or random_seq[0] in numbers \
                or random_seq[0] in numbers or random_seq[0] == '_':
            while not stop:
                random_seq = self.random_string_generator()
                if random_seq in existing_sequences \
                        or random_seq[0] in numbers \
                        or random_seq[0] == '_':
                    continue
                stop = True
        self.update_random_seq(random_seq)
        return random_seq

    def random_string_generator(self, size=random.randint(5, 100), chars=''):
        if not chars:
            chars = self.fetch_random_string_character_set()
        return ''.join(random.choice(chars) for c in range(size))

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

    # DISPLAY

    def display_formatted_dict(self, value_set):
        log.debug('')
        return self.stdout_msg(
            json.dumps(
                value_set, sort_keys=True,
                indent=4, separators=(',', ': ')
            )
        )

    def display_formatted_scrambled_content(self):
        log.debug('')
        return self.display_formatted_dict(self.scrambled_content)

    def display_staged_scrambled_content(self):
        log.debug('')
        for item in self.file_lines:
            self.stdout_msg('{}: {}'.format(item, self.file_lines[item].strip('\n')))

    # CLEANUP

    def cleanup_parsed_content(self):
        log.debug('')
        return self.set_parsed_content({})

    def cleanup_file_path(self):
        log.debug('')
        return self.set_file_path('')

    def cleanup_file_lines(self):
        log.debug('')
        return self.set_file_lines_map({})

    def cleanup_random_seq(self):
        log.debug('')
        return self.set_random_seq([])

    def cleanup_scrambled_content(self):
        log.debug('')
        return self.set_scrambled_content({})

    def cleanup(self):
        log.debug('')
        self.cleanup_file_path()
        self.cleanup_file_lines()
        self.cleanup_random_seq()
        self.cleanup_parsed_content()
        self.cleanup_scrambled_content()
        return True

    # WARNINGS

    def warning_dazzle_report_file_does_not_exist(self, *args):
        self.warning_msg(
            'Specified dazzle report file does not exist.', args
        )
        return False

    def warning_safety_on(self, *args):
        self.warning_msg(
            'Safety is ON. No files modified.', args
        )
        return False

    def warning_could_not_search_for_pattern_in_file_line(self, *args):
        self.warning_msg(
            'Something went wrong. '
            'Could not search for pattern in file line.', args
        )
        return False

    def warning_invalid_search_pattern(self, *args):
        self.warning_msg('Invalid pattern to search for.', args)
        return False

    def warning_random_sequence_already_indexed(self, *args):
        self.warning_msg('Random character sequence already indexed.', args)
        return False

    def warning_file_does_not_exist(self, *args):
        self.warning_msg('File does not exist.', args)
        return False

    def warning_msg(self, msg, details):
        log.warning(msg + ' Details: ({})'.format(details))
        if not self.silent_warnings:
            return self.stdout_msg(
                '[ WARNING ]: {} Details: ({})'.format(msg, details),
                warning=True
            )
        return False

    # ERRORS

    def error_invalid_dazzle_file_path(self, *args):
        self.error_msg('Invalid dazzle report file path.', args)
        return False

    def error_invalid_random_seq(self, *args):
        self.error_msg('Invalid random sequence array.', args)
        return False

    def error_invalid_class_name(self, *args):
        self.error_msg('Invalid class name.', args)
        return False

    def error_invalid_argument_name(self, *args):
        self.error_msg('Invalid function argument name.', args)
        return False

    def error_invalid_variable_name(self, *args):
        self.error_msg('Invalid variable name.', args)
        return False

    def error_invalid_function_name(self, *args):
        self.error_msg('Invalid function name.', args)
        return False

    def error_invalid_scrambled_content_map(self, *args):
        self.error_msg('Invalid scrambled content map.', args)
        return False

    def error_invalid_file_lines_map(self, *args):
        self.error_msg('Invalid file lines map.', args)
        return False

    def error_file_does_not_exist(self, *args):
        self.error_msg('File does not exist.', args)
        return False

    def error_no_file_path_found(self, *args):
        self.error_msg('No file path found.', args)
        return False

    def error_no_parsed_content_found(self, *args):
        self.error_msg('No parsed content found.', args)
        return False

    def error_invalid_scrambled_content_type(self, *args):
        self.error_msg('Invalid scrambled content type.', args)
        return False

    def error_invalid_parsed_content_type(self, *args):
        self.error_msg('Invalid parsed content type.', args)
        return False

    def error_msg(self, msg, details):
        log.error(msg + ' Details: {}'.format(details))
        if not self.silent_errors:
            return self.stdout_msg(
                '[ ERROR ]: {} Details: ({})'.format(msg, details),
                error=True
            )
        return False

