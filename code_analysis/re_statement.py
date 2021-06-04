# -*- coding: utf-8 -*- 
# @Time : 2/24/21 9:56 AM 
# @Author : mxt
# @File : re_statement.py

import re

from code_analysis.configure import *


class RegularRule:
    _DEFAULT_LIST = [
        'c', 'h', 'hpp', 'hxx', 'cpp', 'cc', 'cxx', 'C', 'c++',
        'cs', 'java',
        'js', 'vue', 'ts', 'tsx', 'less', 'scss', 'ftl', 'properties', 'jsp'
    ]

    def get(self, item='c'):
        """
        直接获取相应语言的正则表达式
        :param item:
        :return:
        """
        if item == 'py':
            file_type = "PY"
            file_suffix = PY_RULE
        elif item == "xml":
            file_type = "FRONTEND"
            file_suffix = XML_RULE
        elif item == "html":
            file_type = "DEFAULT"
            file_suffix = HTML_RULE
        elif item in self._DEFAULT_LIST:
            file_type = "DEFAULT"
            file_suffix = DEFAULT_RULE
        elif item in ['css', 'sass', 'php']:
            file_type = "FRONTEND"
            file_suffix = CSS_PHP_RULE
        elif item == 'jsp':
            file_type = "FRONTEND"
            file_suffix = JSP_RULE
        elif item == 'ftl':
            file_type = "FRONTEND"
            file_suffix = FTL_RULE
        elif item == 'sql':
            file_type = "SQL"
            file_suffix = SQL_RULE
        elif item in ['sh', 'properties']:
            file_type = "SH"
            file_suffix = SH_RULE
        else:
            return True, False

        return self._str2re(file_suffix, file_type)

    @staticmethod
    def _str2re(_rule: dict, file_type: str):
        if file_type == "FRONTEND":
            line = _rule.get('line_comment').split(' ')
            line_re_str = u'{0[0]}[\s\S]*?{0[1]}'.format(line)
            line_regular = re.compile(r'%s' % line_re_str, re.S)
        elif file_type == "SH":
            line = _rule.get('line_comment').split(' ')[:1]
            line_re_str = u'%s(.*?)\n' % line[0]
            line_regular = re.compile(r'%s' % line_re_str, re.S)
            return line_regular, line_regular
        else:
            line = _rule.get('line_comment').split(' ')[:1]
            line_re_str = u'%s.*?(?=\n)' % line[0]
            line_regular = re.compile(r'%s' % line_re_str, re.S)

        block = _rule.get('block_comment').split(' ')
        block_re_str = u'{0[0]}[\s\S]*?{0[1]}'.format(block)
        block_regular = re.compile(r'%s' % block_re_str, re.S)

        return block_regular, line_regular
