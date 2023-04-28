def get_seat_chart():
    with open('reservations.txt', 'r') as seat_file:
        # create bus array
        bus = []
        for x in range(1, 13):
            # print(x)
            bus_row = ['O', 'O', 'O', 'O']
            bus.append(bus_row)

        # change reserved seats
        line = seat_file.readline()
        while line:
            line = line.strip() # remove newline character at end of the line
            line = line.split(', ') # split string to get data
            # assign data to variables
            name = line[0]
            row = int(line[1])
            seat = int(line[2])
            ticket_num = line[3]
            # change the bus array
            bus[row][seat] = 'X'

            line = seat_file.readline()

        # return seat chart
        return bus

def get_ticket(first_name):
    # define second string
    class_name = "INFOTC4320"
    # find string lengths
    name_length = int(len(first_name))
    class_name_length = int(len(class_name))
    # find longer and shorter strings
    if name_length > class_name_length:
        shorter_string = class_name
        longer_string = first_name
    else:
        shorter_string = first_name
        longer_string = class_name

    # create empty list
    ticket_list = []

    # start count
    count = 0

    # add alternating characters until end of shorter string
    for x in range(0, int(len(shorter_string))):
        ticket_list.append(first_name[count])
        ticket_list.append(class_name[count])
        count+=1

    # add rest of longer string
    for x in range(count, int(len(longer_string))):
        if longer_string == class_name:
            ticket_list.append(class_name[count])
            count+=1
        if longer_string == first_name:
            ticket_list.append(first_name[count])
            count+=1
    
    # make list into string
    ticket = ''.join(ticket_list)

    # return final string
    return ticket