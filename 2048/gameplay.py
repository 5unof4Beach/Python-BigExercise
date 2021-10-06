import numpy
import random
from settings import Settings


class Gameplay():
    def __init__(self):
        self.settings = Settings()
        # Tạo một ma trận với kích cỡ cho trước trong settings
        self.grid = numpy.zeros((self.settings.grid_size,
                                 self.settings.grid_size),
                                 dtype= int )
        # print(self.grid)

    def next_number(self,k=1):
        #lấy tất cả các vị trí có gía trị = 0 trong ma trận
        unoccupied_pos = list( zip(*numpy.where(self.grid == 0)))

        # lấy ngẫu nhiên 2 vị trí trong list các vị trí = 0
        for pos in random.sample(unoccupied_pos,k):
            if random.random() < .1 :
                self.grid[pos] = 4
            else:
                self.grid[pos] = 2

    def move_event(self,key):
        for i in range(self.settings.grid_size):
            if key in 'lr': # nếu nhập vào là l hoặc r thì lấy hàng
                this_row = self.grid[i,:]
            else:
                this_row = self.grid[:, i] # u hoăc d thì lấy cột

            flipped = False
            if key in 'rd': #nếu là r hoặc d thì lật ngược list để có thể tận dụng hàm get num
                flipped = True
                this_row = this_row[::-1]

            this_n = self._get_num(this_row) # list những số != 0 trong hàng
            # print(this_n)
            new_this_row = numpy.zeros_like(this_row) # tạo một hàng mới chỉ chứa số 0 có kích cỡ giống hàng cũ
            new_this_row[:len(this_n)] = this_n # gắn các giá trị != 0 vào mảng mới

            if flipped:
                new_this_row = new_this_row[::-1]

            if key in 'lr':
                self.grid[i, :] = new_this_row
            else:
                self.grid[:, i] = new_this_row

    def run(self,key):
        self.next_number(k = 2)
        while True:
            print(self.grid)
            key = input()
            if key == 'q':
                break
            previous_grid = self.grid.copy()
            self.move_event(key)
            if( all( (self.grid.flatten() == previous_grid.flatten()) )):
                continue
            self.next_number()

#hàm kiểm tra sau khi bấm nút có thay đổi j ko
    def isTheSame(self,previous_grid):
        if (all((self.grid.flatten() == previous_grid.flatten()))):
            return True

    @staticmethod
    def _get_num(row):
        this_n = row[row != 0]
        res = []
        skip = False
        for i in range(len(this_n)):
            if skip:
                skip = False
                continue
            if i != len(this_n) - 1 and this_n[i] == this_n[i+1]: #nếu 2 số liền nhau mà giống nhau thì cộng lại và cho vào mảng mới
                sum = this_n[i] * 2
                res.append(sum)
                skip = True
            else:
                res.append(this_n[i])
        return res

    def __str__(self):
        return str(self.grid)
    # @staticmethod
    def getGrid(self):
        return self.grid.copy()

# test = Gameplay()
# test.next_number(k = 2)
# test.run()

