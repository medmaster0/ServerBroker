import socket
from thread import *
import sys
import re

server = "localhost"
port = 5555

#SERVER (BROKER) DATA
players = {} #dict of the players connected
# playerId : player dict object (see below)
newCres = {} #dict of the animals walking around
# newCreId : newCre dict object (see below)

#WORLD DATA
num_x_layers = 50
num_y_layers = 30
num_z_layers = 20
world_tiles = [] #3D array for storing tile indices of the world
				#ACCESS:  world_tiles[x][y][z] = tile_index

#Players are dict objects that store user profile....
# Player = {
#	"name" : "Jugga" #name
# 	"pos" : (x,y,z) #tuple, map coords
# 	"lvls" : [] #array of skill lvls
# 				#SKILLS LIST
# 				# 0 - PAINTING
# 				# 1 - CURTAIN_FIX
# 				# 2 - CANDLE_LIGHTING
# 				# 3 - DOOR_MANSHIP
# 				# 4 - HAIR_BRUSH
# 				# 5 - SWEEPING
# 				# 6 - DUSTING
# 				# 7 - PERFUMING
# 	"crePrim" : (r,g,b) #color of creature
# 	"clothesIndex" : int #index of clothes type
# 	"clothesPrim" : (r,g,b) #color of clothes
# 	"clothesSeco" : (r,g,b) #color of clothes
# 	"clothesTert" : (r,g,b) #color of clothes
# 	"clothesQuad" : (r,g,b) #color of clothes
# }

#New Cres are dict objects that store npc animal information....
# NewCre = {
#	"name" : "fox #name
# 	"pos" : (x,y,z) #tuple, map coords
#	"newCreIndex" : determines which newCre it is exactly
# 	"crePrim" : (r,g,b) #color of creature
# }

##BEGIN SERVER INITIALIZATIONS
#############################

#Make some newCres
# for i in range(5):
# 	temp_cre = {
# 	"name" : "fox",
# 	"pos"  : (randi)
# 	}


