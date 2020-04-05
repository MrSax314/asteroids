class obj():

    def __init__(self):
        self.posX = 0
        self.posY = 0
        self.velX = 0
        self.velY = 0
        self.state = 0
        self.direction = 0

    def __init__(self, x, y, vx, vy):
        self.posX = x
        self.posY = y
        self.velX = vx
        self.velY = vy
        self.state = 0
        self.direction = 0

    # Set functions
    def get_px(self):
        return self.posX

    def get_py(self):
        return self.posY

    def get_vx(self):
        return self.velX

    def get_vy(self):
        return self.velY

    def get_state(self):
        return self.state

    def get_direction(self):
        return self.direction

    # Get functions
    def set_px(self, pos):
        self.posX = pos

    def set_py(self, pos):
        self.posY = pos

    def set_vx(self, vel):
        self.velX = vel

    def set_vy(self, vel):
        self.velY = vel

    def set_pos(self, posx, posy):
        self.posX = posx
        self.posY = posy

    def set_vel(self, velx, vely):
        self.velX = velx
        self.velY = vely

    def set_state(self, state):
        self.state = state

    def set_direction(self, direction):
        self.direction = direction

    def stop(self):
        self.velX = 0
        self.velY = 0

    def debug(self):
        print(self.get_vx(), "  ", self.get_vy(), "   ", self.get_direction())

    def debug1(self):
        print(self.get_vx(), "  ", self.get_vy(), "   ", self.get_state())

    def copy(self, copy):
        self.posX = copy.posX
        self.posY = copy.posY
        self.velX = copy.velX
        self.velY = copy.velY

'''     
    def set_vx(self,i):
        for num in range(i):
            self.vel = [self.speed, 0]

    def set_vy(self,i):
        for num in range(i):
            self.vel = [0, self.speed]
'''
