# pycharm中如果无法引入自定义模块，要先在pycharm中右键点击项目根目录->标记目录为Resource Root，然后再右键点击项目根目录->根源。这样就能引用项目根目录下的所有自定义模块了。
import sys
import os
dir_common = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(dir_common)   # 将根目录添加到系统目录,才能正常引用其他文件的内容
print('系统根目录',dir_common)

