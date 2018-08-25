# 用于文件的读取,包含配置文件和数据文件的读取函数.根据文件地址，返回文件中包含的内容

import yaml
import os
from xlrd import open_workbook

# 读取配置文件yaml文件成配置内容
class YamlReader:
    def __init__(self, yamlfilepath):
        if os.path.exists(yamlfilepath):
            self.yamlfilepath = yamlfilepath
        else:
            raise FileNotFoundError('文件不存在！')
        self._data = None

    @property
    def data(self):
        # 如果是第一次调用data，读取yaml文档，否则直接返回之前保存的数据
        if not self._data:
            with open(self.yamlfilepath, 'rb') as f:
                self._data = list(yaml.safe_load_all(f))  # load后是个generator，用list组织成列表
        return self._data


class SheetTypeError(Exception):
    pass

# 读取excel文件中的内容。返回list。
class ExcelReader:
    """
    如：
    excel中内容为：
    | A  | B  | C  |
    | A1 | B1 | C1 |
    | A2 | B2 | C2 |

    如果 print(ExcelReader(excel, title_line=True).data)，输出结果：
    [{A: A1, B: B1, C:C1}, {A:A2, B:B2, C:C2}]

    如果 print(ExcelReader(excel, title_line=False).data)，输出结果：
    [[A,B,C], [A1,B1,C1], [A2,B2,C2]]

    可以指定sheet，通过index或者name：
    ExcelReader(excel, sheet=2)
    ExcelReader(excel, sheet='BaiDuTest')
    """
    def __init__(self, excelpath, sheet=0, title_line=True):
        if os.path.exists(excelpath):
            self.excelpath = excelpath  # excel文件路径
        else:
            raise FileNotFoundError('文件不存在！')
        self.sheet = sheet   # sheet可以是int表示表格的索引，可以是str表示表格的名称
        self.title_line = title_line  # 是否存在标题行，有标题行，每一行都是都是对应列名的取值；没有标题行，每一行都是一个列表
        self._data = list()   # 用于存储每行生成的数据。

    @property
    def data(self):
        if not self._data:
            workbook = open_workbook(self.excelpath)
            if type(self.sheet) not in [int, str]:
                raise SheetTypeError('Please pass in <type int> or <type str>, not {0}'.format(type(self.sheet)))
            elif type(self.sheet) == int:
                s = workbook.sheet_by_index(self.sheet)
            else:
                s = workbook.sheet_by_name(self.sheet)

            if self.title_line:
                title = s.row_values(0)  # 首行为title
                for col in range(1, s.nrows):
                    # 依次遍历其余行，与首行组成dict，拼到self._data中
                    self._data.append(dict(zip(title, s.row_values(col))))
            else:
                for col in range(0, s.nrows):
                    # 遍历所有行，拼到self._data中
                    self._data.append(s.row_values(col))
        return self._data



if __name__ == '__main__':

    y = 'E:\Test_framework\config\config.yml'
    reader = YamlReader(y)
    print(reader.data)

    e = 'E:/Test_framework/data/baidu.xlsx'
    reader = ExcelReader(e, title_line=True)
    print(reader.data)



