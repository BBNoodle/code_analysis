# -*- coding: utf-8 -*- 
# @Time : 2/24/21 9:56 AM 
# @Author : mxt
# @File : re_statement.py

import re

from code_analysis.configure import *


class RegularRule:
    _DEFAULT_LIST = ['c', 'h', 'hpp', 'hxx', 'cpp', 'cc', 'cxx', 'C', 'c++', 'java', 'js', 'vue', 'ts']

    def get(self, item='c'):
        """
        直接获取相应语言的正则表达式
        :param item:
        :return:
        """
        if item == 'py':
            file_suffix = PY_RULE
        elif item in self._DEFAULT_LIST:
            file_suffix = DEFAULT_RULE
        elif item in ['xml', 'html']:
            file_suffix = ML_RULE
        elif item in ['css', 'sass', 'php']:
            file_suffix = CSS_PHP_RULE
        elif item == 'sql':
            file_suffix = SQL_RULE
        elif item == 'sh':
            file_suffix = SH_RULE
        else:
            raise Exception('该文件类型未添加至模板文件中。')

        return self._str2re(file_suffix, True) if item == 'sh' else self._str2re(file_suffix)

    @staticmethod
    def _str2re(_rule: dict, is_sh=False):
        line = _rule.get('line_comment')
        line = '%s(\s|.)' % line
        line_re = re.compile(r'%s' % line)

        if is_sh:
            return line_re, line_re

        block = _rule.get('block_comment').split(' ')
        block = '{0[0]}(\s|.){0[1]}'.format(block)
        block_re = re.compile(r'%s' % block)

        return block_re, line_re
