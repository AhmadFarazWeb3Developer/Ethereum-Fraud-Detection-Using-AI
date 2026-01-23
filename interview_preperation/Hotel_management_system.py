class Room:
    def __init__(self,id,resident_name):
        self.id = id
        self.occupied = True
        self.resident_name = resident_name
        
class Hotel:
    def __init__(self):
        self.rooms = {}
        
    def add_room(self, roomId, room):
        existing_room = self.rooms.get(roomId)
        if existing_room and existing_room.occupied:
            print(f"Room {roomId} is already occupied by {existing_room.resident_name}. Cannot allot.")
        else:
            self.rooms[roomId] = room

    def display_rooms(self):
        if not self.rooms:
            print("No rooms have been allotted yet.")
            return
        
        for roomId, room in self.rooms.items():
            status = "Occupied" if room.occupied else "Vacant"
            print("Room Details:")
            print("----------------")
            print(f"Hotel Room ID: {roomId}")
            print(f"Resident Name: {room.resident_name}")
            print(f"Status: {status}")
            
    def check_room_availability(self, roomId):
        room = self.rooms.get(roomId)
        return room.occupied
       
    
    def check_out_room(self,roomId):
        room= self.rooms.get(roomId)
        if room and room.occupied:
            room.occupied = False
            print(f"Room {roomId} has been checked out.")
        else:
            print(f"Room {roomId} is either not found or already vacant.")
            
    def check_rooms_capacity(self):
         total = len( self.rooms)       
         occupied=sum(1 for room in self.rooms.values() if room.occupied) # 1 count for each occupied room
         vacant= total - occupied
         print("Total Rooms:", total)
         print("Occupied Rooms:", occupied)
         print("Vacant Rooms:", vacant)


def Menu():
    print ("\nWelcome to the Hotel Management System")
    print ("--------------------------------------")
    print ("1). Do you want to allot a room?")
    print ("2). Do you want to display room details?")
    print ("3). Check room availability?")
    print ("4). Check room capacity?")
    print ("5). Check out from room?")
    print ("6). Do you want to close the hotel?")
    print ("--------------------------------------")



hotel = Hotel()


while True:
    Menu()
    operation= input('Enter Operration number 1, 2, 3, 4, 5, or 6 to proceed : ')

    if operation == '1':
        roomId = input("Enter Room ID: ")
        resident_name = input("Enter Resident Name: ")
        room = Room(roomId, resident_name)
        hotel.add_room(roomId, room)
        print(f"Room {roomId} has been allotted to {resident_name}.")

    elif operation == '2':    
        hotel.display_rooms()

    elif operation == '3':
        print("Closing the hotel management system. Goodbye!")
        break
    elif operation == '4':
        hotel.check_rooms_capacity()
        
    elif operation == '5':
        roomId = input("Enter Room ID to check out: ")
        hotel.check_out_room(roomId)    
        
    elif operation == '6':
        print("Closing the hotel management system. Goodbye!")
        break    

    else:
        print("Invalid operation number. Please enter 1, 2, 3, 4, 5, or 6.")







            
        
        