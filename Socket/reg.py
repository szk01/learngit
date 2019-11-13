# 注册正则表达式

from werkzeug.routing import BaseConverter


# 注册正则表达式匹配路由
class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]
