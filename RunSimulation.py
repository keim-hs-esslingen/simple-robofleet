# =============================================================================
# Created at the Esslingen University of Applied Sciences
# Department: Anwendungszentrum KEIM
# Contact: emanuel.reichsoellner@hs-esslingen.de
# Date: February 2021
# License: MIT License
# =============================================================================
# This Script sets the Simulation Parameters and starts the Simulation
# =============================================================================

from POI import POI
from Fleet import Vehicle, Fleet, ModeType
from RequestManager import Request, RequestManager
import time
import turtle

TIMESTEP_LENGTH = 0.01  # (in seconds)


def terminateSimulation(timeStep, fleet):
    print("All Requests were processed -> Simulation ist terminated!")

    allVehiclesTotalDistance = 0

    f = open("Results.txt", "w")
    f.write("Simulation was terminated at TimeStep " + str(timeStep) + "\n\n")
    for id in fleet.getVehicleIds():

        distance = fleet.vehicleDict.get(id).totalDistance
        f.write("Vehicle " + str(id) + ": " + "{:.1f}".format(distance) + " m\n")
        allVehiclesTotalDistance += distance
    f.write("\nTotal Distance " + "{:.1f}".format(allVehiclesTotalDistance) + " m\n")
    f.close()
    print("See the Results File: Results.txt")
    exit()


if __name__ == "__main__":
    # setup DrawingBoard
    drawingBoard = turtle.Screen()
    drawingBoard.title(
        "SimpleRoboFleet - a simple Simulation Environmet to test Routing Strategies and AI Techniques for Robo Taxi Fleets"
    )
    drawingBoard.bgcolor("black")
    drawingBoard.setup(width=1200, height=800)

    fleet = Fleet()
    requestManager = RequestManager(fleet)

    # Simulation Setting:

    # Points of Interest:
    poi1 = POI(-220, -350)
    poi2 = POI(-410, 200)
    poi3 = POI(180, -290)
    poi4 = POI(400, 310)
    poi5 = POI(100, 200)
    poi6 = POI(400, -230)
    poi7 = POI(300, 140)
    poi8 = POI(-500, 100)
    poi9 = POI(-300, -150)
    poi10 = POI(150, 50)
    poi11 = POI(-150, 100)
    poi12 = POI(10, -100)

    # Requests:
    # Example:submitTime = 7 , startPoi = poi1, targetPoi = poi3
    # Important: please don't use a certian submitTime for two Requests
    requestManager.addRequest(7, poi1, poi2)
    requestManager.addRequest(15, poi3, poi4)
    requestManager.addRequest(50, poi8, poi9)
    requestManager.addRequest(70, poi7, poi6)
    requestManager.addRequest(90, poi10, poi5)
    requestManager.addRequest(100, poi9, poi3)
    requestManager.addRequest(110, poi2, poi3)
    requestManager.addRequest(130, poi11, poi1)
    requestManager.addRequest(150, poi3, poi12)

    # Robotaxis:
    # Example: vehicleId = 1 , posx = -200, posy = -250
    fleet.addVehicle(1, -200, -250)
    fleet.addVehicle(2, -250, 200)
    fleet.addVehicle(3, 50, 300)
    fleet.addVehicle(4, 300, -200)
    fleet.addVehicle(5, 370, 50)

    # Perform the Simulation
    for timeStep in range(500):
        print("TimeStep:", timeStep)

        requestManager.step(timeStep)

        for vehicleId in fleet.getVehicleIds():

            vehicle = fleet.vehicleDict.get(vehicleId)
            if vehicle.step():
                if vehicle.requestMode == 2:
                    vehicle.resetRequest()
                    print("Vehicle ", vehicleId, " has dropped a passenger")
                    if requestManager.allRequestsProcessed():
                        allRequestsProcessed = True
                        for id in fleet.getVehicleIds():
                            if fleet.vehicleDict.get(id).requestMode != ModeType.free:
                                allRequestsProcessed = False
                                break
                        if allRequestsProcessed:
                            terminateSimulation(timeStep, fleet)

                if vehicle.requestMode == 1:
                    vehicle.passengerPickUp()
                    print("Vehicle ", vehicleId, " has picked up a passenger")

        time.sleep(TIMESTEP_LENGTH)
