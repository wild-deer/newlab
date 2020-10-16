class LightTime(object):
    #获取车辆数并进行决策返回红绿灯秒数
    def __init__(self, mw):
        self.mw = mw  # 传入UI界面对象
        #初始化红绿灯秒数
        self.std_light_seconds = 20
        self.max_light_seconds = 30
        self.min_light_seconds = 10

        self.cur_color_x = "red"
        self.cur_seconds_x_red = 10
        self.cur_seconds_x_green = 10

        self.total_car_x = 0
        self.total_car_y = 0

    def set_total_car(self,car_count_x,car_count_y):
        #print("car_count_x:",car_count_x,"car_count_y:",car_count_y)
        self.total_car_x = car_count_x
        self.total_car_y = car_count_y
        if self.total_car_x > self.total_car_y:
            self.cur_seconds_x_red -= self.std_light_seconds *0.2
            if self.cur_seconds_x_red < self.min_light_seconds:
                self.cur_seconds_x_red = self.min_light_seconds

            self.cur_seconds_x_green += self.std_light_seconds * 0.2
            if self.cur_seconds_x_green > self.max_light_seconds:
                self.cur_seconds_x_green = self.max_light_seconds
        else:
            self.cur_seconds_x_red += self.std_light_seconds * 0.2
            if self.cur_seconds_x_red > self.max_light_seconds:
                self.cur_seconds_x_red = self.max_light_seconds

            self.cur_seconds_x_green -= self.std_light_seconds * 0.2
            if self.cur_seconds_x_green < self.min_light_seconds:
                self.cur_seconds_x_green = self.min_light_seconds


    '''def loop_light(self):  #红绿灯切换
        while True:
            self.control_light(self.cur_color_x)
            if self.cur_color_x == "red":
                time.sleep(self.cur_seconds_x_red)
            else:
                time.sleep(self.cur_seconds_x_green)

            if self.cur_color_x == "red":
                self.cur_color_x = "green"
            else:
                self.cur_color_x = "red"
                splash_time =3.0
                while splash_time >=0:
                    self.control_light("yellow")
                    time.sleep(0.6)
                    splash_time -= 0.6
                    self.control_light("off")

    def control_light(self,color):  #控制 外设红绿灯
        PARAMS = {'color': color}
        r = requests.post(url = URL , data=PARAMS)
        data = r.json()
    '''