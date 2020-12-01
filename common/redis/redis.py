from flask import current_app
import redis


class Redis(object):
    """redis数据库操作"""

    def __init__(self):
        host = current_app.config['REDIS_HOST']
        port = current_app.config['REDIS_PORT']
        db = current_app.config['REDIS_DB']
        self.redis_obj = redis.StrictRedis(host, port, db)

    def write(self, key, value, expire=None):
        """写入键值对"""
        self.redis_obj.set(key, value, ex=expire)

    def read(self, key):
        """读取键值对内容"""
        value = self.redis_obj.get(key)
        return value.decode('utf-8') if value else value

    def hset(self, name, key, value):
        """写入hash表"""
        self.redis_obj.hset(name, key, value)

    def hmset(self, key, *value):
        """读取指定hash表的所有给定字段的值"""
        value = self.redis_obj.hmset(key, *value)
        return value

    def hget(self, name, key):
        """读取指定hash表的键值"""
        value = self.redis_obj.hget(name, key)
        return value.decode('utf-8') if value else value

    def hgetall(self, name):
        """获取指定hash表所有的值"""
        return self.redis_obj.hgetall(name)

    def delete(self, *names):
        """删除一个或者多个"""
        self.redis_obj.delete(*names)

    def hdel(self, name, key):
        """删除指定hash表的键值"""
        self.redis_obj.hdel(name, key)

    def expire(self, name, expire=None):
        """设置过期时间"""
        self.expire(name, expire)
