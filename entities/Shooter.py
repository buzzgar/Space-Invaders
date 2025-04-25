################################################
# Student Name: Samkelo Nkabinde
# Student Number: 28118944
################################################

import time
import stddraw
import math
from utils.PictureLoader import Picture
import GameSettings
from utils.utils import GameObject

#assumes a scale of -1,1 for both x and y
class Shooter(GameObject):
    def __init__(self, name, x, y, width, height, color, scaleFactor = 0.1, playerFile = 'Player1.png'):
        self._shooter = self._getShooterShape(playerFile)
        self._width = 2*scaleFactor
        self._height = 2*scaleFactor

        super().__init__(name, x, y, self._width, self._height)

        self.screen_width = width
        self.screen_height = height

        self._pixelHeight = self._width/len(self._shooter)
        self._pixelWidth = self._height/len(self._shooter[0])

        self._x = self.screen_width//2
        self._y = 0.9 * self.screen_height

        self.x = self._x + self.get_width() / 2
        self.y = self._y + self.get_height() / 2

        self._speed = GameSettings.player_speed
        self._delta_angle = GameSettings.player_angle_change

        self._angle = 0
        self.allow_draw = True
        
    # Getters for private instances
    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_width(self):
        return self._width

    def get_height(self):
        return self._height

    def get_angle(self):
        return self._angle

    # Motion methods
    def moveLeft(self):
        # Moves shooter left and ensures it does not move beyond boundary 
        if self._x - (self._width / 2) <= 0:
            self._x = 0
        else:
            self._x -= self._speed

        self.x = self._x + self.get_width() / 2
        self.y = self._y + self.get_height() / 2

    def moveRight(self):
         # Moves shooter right and ensures it does not move beyond boundary 
        if self._x + (self._width) < self.screen_width:
            self._x += self._speed
        if self._x + (self._width) >= self.screen_width:
            self._x -= self._speed


        self.x = self._x + self.get_width() / 2
        self.y = self._y + self.get_height() / 2
        
    # Rotation Methods
    def anticlockwise(self):
        # Rotate shoter anti-clockwise and ensures it stays within the horizon
        angle = self._delta_angle
        new_angle = self._angle + math.radians(angle)
        if new_angle > math.radians(90):
            self._angle = math.radians(90)
        else:
            self._angle = new_angle

    def clockwise(self):
        # Rotate shoter clockwise and ensures it stays within the horizon
        angle = -self._delta_angle
        new_angle = self._angle + math.radians(angle)
        if new_angle < math.radians(-90):
            self._angle = math.radians(-90)
        else:
            self._angle = new_angle
        
    # Other Methods
    def _rotatePoints(self, x, y, cx, cy, angle):
         # Rotates the point (x, y) around the center point (cx, cy) by the given angle (in radians).
        x -= cx
        y -= cy
        xRotated = x * math.cos(angle) - y * math.sin(angle)
        yRotated = x * math.sin(angle) + y * math.cos(angle)
        return xRotated + cx, yRotated + cy

    def _renderShooter(self):
        # Renders the shooter by drawing a filled, rotated polygon for each non-black pixel in the shooter matrix.
        # Each pixel is treated as a rectangle (polygon) positioned based on its row and column, then rotated
        # around the center of the shooter before being drawn with its original color.
        
        for i in range(len(self._shooter)):
            for j in range(len(self._shooter[0])):
                color = self._shooter[i][j]
                if (color.getRed(),color.getGreen(),color.getBlue()) != (0,0,0):
                    x = self._x + j * self._pixelWidth
                    y = self._y + (len(self._shooter) - i - 1) * self._pixelHeight
                
                    Xcorners = [x, x + self._pixelWidth, x + self._pixelWidth, x]
                    Ycorners = [y, y, y + self._pixelHeight, y + self._pixelHeight]
                    rotatedXcorners = []
                    rotatedYcorners = []
                    centerX = self._x + self._width / 2
                    centerY = self._y + self._height / 2
                    
                    for k in range(4):
                        rx, ry = self._rotatePoints(Xcorners[k], Ycorners[k], centerX, centerY, self._angle)
                        rotatedXcorners.append(rx)
                        rotatedYcorners.append(ry)
                    stddraw.setPenColor(color)
                    stddraw.filledPolygon(rotatedXcorners, rotatedYcorners)

    
    def _getShooterShape(self,filePath):
        # Loads a PNG image from the given file path and converts it into a 2D matrix of color values
        pic = Picture(filePath)
        picMatrix = [[None] * pic.width()  for i in range(pic.height())]
        for i in range(pic.height()):
            for j in range(pic.width()):
                color = pic.get(j,i)
                picMatrix[i][j] = color
        return picMatrix
        
    def drawShooter(self):
        # Draws the shooter on the screen
        self._renderShooter()


    

    