##FUNCTION DEF
def threaded_client(conn, player_id):
	#Initial Message
	conn.send("hi from serve")

	isRegistered = False #keeps track of if we made a dictionary and registered it

	#Loop For Duration of Server-Client Communication
	while True:
		try:
			data = conn.recv(2*2048).decode('utf-8')
			#data = conn.recv(2048)
			print("This is the data:" + str(data))

			if not data:
				print("disconnected")
				break
			else:
				print("We recieved some data")

			#Parse and Process Data Here

			#concerning PLAYER REGISTRATION
			if "REGISTER" in data:
				print("got register message")
				#make dummy dict
				temp_player = {
					"name" : "XXXX", #name
					"pos" : (9999,9999,9999), #tuple, map coords
					"lvls" : [0,0,0,0,0,0,0,0], #array of skill lvls
								#SKILLS LIST
								# 0 - PAINTING
								# 1 - CURTAIN_FIX
								# 2 - CANDLE_LIGHTING
								# 3 - DOOR_MANSHIP
								# 4 - HAIR_BRUSH
								# 5 - SWEEPING
								# 6 - DUSTING
								# 7 - PERFUMING
					"crePrim" : (1.0,1.0,1.0), #color of creature
					"clothesIndex" : 9999, #index of clothes type
					"clothesPrim" : (9999,9999,9999), #color of clothes
					"clothesSeco" : (9999,9999,9999), #color of clothes
					"clothesTert" : (9999,9999,9999), #color of clothes
					"clothesQuad" : (9999,9999,9999) #color of clothes
				}
				#Register the dict into the list of players
				#players.update(str(player_id) = temp_player)
				players[player_id] = temp_player

			if "CRE_NAME" in data:
				#Parse data for name
				extracted_data = re.findall("CRE_NAME<(.*)>END_CRE_NAME", data)
				#Register the new name in the player dict
				players[player_id]["name"] = extracted_data[0]

			if "CRE_PRIM" in data: 
				#Parse data for crePrim
				extracted_data = re.findall("CRE_PRIM<(.*),(.*),(.*)>END_CRE_PRIM", data)
				#Register the new color in the player dict
				players[player_id]["crePrim"] = (extracted_data[0][0],extracted_data[0][1],extracted_data[0][2])

			if "CRE_POS" in data:
				#Parse data for position
				extracted_data = re.findall("CRE_POS<(.*),(.*),(.*)>END_CRE_POS", data)
				#Register the new data in the player dict
				players[player_id]["pos"] = (extracted_data[0][0],extracted_data[0][1],extracted_data[0][2])

			if "CLOTHES_INDEX" in data:
				#Parse data for name
				extracted_data = re.findall("CLOTHES_INDEX<(.*)>END_CLOTHES_INDEX", data)
				#REgister in player dict
				players[player_id]["clothesIndex"] = extracted_data[0]

			if "CLOTHES_PRIM" in data: 
				#Parse data 
				extracted_data = re.findall("CLOTHES_PRIM<(.*),(.*),(.*)>END_CLOTHES_PRIM", data)
				#Register the new color in the player dict
				players[player_id]["clothesPrim"] = (extracted_data[0][0],extracted_data[0][1],extracted_data[0][2])

			if "CLOTHES_SECO" in data: 
				#Parse data 
				extracted_data = re.findall("CLOTHES_SECO<(.*),(.*),(.*)>END_CLOTHES_SECO", data)
				#Register the new color in the player dict
				players[player_id]["clothesSeco"] = (extracted_data[0][0],extracted_data[0][1],extracted_data[0][2])
			
			if "CLOTHES_TERT" in data: 
				#Parse data 
				extracted_data = re.findall("CLOTHES_TERT<(.*),(.*),(.*)>END_CLOTHES_TERT", data)
				#Register the new color in the player dict
				players[player_id]["clothesTert"] = (extracted_data[0][0],extracted_data[0][1],extracted_data[0][2])

			if "CLOTHES_QUAD" in data: 
				#Parse data 
				extracted_data = re.findall("CLOTHES_QUAD<(.*),(.*),(.*)>END_CLOTHES_QUAD", data)
				#Register the new color in the player dict
				players[player_id]["clothesQuad"] = (extracted_data[0][0],extracted_data[0][1],extracted_data[0][2])

			#concerning MAP RECORDING
			if "NEW_MAP" in data:
				#Parse data
				extracted_data = re.findall("NEW_MAP<(\d+),(\d+),(\d+)>END_NEW_MAP", data)
				print(extracted_data)
				#

			if "PUT_TILE_DATA" in data:
				#Parse data
				extracted_data = re.findall("PUT_TILE_DATA<(\d+),(\d+),(\d+),(\d+)>END_PUT_TILE_DATA", data)
				#extracted_data now is a list of tuples of the form (x,y,z,tile_index)
				for tile_tuple in extracted_data:
					#Convert the items in tuples to numbers (ints)
					temp_tile_x = int(tile_tuple[0])
					temp_tile_y = int(tile_tuple[1])
					temp_tile_z = int(tile_tuple[2])
					temp_tile_index = int(tile_tuple[3])
					#REGISTER IN WORLD DATA
					world_tiles[temp_tile_x][temp_tile_y][temp_tile_z] = temp_tile_index
					print(" new put")
					print(world_tiles)


			conn.sendall("MSG_CONF")
			#We will send these commands every time we get a new message
			#SEND newCre positions
			for key in newCres.keys():
				print(key)

			#print(players)

		except KeyboardInterrupt:
			print("closing from key")
			if conn:  # <---
				conn.close()
			break  # <---

		except Exception as e:
			print(e)
			if conn:  # <---
				conn.close()
			break



	#Means we aren't talking anymore
	#Connection Closed
	print("Lost connection")
	conn.close()

##MAIN ROUTINE STARTS HERE
###########################

#Initialize world variables...
for i in range(num_x_layers):
	temp_row = []
	for j in range(num_y_layers):
		temp_col = []
		for k in range(num_z_layers):
			temp_item = "UNS"
			temp_col.append(temp_item)
		temp_row.append(temp_col)
	world_tiles.append(temp_row)


#Bind Server Socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
	s.bind((server,port))
except socket.error as e:
	str(e)

s.listen(2)
print("Start Server")

##Main Server Code (always listening)
player_counter = 0
while True:
	conn, addr = s.accept()
	print("connected to:", addr)
	start_new_thread(threaded_client, (conn, player_counter))
	player_counter = player_counter + 1






