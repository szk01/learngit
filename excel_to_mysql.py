import xlrd
import pymysql


# 从excel中拿到相应的数据,公司表
def read_excel(path):
    workbook = xlrd.open_workbook(path)         # 读取excel
    # print( workbook.sheet_names())
    sheet = workbook.sheet_by_name('Data')     # 读取到一张表
    print('行数', sheet.nrows)
    print('列数', sheet.ncols)
    rs = sheet.nrows
    # cs = sheet.ncols
    cx = [0, 1, 2, 3, 13, 9, 10]

    # 需要的记录放入一个数组中
    for i in range(1, rs):
        info = []
        for j in cx:
            sc = sheet.cell_value(i, j)
            info.append(sc)
        yield info


# 插入到数据库(公司表)
def save_to_MYSQL(datas):
    # 连接到数据库
    db = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='nonghao')
    cursor = db.cursor()
    sql = "INSERT INTO ccompany1(id, c_code, name, phone, address, industy, route_range) values(%s,%s,%s,%s,%s,%s,%s)"
    for data in datas:
        try:
            print('data', data)
            # print(data['novel_name'])
            cursor.execute(sql, (data[0], data[1], data[2], data[3], data[4], data[5], data[6]))
            db.commit()
            print('插入数据成功', data[2])
        except Exception as e:
            print('插入数据失败！！', e)
            db.rollback()


# 从excel拿到客户表（联系人表）， 只有一个姓名的
def read_excel_client(path):
    workbook = xlrd.open_workbook(path)         # 读取excel
    # print( workbook.sheet_names())
    sheet = workbook.sheet_by_name('Data')     # 读取到一张表
    print('行数', sheet.nrows)
    print('列数', sheet.ncols)
    rs = sheet.nrows
    # cs = sheet.ncols
    cx = [0, 21, 22, 25, 28, 31, 32]

    # 需要的记录放入一个数组中
    for i in range(1, rs):
        info = []
        for j in cx:
            sc = sheet.cell_value(i, j)
            info.append(sc)

        if info[1] != '' and type(info[1]) == str:                                       # 姓名为空，或者联系人有多个，跳过这个联系人
            if is_marks(info[1], [',', '、', '，', '.']):
                pass
            else:
                yield info


# 一个名字拓展成数组
def name_to_array(names):
    for n in names:
        extend = ['', '', '', '', '']                       # 放在这里每次都会重写extend列表
        extend.insert(1, n)
        yield extend


# 处理很多名字
def excute_names(path):
    workbook = xlrd.open_workbook(path)         # 读取excel
    # print( workbook.sheet_names())
    sheet = workbook.sheet_by_name('Data')     # 读取到一张表
    print('行数', sheet.nrows)
    print('列数', sheet.ncols)
    rs = sheet.nrows
    # cs = sheet.ncols
    cx = [0, 21, 22, 25, 28, 31, 32]

    # 需要的记录放入一个数组中
    for i in range(1, rs):
        info = []
        for j in cx:
            sc = sheet.cell_value(i, j)
            info.append(sc)

        if info[1] != '' and type(info[1]) == str:                                       # 姓名为空，或者联系人有多个，跳过这个联系人
            if is_marks(info[1], [',', '、', '，', '.']):
                names = spilt_str([',', '、', '，', '.'], info[1])
                print('names', names)
                clients = name_to_array(names)
                extend_MYSQL_client(clients)


# 添加多个名字的客户到表
def extend_MYSQL_client(datas):
    # 连接到数据库
    db = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='nonghao')
    cursor = db.cursor()
    sql = "INSERT INTO client1(name) values(%s)"
    for data in datas:
        try:
            # print(data['novel_name'])
            cursor.execute(sql, (data[1]))
            print('data[1]', data[1])
            db.commit()
            print('插入数据成功', data[1])
        except Exception as e:
            print('插入数据失败！！', e)
            db.rollback()



# 是否有标点
def is_marks(string, marks):
    for i in range(0, len(marks)):
        if marks[i] in string:
            return True
        else:
            i += 1


# 根据marks中存在的字符分割字符串，分割字符串
def spilt_str(marks, string):
    for i in range(0, len(marks)):
        if marks[i] in string:
            return string.split(marks[i])
        else:
            i += 1


# 插入到数据库(客户表)
def save_to_MYSQL_client(datas):
    # 连接到数据库
    db = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='nonghao')
    cursor = db.cursor()
    sql = "INSERT INTO client1(id, name, sex, phone, email, position, qq) values(%s,%s,%s,%s,%s,%s,%s)"
    for data in datas:
        try:
            print('data', data)
            # print(data['novel_name'])
            cursor.execute(sql, (data[0], data[1], data[2], data[3], data[4], data[5], data[6]))
            print('data[1]', data[1])
            db.commit()
            print('插入数据成功', data[1])
        except Exception as e:
            print('插入数据失败！！', e)
            db.rollback()


if __name__ == '__main__':
    path = 'C:/Users/86177/Desktop/clients.xlsx'
    # data = read_excel(path)
    # save_to_MYSQL(data)
    # data = read_excel_client(path)
    # save_to_MYSQL_client(data)
    # names = spilt_str([',', '，', '/', '.'], 'JINKING,杨小姐.苏小姐')
    # print('names', names)
    # names = spilt_str([',', '、', '，', '.'], '吴小姐.周先生')
    # print('names', names)
    # clients = name_to_array(names)
    # for c in clients:
    #     print('c', c)
    excute_names(path)