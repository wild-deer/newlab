import random


def led_control(car1, car2, car3, car4, state):
    # 四种不同的状态并且传入之前的状态state
    #  state= 1   路口1、3绿灯，路口2、4红灯
    # state= 2 路口2、4绿灯，路口1、3红灯
    # state= 3 状态1变为状态2
    # state= 4 状态2变为状态1

    if (car1 + car3) > (car2 + car4):  # 如果state = 1
        if state == 2:  # 如果之前的状态是state = 2
            state = 4  # 此时state = 4
            return state
        state = 1
        return state
    if (car1 + car3) < (car2 + car4):  # 如果state = 2

        if state == 1:  # 如果之前的状态是state = 1
            state = 3  # 此时state = 3
            return state
        state = 2  # 否则此时state = 2
        return state
if __name__ == '__main__':
    state = 0
    while 1:
        print("请输入state")
        i = input()

        state = int(i)
        car1 = random.randint(0, 50)
        car2 = random.randint(0, 50)
        car3 = random.randint(0, 50)
        car4 = random.randint(0, 50)
        state = led_control(car1,car2,car3,car4,state)
        print("car1 + car3 =" + str(car1 + car3))
        print("car2 + car4 =" + str(car2 + car4))
        print(state)