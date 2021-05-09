# Generate Waypoints File
# -----------------------
waypoint_file = "evidence_waypoint_file.txt"
f = open(waypoint_file, 'w')

# Home Position
print ("Home Position")
home = mission.__getattribute__("home_pos")         # GpsCoordinate Object
print (home, '\n')

# Mission Waypoints
mission_waypoints = mission.__getattribute__("mission_waypoints")   # List of Waypoint Objects
print ("Way Points")
print (mission_waypoints)
print ('\n')

# Write Points to File
f.write("QGC WPL 110\n")                                                             # Required for mission planner
f.write(create_waypoint_record(0, 1, 16, str(home.__getattribute__("latitude")),     # Home Position Waypoint
                               str(home.__getattribute__("longitude")),
                               str(HOME_START_HEIGHT)) + "\n")

count = 1
for i in mission_waypoints:
    entry = create_waypoint_record(count, 0, 16, str(i.__getattribute__("latitude")),   # Move Waypoint Location
                                   str(i.__getattribute__("longitude")),
                                   str(i.__getattribute__("altitude_msl") * METERS_IN_FOOT))
    count += 1
    f.write(entry+"\n")

# Close Waypoints File
f.close()