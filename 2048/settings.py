
class Settings:
    def __init__(self):
        self.screen_width = 800
        self.screen_height = 800
        self.bg_color = (187, 173, 160)

        self.grid_size = 4
        #mã màu cho các số
        self.number_color = {0: (236, 203, 98),
                             2: (238, 228, 218),
                             4: (237, 224, 200),
                             8: (242, 177, 121),
                             16: (245, 149, 99),
                             32: (247, 134, 97),
                             64: (247, 94, 60),
                             128: (239, 204, 112),
                             256: (234, 203, 97),
                             512: (239, 198, 80),
                             1024: (245, 231, 184),
                             2048: (249, 238, 172),
                             4096: (255, 59, 62)}

        self._victory_point = 2048