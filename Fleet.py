# =============================================================================
# Created at the Esslingen University of Applied Sciences
# Department: Anwendungszentrum KEIM
# Contact: emanuel.reichsoellner@hs-esslingen.de
# Date: February 2021
# License: MIT License
# =============================================================================
# This Script provides classes to manage the Robo Taxi Fleet
# =============================================================================

import math
import turtle
from enum import IntEnum
from RequestManager import Request

PIXELS_PER_STEP = 10  # we go 10 pixels per step by default


class ModeType(IntEnum):
    free = 0  # green
    to_passenger = 1  # blue
    with_passenger = 2  # red


class Vehicle:
    def __init__(self, initialX, initialY):
        self.passengerList = []

        self.targetX = initialX
        self.targetY = initialY
        self.requestMode = ModeType(0)

        self.stepLength = PIXELS_PER_STEP
        self.drawingEntity = turtle.Turtle()
        self.totalDistance = 0
        self.setMode(0)
        self.request = None
        self.drawingEntity.shape("triangle")
        self.drawingEntity.turtlesize(1.5)
        self.drawingEntity.penup()  # we use penup() that no lines are drawn with the goto command
        self.drawingEntity.goto(initialX, initialY)

    def addDistance(self, targetPoi):
        self.totalDistance += math.sqrt(
            (targetPoi.xPos - self.drawingEntity.xcor()) ** 2
            + (targetPoi.yPos - self.drawingEntity.ycor()) ** 2
        )

    def addPassenger(self, passenger):
        self.passengerList.append(passenger)

    def setRequest(self, request):
        self.request = request
        self.setMode(1)
        self.setTargetPoi(request.startPoi)

    def passengerPickUp(self):
        self.setTargetPoi(self.request.targetPoi)
        self.setMode(2)

    def resetRequest(self):
        self.request.passenger.drawingEntity.color("yellow")
        self.request = None
        self.setMode(0)

    def setMode(self, requestMode):
        self.requestMode = ModeType(requestMode)
        if requestMode == ModeType.free:
            self.drawingEntity.color("green")
        if requestMode == ModeType.to_passenger:
            self.drawingEntity.color("blue")
        if requestMode == ModeType.with_passenger:
            self.drawingEntity.color("red")

    def setTargetPoi(self, poi):
        self.addDistance(poi)
        self.targetX = poi.xPos
        self.targetY = poi.yPos

    def step(self):
        xDiff = self.targetX - self.drawingEntity.xcor()
        yDiff = self.targetY - self.drawingEntity.ycor()

        if xDiff != 0:
            angle = math.atan(yDiff / xDiff)
            if xDiff < 0:
                angle = math.pi + angle
        else:
            if yDiff > 0:
                angle = math.pi / 2
            else:
                angle = -math.pi / 2

        if xDiff ** 2 + yDiff ** 2 < self.stepLength ** 2:
            self.drawingEntity.goto(self.targetX, self.targetY)
            pcounter = 0
            for passenger in self.passengerList:
                if passenger:
                    passenger.drawingEntity.goto(
                        self.targetX, self.targetY + pcounter * 15
                    )
                    pcounter += 1
            # True means that the Target is reached
            return True
        else:
            newX = self.drawingEntity.xcor() + self.stepLength * math.cos(angle)
            newY = self.drawingEntity.ycor() + self.stepLength * math.sin(angle)

            self.drawingEntity.goto(newX, newY)

            if self.requestMode == ModeType.with_passenger:
                self.request.passenger.drawingEntity.goto(newX, newY)

            # False means that the Target is not reached yet
            return False


class Fleet:
    def __init__(self):
        self.vehicleDict = {}

    def addVehicle(self, id, initialX, initialY):
        self.vehicleDict[id] = Vehicle(initialX, initialY)

    def getVehicle(self, id):
        return self.vehicleDict.get(id)

    def getVehicleList(self):
        return self.vehicleDict.values()

    def getVehicleIds(self):
        return self.vehicleDict.keys()

    def getClosestVehicle(self, poi):
        x = poi.xPos
        y = poi.xPos
        closestVehicleId = 0
        minDist = 1000
        # find the closest available Robo Taxi
        for vehicleId in self.vehicleDict.keys():
            if self.vehicleDict.get(vehicleId).requestMode == 0:
                dist = math.sqrt(
                    (x - self.vehicleDict.get(vehicleId).drawingEntity.xcor()) ** 2
                    + (y - self.vehicleDict.get(vehicleId).drawingEntity.ycor()) ** 2
                )
                print("vehicle ", vehicleId, "dist:", dist)
                if dist < minDist:
                    minDist = dist
                    closestVehicleId = vehicleId
        return closestVehicleId
