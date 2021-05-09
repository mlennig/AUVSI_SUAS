from create_waypoint_record import create_waypoint_record

# Generate Waypoints File
# -----------------------

def makeWaypointFile(waypoints, coordList):
    waypoint_file = "evidenceID_waypoint_file.txt"
    f = open(waypoint_file, 'w')
    HOME_START_HEIGHT = 57.869999
    lat = 0
    lon = 1
    ALTITUDE_IN_FEET = 50
    
    # Write Points to File
    # Required for mission planner
    f.write("QGC WPL 110\n")     
    
    # Home Position Waypoint
    f.write(create_waypoint_record(0, 1, 16, str(coordList[0][lat]), str(coordList[0][lon]), str(HOME_START_HEIGHT)) + "\n")
    
    # Make Waypoint Locations
    count = 1
    for i in range(len(waypoints)):
        entry = create_waypoint_record(count, 0, 16, str(waypoints[i][lat]), str(waypoints[i][lon]), str(ALTITUDE_IN_FEET))
        count += 1
        f.write(entry+"\n")
    
    # Close Waypoints File
    f.close()