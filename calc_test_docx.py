#!/usr/bin/env python
# -*- coding:utf-8 -*-
import datetime
import random
import time
from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt

TOPIC_NUM = 100
SYMBOL = ['+', '-']
REPEAT = False
NUM_LIMIT = 10
COLUMN_COUNT = 3


def calc(x, y, symbol):
    if symbol == '+':
        return x + y
    elif symbol == '-':
        return x - y
    elif symbol == '*':
        return x * y
    elif symbol == '/':
        if y == 0: return 9999
        if x % y != 0: return 9999
        return x / y


def generate():
    program = list()
    for _ in range(TOPIC_NUM):
        x = random.randint(0, NUM_LIMIT)
        y = random.randint(0, NUM_LIMIT)
        symbol = SYMBOL[random.randint(0, len(SYMBOL) - 1)]
        cur_time = time.time()
        while calc(x, y, symbol) > NUM_LIMIT or calc(x, y, symbol) < 0 or f"{x} {symbol} {y} =" in program:
            x = random.randint(0, NUM_LIMIT)
            y = random.randint(0, NUM_LIMIT)
            if time.time() - cur_time > 2:
                return program
        program.append(f"{x} {symbol} {y} =")
    return program


def set_section_columns(section, num_cols):
    """
    设置 Word 文档的部分为多栏布局
    :param section: 要设置的文档部分
    :param num_cols: 列数（如 2 表示两栏布局）
    """
    # 获取 section 对象的 'pgMar' 和 'cols' 属性
    sectPr = section._sectPr
    cols = sectPr.xpath('./w:cols')

    # 如果没有'cols'，则创建
    if not cols:
        cols = OxmlElement('w:cols')
        sectPr.append(cols)
    else:
        cols = cols[0]

    # 设置栏数
    cols.set(qn('w:num'), str(num_cols))


def generate_doc():
    doc = Document()
    for p in generate():
        p = doc.add_paragraph(p)
        p.runs[0].font.size = Pt(18)
    section = doc.sections[0]
    set_section_columns(section, COLUMN_COUNT)
    now = datetime.datetime.now()
    formatted_time = now.strftime("%y%m%d%H%M%S")
    doc.save(f"calc_test_{formatted_time}.docx")


if __name__ == '__main__':
    generate_doc()
