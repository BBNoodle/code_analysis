# -*- coding: utf-8 -*- 
# @Time : 2/7/21 4:36 PM 
# @Author : mxt
# @File : __init__.py
import re
from code_analysis.re_statement import RegularRule


def _calculate_list_diff(target: list, be_subtracted: list):
    for item in be_subtracted:
        try:
            index = target.index(item)
            del target[index]
        except:
            target.append(item)
    return target


class CodeAnalysis:
    # 新增代码行数
    _addCodeLine = 0
    # 删除代码行数
    _delCodeLine = 0
    # 新增注释代码行数
    _addNotesCodeLine = 0
    # 删除注释代码行数
    _delNotesCodeLine = 0
    # 新增空行
    _addEmptyCodeLine = 0
    # 删除空行
    _delEmptyCodeLine = 0

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
            return self._addCodeLine, self._delCodeLine, self._addNotesCodeLine, \
                   self._delNotesCodeLine, self._addEmptyCodeLine, self._delEmptyCodeLine

        for data in self.datas:
            suffix = data['newPath'].split('.')[-1]
            content = data.get('diff').split('\n', maxsplit=1)[1]
            add_content = [_ for _ in content.split('\n') if _.startswith('+')]
            del_content = [_ for _ in content.split('\n') if _.startswith('-')]

            # 扫描所有空行数
            self._addEmptyCodeLine = len(add_content) - len([_ for _ in add_content if len(_.replace('+', '')) != 0])
            self._delEmptyCodeLine = len(del_content) - len([_ for _ in del_content if len(_.replace('-', '')) != 0])

            # 扫描注释行
            block, b_re, line, l_re = self._re_rule.get(suffix)
            if block and isinstance(block, bool):
                continue
            block_content = block.findall(content)
            add_notes_block, del_notes_block = self._replace_iter(block_content, b_re)
            line_content = line.findall(content)
            add_notes_line, del_notes_line = self._replace_iter(line_content, l_re)

            # 注释行数
            self._addNotesCodeLine = len(add_notes_block) + len(add_notes_line)
            self._delNotesCodeLine = len(del_notes_block) + len(del_notes_line)

            # 有效代码行数
            self._addCodeLine = len(add_content) - self._addEmptyCodeLine - self._addNotesCodeLine
            self._delCodeLine = len(del_content) - self._delEmptyCodeLine - self._delNotesCodeLine

    @staticmethod
    def _replace_iter(content_list: list, re_rule: list):
        add = list()
        delete = list()
        for content in content_list:
            add.append(re_rule[0])
            delete.append(re_rule[0])
            add += [_ for _ in content.split('\n') if _.startswith('+')]
            delete += [_ for _ in content.split('\n') if _.startswith('-')]
        add = list() if len(add) == len(content_list) else add
        delete = list() if len(delete) == len(content_list) else delete
        return add, delete

    def result(self):
        return {"addCode": self._addCodeLine, "delCode": self._delCodeLine,
                "addNotes": self._addNotesCodeLine, "delNotes": self._delNotesCodeLine,
                "addEmpty": self._addEmptyCodeLine, "delEmpty": self._delEmptyCodeLine}
