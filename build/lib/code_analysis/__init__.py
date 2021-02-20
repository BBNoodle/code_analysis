# -*- coding: utf-8 -*- 
# @Time : 2/7/21 4:36 PM 
# @Author : mxt
# @File : __init__.py

import re


PY_RULE = {
    "block_comment": ['"""', "'''"],
    "line_comment": "#"
}

JAVA_RULE = {
    "block_comment": '/*',
    "line_comment": "//"
}

HTML_RULE = {
    "block_comment": "<!--",
    "line_comment": "<!--"
}

CSS_RULE = {
    "block_comment": '/*',
    "line_comment": "/*"
}

JS_RULE = {
    "block_comment": '/*',
    "line_comment": "//"
}

SQL_RULE = {
    "block_comment": "/*",
    "line_comment": ["-- ", "#"]
}

SH_RULE = {
    "block_comment": "#",
    "line_comment": "#"
}


def get_rule(_path):
    if _path.split('.')[-1] == 'py':
        return PY_RULE
    elif _path.split('.')[-1] == 'java':
        return JAVA_RULE
    elif _path.split('.')[-1] == 'html':
        return HTML_RULE
    elif _path.split('.')[-1] in ['js', 'vue', 'ts', 'xml']:
        return JS_RULE
    elif _path.split('.')[-1] == 'css':
        return CSS_RULE


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
        if datas is None:
            datas = list()
        self.datas = datas
        self._main()

    def _main(self):
        if len(self.datas) == 0:
            return self._addCodeLine, \
                   self._delCodeLine, \
                   self._effectiveCodeLine, \
                   self._notesCodeLine, \
                   self._emptyCodeLine

        for data in self.datas:
            rule = get_rule(data['newPath'])
            add = [_[1:].lstrip() for _ in data['diff'].split('\n') if _.startswith('+')]
            delete = [_[1:].lstrip() for _ in data['diff'].split('\n') if _.startswith('-')]
            if data['deletedFile']:
                self.delete_files(delete, rule)
            elif data['newFile']:
                self.new_files(add, rule)
            else:
                self.old_files(add, delete, rule)

    def new_files(self, add, _rule):
        for add_str in add:
            if len(add_str) == 0:
                self._emptyCodeLine += 1
            line_comment = re.findall(r'^%s.*' % _rule['line_comment'], add_str)
            block_comment = re.findall(r'^%s.*' % _rule['block_comment'], add_str)
            self._notesCodeLine += len(line_comment)
            self._notesCodeLine += len(block_comment)
            self._effectiveCodeLine = len(add) + self._notesCodeLine + self._emptyCodeLine
            self._addCodeLine += self._effectiveCodeLine

    def old_files(self, add, delete, _rule):
        self.new_files(add, _rule)
        self.delete_files(delete, _rule)

    def delete_files(self, delete, _rule):
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
        return self._addCodeLine, self._delCodeLine, self._effectiveCodeLine, self._notesCodeLine, self._emptyCodeLine
