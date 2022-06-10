import numpy as np
import random

class Strategy:
    def __init__(self):
        self.arena = np.zeros((0, 0))
        self.my_url = None
        self.my_coor = (0, 0)
        self.my_direction = None
        self.face_border_list = None
        
    def get_my_url(self, request):
        self.my_url = request['_links']['self']['href']
    
    def get_arena_size(self, request):
        height, weight = request['arena']['dims']
        self.arena = np.zeros((height, weight))
        self.face_border_list = zip([0, 0, height-1, weight-1], ['N', 'W', 'S', 'E'])
    
    def draw_map(self, request):
        usr_loc = self.arena.copy()
        danger_zone = self.arena.copy()
        makrov_map = self.arena.copy() * 0.
        for url, info in request['arena']['state'].items():
            y, x, direction, is_hit, score = info.values()
            if url == me_url:
                self.my_coor = (y, x)
                self.my_direction = direction
                self.face_border = self.is_face_boreder()
                usr_loc[y, x] = 1
                continue
            usr_loc[y, x] = 1

            if direction == 'N':
                fire_range = max(0, y-3)
                danger_zone[fire_range: y, x] = 1
            elif direction == 'S':
                fire_range = y+3
                danger_zone[y: fire_range, x] = 1
            elif direction == 'W':
                fire_range = max(0, x-3)
                danger_zone[y, fire_range: x] = 1
            elif direction == 'E':
                fire_range = x+3
                danger_zone[y, x: fire_range] = 1
        return usr_loc, danger_zone

    def is_face_boreder(self):
        for status in list(zip(self.my_coor, self.my_direction*2)):
            if status in self.face_border_list:
                return True
        return False
    
    def target_in_fire_range(self, usr_loc):
        x, y = self.my_coor
        print(y, x, self.my_direction)
        if self.my_direction == 'N':
            fire_range = max(0, y-3)
            target_in_range = usr_loc[fire_range: y, x]
        elif self.my_direction == 'S':
            fire_range = y+3
            target_in_range = usr_loc[y: fire_range, x]
        elif self.my_direction == 'W':
            fire_range = max(0, x-3)
            target_in_range = usr_loc[y, fire_range: x]
        elif self.my_direction == 'E':
            fire_range = x+3
            target_in_range = usr_loc[y, x: fire_range]
        print(sum(target_in_range))
        return sum(target_in_range)

    def escape(self):
        if self.face_border:
            return random.choice(['R', 'L'])
        return 'F'
    
    def prepare(self):
        pass
    
    def fire(self):
        return 'T'
    
    def action(self):
        pass
    
    def next_step(self, request):
        self.get_arena_size(request)
        self.get_my_url(request)
        usr_loc, danger_zone = self.draw_map(request)
        if danger_zone[self.my_coor]:
            return self.escape()
        
        elif self.target_in_fire_range(usr_loc) > 0:
            return 'T'
        elif self.face_border:
            return random.choice(['R', 'L'])
        else:
            return random.choice(['F', 'R', 'L'])
