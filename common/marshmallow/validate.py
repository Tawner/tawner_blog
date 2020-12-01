from common.models import *
"""校验器"""


class choice:
    """选择范围"""
    def __init__(self, array):
        self.array = array

    def __call__(self, vaule):
        return True if vaule in self.array else False


class str_range(object):
    """字符串长度"""
    def __init__(self, low, high, argument='argument'):
        self.low = low
        self.high = high
        self.argument = argument

    def __call__(self, value):
        if len(value) <= self.low or len(value) >= self.high:
            error = ('Invalid {arg}: {val}. {arg} length must be within the range {lo} - {hi}'
                     .format(arg=self.argument, val=value, lo=self.low, hi=self.high))
            raise ValueError(error)
        return value


def positive(value):
    """正整数"""
    return True if value > 0 else False


def natural(value):
    """自然数"""
    return True if value >= 0 else False





class date_time:
    """时间格式化"""
    def __init__(self, time_format='%Y-%m-%d', argument='argument'):
        self.time_format = time_format
        self.argument = argument

    def __call__(self, value):
        if isinstance(value, int):
            return datetime.fromtimestamp(value)
        elif isinstance(value, str):
            try:
                value = datetime.strptime(value, self.time_format)
            except:
                raise ValueError(self.argument + '参数格式错误，格式：%s' % self.time_format)
            return value
        else:
            raise ValueError(self.argument + '参数格式错误，格式：%s' % self.time_format)


class data_exist:
    """数据存在判断"""
    def __init__(self, model):
        self.model = model

    def __call__(self, value):
        obj = self.model.query.filter(self.model.id == value, self.model.is_delete == 0).first()
        return True if obj else False


class category_exist:
    """校验栏目"""
    def __init__(self, module=None, level=None):
        self.module = module
        self.level = level

    def __call__(self, value):
        query_args = [Category.id == value, Category.is_delete == 0]
        if self.module:
            query_args.append(Category.module == self.module)
        if self.level:
            query_args.append(Category.level == self.level)
        obj = Category.query.filter(*query_args).first()
        return True if obj else False


def image_exist(value):
    image = Upload.query.filter(Upload.is_delete == 0, Upload.file_type == 0, Upload.id == value).first()
    return True if image else False




