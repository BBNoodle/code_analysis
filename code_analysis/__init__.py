# -*- coding: utf-8 -*- 
# @Time : 2/7/21 4:36 PM 
# @Author : mxt
# @File : __init__.py
import re

from code_analysis.re_statement import RegularRule


class CodeAnalysis:
    # 新增代码行数
    _addCodeLine = 0
    # 删除代码行数
    _delCodeLine = 0
    # 有效代码行数
    _effectiveCodeLine = 0
    # 注释代码行数
    _notesCodeLine = 0
    # 空行
    _emptyCodeLine = 0

    def __init__(self, datas=None):
        self._re_rule = RegularRule()
        if datas is None:
            datas = list()
        self.datas = datas
        self._main()

    def _main(self):
        """
        CodeAnalysis主要入口
        :return:
        """
        if len(self.datas) == 0:
            return self._addCodeLine, \
                   self._delCodeLine, \
                   self._effectiveCodeLine, \
                   self._notesCodeLine, \
                   self._emptyCodeLine

        for data in self.datas:
            suffix = data['newPath'].split('.')[-1]
            block, line = self._re_rule.get(suffix)
            block_content = block.match(data['diff'])
            line_content = line.match(data['diff'])

    def _delete_files(self, delete, _rule):
        for del_str in delete:
            if len(del_str) == 0:
                self._emptyCodeLine -= 1
            line_comment = re.findall(r'^%s.*' % _rule['line_comment'], del_str)
            block_comment = re.findall(r'^%s.*' % _rule['block_comment'], del_str)
            self._notesCodeLine -= len(line_comment)
            self._notesCodeLine -= len(block_comment)
            self._effectiveCodeLine = len(delete) + self._notesCodeLine + self._emptyCodeLine
            self._delCodeLine += self._effectiveCodeLine

    def result(self):
        return {"add": self._addCodeLine,
                "del": self._delCodeLine,
                "effect": self._effectiveCodeLine,
                "notes": self._notesCodeLine,
                "empty": self._emptyCodeLine}
