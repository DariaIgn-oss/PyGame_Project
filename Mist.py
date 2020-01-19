from technical_function import load_image
from settings import mist_sprite
from Object import Object

class Mist(Object):
    mist_image = [load_image(f'mist{i}.png') for i in range(1, 9)]
    index = 0

    def __init__(self):
        super().__init__(0, 0, Mist.mist_image[Mist.index], mist_sprite)

    def update(self):
        Mist.index += 1
        if Mist.index == 63:
            Mist.index = 0
        else:
            self.image = Mist.mist_image[Mist.index // 8]