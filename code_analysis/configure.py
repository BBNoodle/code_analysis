# -*- coding: utf-8 -*- 
# @Time : 2/24/21 9:30 AM 
# @Author : mxt
# @File : configure.py

# Python
PY_RULE = {
    "block_comment": '""" """',
    "line_comment": "#"
}

# C, C++, C#, JAVA, JS, le
DEFAULT_RULE = {
    "block_comment": '/\* \*/',
    "line_comment": "\/\/"
}

# XML
XML_RULE = {
    "block_comment": "<!-- -->",
    "line_comment": "<!-- -->"
}

# HTML
HTML_RULE = {
    "block_comment": "<!-- -->",
    "line_comment": "\/\/"
}

# JSP
JSP_RULE = {
    "block_comment": "<%-- --%>",
    "line_comment": "<%-- --%>"
}

# FTL
FTL_RULE = {
    "block_comment": "<#-- -->",
    "line_comment": "<#-- -->"
}

CSS_PHP_RULE = {
    "block_comment": '/\* \*/',
    "line_comment": "/\* \*/"
}

SQL_RULE = {
    "block_comment": "/\* \*/",
    "line_comment": "-- "
}

SH_RULE = {
    "block_comment": "#",
    "line_comment": "# "
}
