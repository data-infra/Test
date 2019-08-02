import logging
logger = logging.getLogger('test')
logger.setLevel(logging.DEBUG)  # 输出所有大于INFO级别的log
fmt = logging.Formatter('%(name)s - %(levelname)s - %(asctime)s - %(message)s')
# 添加StreamHandler，并设置级别为WARNING
stream_hdl = logging.StreamHandler()
stream_hdl.setLevel(logging.DEBUG)
stream_hdl.setFormatter(fmt)
logger.addHandler(stream_hdl)
# 添加FileHandler，并设置级别为DEBUG
file_hdl = logging.FileHandler('test.log')
file_hdl.setLevel(logging.DEBUG)
file_hdl.setFormatter(fmt)
logger.addHandler(file_hdl)

logger.info('I am <info> message.')
logger.debug('I am <debug> message.')  # 不输出