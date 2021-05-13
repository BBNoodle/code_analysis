# -*- coding: utf-8 -*- 
# @Time : 2/24/21 9:56 AM 
# @Author : mxt
# @File : re_statement.py

import re

from code_analysis.configure import *


class RegularRule:
    _DEFAULT_LIST = [
        'c', 'h', 'hpp', 'hxx', 'cpp', 'cc', 'cxx', 'C', 'c++', 'java', 'js', 'vue', 'ts', 'ftl', 'properties', 'jsp'
    ]

    def get(self, item='c'):
        """
        直接获取相应语言的正则表达式
        :param item:
        :return:
        """
        is_sh = False
        is_front_end = False
        if item == 'py':
            file_suffix = PY_RULE
        elif item in self._DEFAULT_LIST:
            file_suffix = DEFAULT_RULE
        elif item in ['xml', 'html']:
            is_front_end = True
            file_suffix = ML_RULE
        elif item in ['css', 'scss', 'sass', 'php']:
            is_front_end = True
            file_suffix = CSS_PHP_RULE
        elif item == 'jsp':
            is_front_end = True
            file_suffix = JSP_RULE
        elif item == 'ftl':
            is_front_end = True
            file_suffix = FTL_RULE
        elif item == 'sql':
            file_suffix = SQL_RULE
        elif item in ['sh', 'properties']:
            is_sh = True
            file_suffix = SH_RULE
        else:
            print(f"该文件类型::{item}::未添加至模板文件中。")
            return True, False, False, False

        return self._str2re(file_suffix, is_sh, is_front_end)

    @staticmethod
    def _str2re(_rule: dict, is_sh: bool, is_front_end: bool):
        if is_front_end:
            line = _rule.get('line_comment').split(' ')
            line_re_str = '{0[0]}[\s\S]*?{0[1]}'.format(line)
            line_regular = re.compile(r'%s' % line_re_str, re.S)
        else:
            line = _rule.get('line_comment').split(' ')[:1]
            line_re_str = '%s(.*)' % line[0]
            line_regular = re.compile(r'%s' % line_re_str, re.S)

        if is_sh:
            return line_regular, line, line_regular, line

        block = _rule.get('block_comment').split(' ')
        block_re_str = '{0[0]}[\s\S]*?{0[1]}'.format(block)
        block_regular = re.compile(r'%s' % block_re_str, re.S)

        return block_regular, block, line_regular, line
