# -*- coding: utf-8 -*- 
# @Time : 2/7/21 4:36 PM 
# @Author : mxt
# @File : __init__.py
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
            content = data.get('diff')
            add_content = [_ for _ in content.split('\n') if _.startswith('+')]
            del_content = [_ for _ in content.split('\n') if _.startswith('-')]

            # 扫描所有空行数
            add_empty = len(add_content) - len([_ for _ in add_content if len(_.replace('+', '')) != 0])
            del_empty = len(del_content) - len([_ for _ in del_content if len(_.replace('-', '')) != 0])

            # 扫描注释行
            block, b_re, line, l_re = self._re_rule.get(suffix)
            if block and isinstance(block, bool):
                continue
            block_content = block.findall(content)
            add_block, del_block = self._replace_iter(block_content, b_re)
            line_content = line.findall(content)
            add_line, del_line = self._replace_iter(line_content, l_re)

            # 去除空行之后的总行
            add_content = [_ for _ in add_content if len(_.replace('+', '')) != 0]
            del_content = [_ for _ in del_content if len(_.replace('-', '')) != 0]

            # 注释的空行数
            notes_add_empty = len(add_block) - len([_ for _ in add_block if len(_.replace('+', '')) != 0])
            notes_del_empty = len(del_block) - len([_ for _ in del_block if len(_.replace('+', '')) != 0])

            # 实际空行数
            self._addEmptyCodeLine = add_empty - notes_add_empty
            self._delEmptyCodeLine = del_empty - notes_del_empty

            # 去除空行之后的注释行
            add_block = [_ for _ in add_block if len(_.replace('+', '')) != 0]
            del_block = [_ for _ in del_block if len(_.replace('-', '')) != 0]

            # 过滤注释行
            add_content = _calculate_list_diff(_calculate_list_diff(add_content, add_block), add_line)
            del_content = _calculate_list_diff(_calculate_list_diff(del_content, del_block), del_line)

            # 实际有效代码行数
            self._addCodeLine = len(add_content)
            self._delCodeLine = len(del_content)

            # 实际注释行数
            self._addNotesCodeLine = len(add_block) + len(add_line)
            self._addNotesCodeLine = len(del_block) + len(del_line)

    @staticmethod
    def _replace_iter(content_list: list, re_rule: list):
        add = list()
        delete = list()
        for content in content_list:
            for _ in re_rule:
                content = content.replace(_, '', 1)
            add += [_ for _ in content.split('\n') if _.startswith('+')]
            delete += [_ for _ in content.split('\n') if _.startswith('-')]
        return add, delete

    def result(self):
        return {"addCode": self._addCodeLine, "delCode": self._delCodeLine,
                "addNotes": self._addNotesCodeLine, "delNotes": self._delNotesCodeLine,
                "addEmpty": self._addEmptyCodeLine, "delEmpty": self._delEmptyCodeLine}
