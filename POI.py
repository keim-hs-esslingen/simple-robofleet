# =============================================================================
# Created at the Esslingen University of Applied Sciences
# Department: Anwendungszentrum KEIM
# Contact: emanuel.reichsoellner@hs-esslingen.de
# Date: February 2021
# License: MIT License
# =============================================================================
# This Script provides the class Point of Interest
# =============================================================================

import math
import turtle


class POI:
    def __init__(self, xPos, yPos):
        self.xPos = xPos
        self.yPos = yPos
        self.drawingEntity = turtle.Turtle()
        self.drawingEntity.shape("square")
        self.drawingEntity.color("yellow")
        self.drawingEntity.turtlesize(1.5)
        self.drawingEntity.penup()  # we use penup() that no lines are drawn with the goto command
        self.drawingEntity.goto(xPos, yPos)
