# 继承Funcs类，主要是拿到分机的状态
# 这个类决定了什么来电由哪个分机接
# 记录分机接电话的频率


class Call_to_seat(object):
    s = {}
    '''
    s = {
        '213': 1,
        '214': 0,
        '215': 1,
    }
    '''

    # 将Funcs中的空闲分机的变量更新到s中
    def __init__(self, online_seat):
        ds = Call_to_seat.s
        for os in online_seat:
            ds[os] = 0

    # 选择此次接电话的分机
    # 找到次数最小的值，如果都相等，从第一个开始
    @staticmethod
    def select_seat():
        ds = Call_to_seat.s
        r = min(ds.items(), key=lambda x: x[1])[0]
        return r

    # 有新的分机上线,将其加入s中
    def new_seat_online(self, new_seat):
        ds = Call_to_seat.s
        ds[new_seat] = 0

    # 来电转接分机，记录下分机的接电话的次数
    def update_number(self, seat):
        ds = Call_to_seat.s
        ns = ds[seat] + 1
        ds[seat] = ns
