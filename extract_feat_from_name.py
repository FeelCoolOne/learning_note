# encoding:utf-8
from pymongo import MongoClient
import ConfigParser
from difflib import SequenceMatcher
import re
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def is_chinese(uchar):
    if u'\u4e00' <= uchar <= u'\u9fff':
        return True
    else:
        return False


def is_number(uchar):
    if u'\u0030' <= uchar <= u'\u0039':
        return True
    else:
        return False


def is_alphabet(uchar):
    if (u'\u0041' <= uchar <= u'\u005a') or (u'\u0061' <= uchar <= u'\u007a'):
        return True
    else:
        return False


def is_other(uchar):
    if not (is_chinese(uchar) or is_number(uchar) or is_alphabet(uchar)):
        return True
    else:
        return False


def get_info(config):
    """
    get connection from mongoDB
    """
    cf = ConfigParser.ConfigParser()
    cf.read(config)
    address = cf.get('mongo', 'address')
    port = int(cf.get('mongo', 'port'))
    username = cf.get('mongo', 'username')
    password = cf.get('mongo', 'password')
    database = cf.get('mongo', 'database')
    collection = cf.get('mongo', 'collection')

    con = MongoClient(address, port)
    EPGInfo = con[database]
    EPGInfo.authenticate(username, password)
    collection = EPGInfo[collection]
    return collection


def com_len(string1, string2):
    match = SequenceMatcher(None, string1, string2).find_longest_match(0, len(string1), 0, len(string2))
    return match.size


def delete_nonsense(string):
    words_ns = [u"\\u4e4b", u"\u4e4b", u"\u7684", u"\uff1a", u"\uff01", " ",
                u"\uff08", u"\uff09", u"\u300a", u"\u300b", u"\uff1f", u"\u002d", r"\(", r"\)", u"\!",
                u"\u666e\u901a\u8bdd\u7248", u"\u53f0\u8bed\u7248", u"\u756a\u5916\u7bc7",
                u"\u65e5\u8bed\u7248", u"\u7ca4\u8bed\u7248", u"\u7cbe\u7f16\u7248",
                u"\u65e5\u6587\u7248", u"\u5408\u96c6", u"\u4e2d\u6587\u7248",
                u"\u4e1c\u5317\u65b9\u8a00\u7248", u"\u5267\u573a\u7248", u"\u73af\u7ed5\u58f0\u7248",
                u"\u0032\u0030\u0030\u0031\u7248", u"\u7535\u5f71\u7248", u"\u603b\u7bc7",
                u"\u82f1\u6587\u7248", u"\u52a8\u753b", u"\u96c6\u9526", u"\u4f5c\u54c1\u96c6",
                u"\u52a0\u957f\u7248", u"\u5927\u7535\u5f71", u"\u7cbe\u534e\u7248",
                u"\u914d\u97f3\u7248", u"\u4e1c\u5317\u7248", u"\u4e0a\u6d77\u65b9\u8a00\u7248",
                u"\u7cbe\u9009\u96c6", u"\u52a8\u753b\u7248", u"\u56db\u5ddd\u7248", u"\u4e2d\u914d\u7248",
                u"\u5916\u4f20", u"\u56db\u5ddd\u8bdd\u7248", u"\u9655\u897f\u65b9\u8a00\u7248",
                u"\u7cfb\u5217", u"\u9ad8\u6e05\u7248", u"\u65e5\u5e38\u7bc7", u"\u0054\u0056\u7248",
                u"\u5170\u5dde\u65b9\u8a00\u7248", u"\u7ecf\u5178\u7248", u"\u82f1\u8bed\u7248",
                u"\u666e\u901a\u8bdd\u7248", u"\u7279\u522b\u7bc7", u"\u7279\u522b\u7248",
                u"\u8fde\u8f7d\u0032\u0030\u5e74", u"\u6f6e\u6c55\u7248", u"\u65b9\u8a00\u7248",
                u"\u5361\u901a\u7248", u"\u52a8\u6001\u6f2b\u753b", "·", ]
    pat_ns = [u"\u7b2c[\u4e00,\u4e8c,\u4e09,\u56db,\u4e94,\u516d,\u4e03,\u516b,\u4e5d,\u5341]\u5b63", u"\u7b2c[0-9]\u5b63",
              u"\u7b2c[\u4e00,\u4e8c,\u4e09,\u56db,\u4e94,\u516d,\u4e03,\u516b,\u4e5d,\u5341]\u90e8", u"\u7b2c[0-9]\u90e8",
              u"\u7b2c[\u4e00,\u4e8c,\u4e09,\u56db,\u4e94,\u516d,\u4e03,\u516b,\u4e5d,\u5341]\u671f", u"\u7b2c[0-9]\u671f",
              u"[\u4e00,\u4e8c,\u4e09,\u56db,\u4e94,\u516d,\u4e03,\u516b,\u4e5d,\u5341]{1}$", u"[\d]{1,4}$",
              u"[\u4e0a,\u4e0b]\u90e8$", u"[\d]{4}\u7248", ]
    for p in words_ns:
        string = re.sub(p, "", string)
    for p in pat_ns:
        string = re.sub(p, "", string)
    return string


# if __name__ == "__main__":

    # config = "./config.ini"
    # col = get_info(config)
    # condition = {"model": "cartoon"}
    # docs = col.find(condition, projection={"name": 1})

    # name_set_list = list()
    # name_list = list()
    # size = 0
    # for doc in docs:
    #     d = dict(doc)
    #     name_list.append(d["name"])
    #     size += 1
    # with open("./name_new.txt", "w") as g, open("name.txt", 'r') as f:
    #     for name in f:
    #         g.write(delete_nonsense(name.strip().decode("utf-8")) + "\n")
    # raise
    # for name in name_list:
    # focus = name_list[4]
    # # focus = u"\u5fcd\u8005\u795e\u9f9f"
    # value = [com_len(focus, name) for name in name_list]
    # si = sorted(range(len(name_list)), key=lambda x: value[x], reverse=True)[:10]
    # # print(focus)
    # for i in si:
    #     print name_list[i]
