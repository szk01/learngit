'''
目的：填写client1表中的com_id字段

取到client1中的name, phone， position字段，再加上id字段。作为标识符 （只能找到没有被拆分的联系人起作用）
在ccompany表中找到相应的记录的id，e字段在ccompany表中
将id填写到client1中

取到
'''

import pymysql

db = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='nonghao')
cursor = db.cursor()


# # 取到client1表中的name, phone, position字段
# def get_client_name():
#     sql = "select name, phone, position from client1"
#     cursor.execute(sql)
#     resultes = cursor.fetchall()
#     for r in resultes:
#         yield r
#
#
# # 在ccompany表中查到对应的id， 将id填到client1表的com_code表中
# def get_id(name, phone, position):
#     sql = 'select id from ccompany where contact_name ="%s" AND contact_phone ="%s" AND contact_role ="%s"' % (name, phone, position)
#     cursor.execute(sql)
#     result = cursor.fetchone()
#     print('result', result)
#     return result
#
#
# # 两个字段找到对应的id
# def get_id_byTwo(name, position):
#     sql = 'select id from ccompany where contact_name ="%s" AND contact_role ="%s"' % (name, position)
#     cursor.execute(sql)
#     result = cursor.fetchone()
#     print('result', result)
#     return result
#
#
# # 将得到的id写入client1的记录中
# def update_comId_by_two(id, name, position):
#     sql = "update client1 set com_id=%s where name=%s AND position = %s"
#     try:
#         cursor.execute(sql, (id, name, position))
#         print('更新成功', id)
#         db.commit()
#     except Exception as e:
#         print('更新失败', e)
#
#
# # 将得到的id更新到对应的记录
# def update_comId(id, name, phone, position):
#     sql = "update client1 set com_id=%s where name=%s AND phone=%s AND position = %s"
#     try:
#         cursor.execute(sql, (id, name, phone, position))
#         print('更新成功')
#         db.commit()
#     except Exception as e:
#         print('更新失败', e)
#
#
# # 重置com_Id字段
# def reset_comId():
#     sql = "update client1 set com_id=0"
#     try:
#         cursor.execute(sql)
#         print('更新成功')
#         db.commit()
#     except Exception as e:
#         print('更新失败', e)
#
#
# if __name__ == '__main__':
#     # # 重置com_Id
#     # reset_comId()
#
#     # 更改com_Id
#     ds = get_client_name()
#     for d in ds:
#         if 'e' in d[1]:                                 # 如果其中包含e，则只用两个标准对照
#             result = get_id_byTwo(d[0], d[2])
#             update_comId_by_two(result[0], d[0], d[2])
#         else:
#             result = get_id(d[0], d[1], d[2])
#             update_comId(result[0], d[0], d[1], d[2])
#
#     # 测试get_id函数
#     # id = get_id('徐思康', '13631222239', '销售')
#     #     # print('id', id[0])

'''
先写最简单的，一个名字对应一个字段
如果client1表中的name字段，值只有一个，不包含，,.、符号
    设置com_id的值和id值一样
    设置不成功，跳过这个设置
'''


# 是否包含这些标点符号
def is_marks(string, marks):
    for i in range(0, len(marks)):
        if marks[i] in string:
            return True
        else:
            i += 1


# 拿到client1表中的所有id,以此来循环迭代
def get_ids():
    '''
    得到的结果是(
        (1,), (2,), (3,), (4,), (5,),
    )
    '''
    sql = "select id from client1"
    cursor.execute(sql)
    ids = cursor.fetchall()
    return ids


# 根据id得到name，然后判断
def getName_byId(id):
    sql = "select name from client1 where id=%s"
    cursor.execute(sql, (id))
    name = cursor.fetchone()
    return name[0]


# 设置com_id和id一样
def set_comId(id):
    sql = "update client1 set com_id=%s where id=%s"
    cursor.execute(sql, (id, id))
    db.commit()


# 主逻辑
def main():
    ids = get_ids()
    for i in range(0, len(ids)):
        id = ids[i][0]
        # print('id', id)
        name = getName_byId(id)
        if is_marks(name, [',', '，', '.', '、', '/']):
            i += 1
        else:
            try:
                set_comId(id)
                print('更新成功', i, name)
            except Exception as e:
                i += 1


if __name__ == '__main__':
    # ids = get_ids()
    # print('ids', ids)
    main()















