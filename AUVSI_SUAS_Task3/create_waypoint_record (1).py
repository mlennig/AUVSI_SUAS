def create_waypoint_record(id_number, home_flag, command_id, lat, lng, alt):
    """
    TSV Record in the form of:
    id_number, home_flag, 0, command_id, 0, 0, 0, 0, lat, lng, alt, 1
    :param id_number: integer value/count representing the instruction order in mission planner
    :param home_flag: 1 represents a home position, 0 represents other
    :param command_id: integer value that corresponds to a specific mission planner command
    :param lat: Waypoint latitude
    :param lng: Waypoint longitude
    :param alt: Waypoint altitude
    """

    return (str(id_number) + "\t" +
            str(home_flag) + "\t" +
            "0\t" +
            str(command_id) + "\t" +
            "0\t0\t0\t0\t" +
            str(lat) + "\t" +
            str(lng) + "\t" +
            str(alt) + "\t" +
            "1")