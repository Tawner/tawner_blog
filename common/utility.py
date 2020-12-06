import hashlib, random, string
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app


def md5(content):
    """
    md5加密函数
    :param content: [str|bytes] 要加密的内容
    :return:
    """
    res = hashlib.md5(content).hexdigest() if isinstance(content, bytes) else hashlib.md5(content.encode()).hexdigest()
    return res


def random_str(str_type=0, length=6):
    """
    生成随机字符串
    :param str_type: [int] 字符串类型,0小写，1大写，2数字，3小写+数字，4大写+数字，5大小写，6大小写数字
    :param length: [int] 长度
    :return:
    """
    type_dict = {
        0: string.ascii_lowercase,
        1: string.ascii_uppercase,
        2: string.digits,
        3: string.ascii_lowercase + string.digits,
        4: string.ascii_uppercase + string.digits,
        5: string.ascii_letters,
        6: string.ascii_letters + string.digits
    }
    return ''.join(random.sample(type_dict.get(str_type, type_dict[0]), length))


def encrypt(data, expire=7*86400):
    """
    字典生成加密字符串函数
    :param data [dict] 需要加密的数据
    :param expire [int] 过期时间单位秒
    :return:
    """
    s = Serializer(current_app.config["SECRET_KEY"], expires_in=expire)
    return s.dumps(data).decode("ascii")


def decrypt(encrypt_str):
    """
    解密函数
    :param encrypt_str [str] 要解密的字符串
    :return:
    """
    s = Serializer(current_app.config["SECRET_KEY"])
    try:
        data = s.loads(encrypt_str)
    except Exception:
        return None
    return data


def file_size(size):
    """计算文件大小"""
    if size >= 1024 ** 3:  # G
        return '%.2fG' % (size / (1024 ** 3))
    elif size >= 1024 ** 2: # M
        return '%.2fM' % (size / (1024 ** 2))
    elif size >= 1024:  # KB
        return '%.2fKB' % (size / 1024)
    else:  # B
        return '%.2fB' % size
