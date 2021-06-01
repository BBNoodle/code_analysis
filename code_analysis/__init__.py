# -*- coding: utf-8 -*- 
# @Time : 2/7/21 4:36 PM 
# @Author : mxt
# @File : __init__.py
import re
from six.moves import xrange
from code_analysis.re_statement import RegularRule


def _calculate_list_diff(target: list, be_subtracted: list, is_add: bool):
    _surplus = list()
    symbol = "+" if is_add else "-"
    target = target.copy()
    for item in be_subtracted:
        try:
            index = target.index(item.replace(symbol, '').replace('\t', '').replace(' ', ''))
            del target[index]
        except:
            del_temp = [_.replace(symbol, '').replace('\t', '').replace(' ', '') for _ in target]
            if item.replace(symbol, '').replace('\t', '').replace(' ', '') in del_temp:
                index = del_temp.index(item.replace(symbol, '').replace('\t', '').replace(' ', ''))
                del target[index]
            else:
                _surplus.append(item)
    return _surplus


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
            block_content = list()
            if len(data.get('diff')) == 0:
                continue
            suffix = data['newPath'].split('.')[-1].lower()
            content = data.get('diff').split('\n', maxsplit=1)[1]
            add_content = [_ for _ in content.split('\n') if _.startswith('+')]
            del_content = [_ for _ in content.split('\n') if _.startswith('-')]

            # 扫描注释行
            block, line = self._re_rule.get(suffix)
            if block and isinstance(block, bool):
                continue
            for _ in block.findall(content):
                if isinstance(_.split('\n'), list):
                    block_content += _.split('\n')
                else:
                    block_content.append(_)
            block_content = self._scan_content_symbol(add_content, del_content, block_content)
            add_notes_block, del_notes_block = self._replace_iter(block_content)
            line_content = self._scan_content_symbol(add_content, del_content, line.findall(content))
            add_notes_line, del_notes_line = self._replace_iter(line_content)

            add_remove_empty = len([_ for _ in add_content if len(_.replace('+', '')) != 0])
            del_remove_empty = len([_ for _ in del_content if len(_.replace('-', '')) != 0])

            # 注释行数
            self._addNotesCodeLine += len(add_notes_block) + len(add_notes_line)
            self._delNotesCodeLine += len(del_notes_block) + len(del_notes_line)

            # 扫描所有空行数
            self._addEmptyCodeLine += len(add_content) - add_remove_empty
            self._delEmptyCodeLine += len(del_content) - del_remove_empty

            add_code = add_remove_empty - len(add_notes_block) - len(add_notes_line)
            del_code = del_remove_empty - len(del_notes_block) - len(del_notes_line)

            # 有效代码行数
            self._addCodeLine += add_code
            self._delCodeLine += del_code

    @staticmethod
    def _scan_content_symbol(add_list: list, delete_list: list, line_content_list: list):
        add_list = [_ for _ in add_list if _ not in _calculate_list_diff(line_content_list, add_list, True)]
        del_list = [_ for _ in delete_list if _ not in _calculate_list_diff(line_content_list, delete_list, False)]
        return add_list + del_list

    @staticmethod
    def _replace_iter(content_list: list):
        add = list()
        delete = list()
        for content in content_list:
            add += [_ for _ in content.split('\n') if _.startswith('+')]
            delete += [_ for _ in content.split('\n') if _.startswith('-')]
        return add, delete

    def result(self):
        return {"addCode": self._addCodeLine, "delCode": self._delCodeLine,
                "addNotes": self._addNotesCodeLine, "delNotes": self._delNotesCodeLine,
                "addEmpty": self._addEmptyCodeLine, "delEmpty": self._delEmptyCodeLine}
