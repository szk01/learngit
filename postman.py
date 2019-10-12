# import requests
#
# url = "http://180.175.33.122:8787"
#
# payload = "<?xml version=\"1.0\" encoding=\"utf-8\" ?>\n  <Control attribute=\"Query\">\n  <Deviceinfo/>\n  </Control>"
# headers = {
#     'content-type': "text/html",
#     'cache-control': "no-cache",
#     'postman-token': "63819baf-7cd0-48d7-ff43-f093805ccaf1"
#     }
#
# response = requests.request("POST", url, data=payload, headers=headers)
#
# print(response.text)


# import random
#
# def generate_code():
#     # 定义一个种子，从这里面随机拿出一个值，可以是字母
#     seeds = "1234567890"
#     # 定义一个空列表，每次循环，将拿到的值，加入列表
#     random_num = []
#     # choice函数：每次从seeds拿一个值，加入列表
#     for i in range(6):
#         random_num.append(random.choice(seeds))
#     # 将列表里的值，变成四位字符串
#     return "" . join(random_num)
#
# # 生成40组随机数
# if __name__ == '__main__':
#     for i in range(40):
#         p = generate_code()
#         print(p)

# 增删改查
'''
add 
    实例化一个ORM对象，加上各种参数client = Client(id=1, cid=2, number=123)
    
delete
    通过Model对象的方法，找到这个实例，然后删除

update
    通过Model对象的方法，找到这个实例，然后改变实例的变量
'''

# zip()和dict()的转变

k = ['k1', 'k2', 'k3', 'k4']
v = ['v1', 'v2', 'v3', 'v3', 'v4']

def zipToDict():
    zipped = zip(k, v)

    # for z in zipped:            # 由元祖组成的列表
    #     print('z', z)

    # listedZip = list(zipped)
    # print(listedZip)
    # for l in listedZip:
    #     print('l', l)

    # dictedZip =dict(zipped)
    # print('dictedZip', dictedZip)

zipToDict()