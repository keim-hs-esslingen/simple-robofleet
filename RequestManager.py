# =============================================================================
# Created at the Esslingen University of Applied Sciences
# Department: Anwendungszentrum KEIM
# Contact: emanuel.reichsoellner@hs-esslingen.de
# Date: February 2021
# License: MIT License
# =============================================================================
# This Script provides classes to manage the Requests
# =============================================================================


import math
import turtle


class Passenger:
    def __init__(self, initialX, initialY):
        self.drawingEntity = turtle.Turtle()
        self.drawingEntity.shape("circle")
        self.drawingEntity.color("yellow")
        self.drawingEntity.turtlesize(0.5)
        self.drawingEntity.penup()  # we use penup() that no lines are drawn with the goto command
        self.drawingEntity.goto(initialX, initialY)


class Request:
    def __init__(self, startPoi, targetPoi):
        self.startPoi = startPoi
        self.targetPoi = targetPoi
        self.passenger = Passenger(startPoi.xPos, startPoi.yPos)


class RequestManager:
    def __init__(self, fleet):
        self.Requests = {}
        self.fleet = fleet
        self.submittedRequests = []

    def addRequest(self, submitTime, startPoi, targetPoi):
        # the submitTime is also the Request Id
        self.Requests[submitTime] = Request(startPoi, targetPoi)

    def getRequest(self, submitTime):
        currentRequest = self.Requests.get(submitTime)
        if currentRequest:
            self.addToBuffer(currentRequest)
            del self.Requests[submitTime]
        if len(self.submittedRequests) > 0:
            return self.submittedRequests[-1]
        else:
            return None

    def addToBuffer(self, request):
        self.submittedRequests.append(request)

    def step(self, timeStep):
        request = self.getRequest(timeStep)
        if request:
            startPoi = request.startPoi
            request.passenger.drawingEntity.color("cyan")
            print("New Request was submitted!")
            closestVehicleId = self.fleet.getClosestVehicle(startPoi)

            if closestVehicleId != 0:
                assignedVehicle = self.fleet.getVehicle(closestVehicleId)
                assignedVehicle.setRequest(request)
                del self.submittedRequests[-1]
            else:
                print("No vehicle available for submitted Request!")

    def allRequestsProcessed(self):
        if len(self.Requests) == 0 and len(self.submittedRequests) == 0:
            return True
        else:
            return False
