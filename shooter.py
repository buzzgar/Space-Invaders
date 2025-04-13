import stddraw
import math
#assumes a scale of -1,1 for both x and y
class Shooter:
    def __init__(self,scaleFactor = 0.1,playerFile = 'player1.txt'):
        self._shooter = self._getShooterShape(playerFile)
        self._width = 2*scaleFactor
        self._heigth = 2*scaleFactor
        self._pixelHeight = self._width/len(self._shooter)
        self._pixelWidth = self._heigth/len(self._shooter[0])
        self._x = -scaleFactor
        self._y = -0.9
        self._speed = 0.08
        self._angle = 0
       

    def move(self, direction):
        if direction.lower() == 'a':
            self._moveLeft()
        else:
            self._moveRight()

    def _moveLeft(self):
        if self._x - (self._width / 2) <= -1:
            self._x = -1 
        else:
            self._x -= self._speed

    def _moveRight(self):
        if self._x + (self._width/2) >= 0.8:
            self._x = 1 - self._width
        else:
            self._x += self._speed
    

    def rotate(self, angle):
        if angle < 0:
            self._clockwise(angle)
        else:
            self._anticlockwise(angle)

    def _anticlockwise(self,angle):
        new_angle = self._angle + math.radians(angle)
        if new_angle > math.radians(45):
            self._angle = math.radians(45)
        else:
            self._angle = new_angle


    def _clockwise(self,angle):
        new_angle = self._angle + math.radians(angle)
        if new_angle < math.radians(-45):
            self._angle = math.radians(-45)
        else:
            self._angle = new_angle
        

    def _rotatePoints(self, x, y, cx, cy, angle):
        x -= cx
        y -= cy
        xRotated = x * math.cos(angle) - y * math.sin(angle)
        yRotated = x * math.sin(angle) + y * math.cos(angle)
        return xRotated + cx, yRotated + cy

    def _draw(self):
        stddraw.clear(stddraw.GRAY)  # Moved here
        for i in range(len(self._shooter)):
            for j in range(len(self._shooter[0])):
                if self._shooter[i][j] != 0:
                    x = self._x + j * self._pixelWidth
                    y = self._y + (len(self._shooter) - i - 1) * self._pixelHeight

                    Xcorners = [x, x + self._pixelWidth, x + self._pixelWidth, x]
                    Ycorners = [y, y, y + self._pixelHeight, y + self._pixelHeight]

                    rotatedXconners = []
                    rotatedYconners = []
                    centerX = self._x + self._width / 2
                    centerY = self._y + self._heigth / 2
                    for k in range(4):
                        rx, ry = self._rotatePoints(Xcorners[k], Ycorners[k], centerX, centerY, self._angle)
                        rotatedXconners.append(rx)
                        rotatedYconners.append(ry)

                    if self._shooter[i][j] == 2:
                        stddraw.setPenColor(stddraw.RED)
                    else:
                        stddraw.setPenColor(stddraw.BOOK_BLUE)
                    stddraw.filledPolygon(rotatedXconners, rotatedYconners)
        
    def _getShooterShape(self,file_path):
        shapeMatrix = []
        with open(file_path, 'r') as file:
            for line in file:
                row = [int(x) for x in line.strip().split(',')]
                shapeMatrix.append(row)
        return shapeMatrix

    def drawShooter(self):
        self._draw()


    