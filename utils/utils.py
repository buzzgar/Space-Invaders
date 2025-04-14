import stdaudio


class GameObject:

    def __init__(self, name, x, y, width, height, color):
        self.x = x
        self.y = y
        self.name = name

        self.width = width
        self.height = height

        self.color = color

        self.is_alive = False
        self.is_destroyed = False

        self.allow_draw = False

    def draw(self):
        if self.allow_draw:
            self._draw()

    def _draw(self):
        pass

class Music:
    def __init__(self, file):
        self.filename = file

    def play_audio(self):
        stdaudio.playFile(self.filename)

def collides(entity1: GameObject, entity2: GameObject) -> bool:

    e1_x = entity1.x - entity1.width//2
    e1_y = entity1.y - entity1.height//2

    e2_x = entity2.x - entity2.width//2
    e2_y = entity2.y - entity2.height//2

    return (
            e1_x + entity1.width > e2_x and
            e1_x < e2_x + entity2.width and
            e1_y + entity1.height > e2_y and
            e1_y < e2_y + entity2.height
    )

