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

	recvBuffer = "" #a buffer to keep track of all the recieved data

	#Loop For Duration of Server-Client Communication
	while True:
		try:
			data = conn.recv(2*2048)#.decode('utf-8')
			recvBuffer = recvBuffer + str(data)
			print("This is the data:" + str(data) + "\0")
			print("\n\n\n\n\n\n")
			#print("BUFFER")
			#print("This is the buffer" + str(recvBuffer))

			if not data:
				print("disconnected")
				break
			else:
				print("We recieved some data")

			#Parse and Process Data Here
			#Strip the TCP chunk characters 4) and (0 and 4*
			recvBuffer = recvBuffer.replace("4)", "")
			recvBuffer = recvBuffer.replace("(0", "")
			recvBuffer = recvBuffer.replace("4*", "")

			if "PRINT_BUFFER" in recvBuffer:
				print(recvBuffer)

				#REMOVE COMMAND FROM BUFFER...
				recvBuffer = recvBuffer.replace("PRINT_BUFFER", "")

			#concerning PLAYER REGISTRATION
			if "REGISTER" in recvBuffer:
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
				isRegistered = True

				#REMOVE COMMAND FROM BUFFER...
				recvBuffer = recvBuffer.replace("REGISTER", "")

			if "CRE_NAME" in recvBuffer:
				print("cjecl name")
				#Parse data for name
				extracted_data = re.findall("CRE_NAME<([A-Za-z]*)>END_CRE_NAME", recvBuffer)
				#Register the new name in the player dict
				players[player_id]["name"] = extracted_data[0]

				#REMOVE COMMAND FROM BUFFER...
				recvBuffer = recvBuffer.replace("CRE_NAME<"+extracted_data[0]+">END_CRE_NAME", "")

				print("end name")

			if "CRE_PRIM" in recvBuffer: 
				print("cjecl cre prim")
				#Parse data for crePrim (note that weird regex expression to match float or int)
				extracted_data = re.findall("CRE_PRIM<(\d+(?:\.\d+)?),(\d+(?:\.\d+)?),(\d+(?:\.\d+)?)>END_CRE_PRIM", data)
				#Register the new color in the player dict
				players[player_id]["crePrim"] = (extracted_data[0][0],extracted_data[0][1],extracted_data[0][2])

				#REMOVE COMMAND FROM BUFFER...
				recvBuffer = recvBuffer.replace("CRE_PRIM<"+extracted_data[0][0]+","+extracted_data[0][1]+","+extracted_data[0][2]+">END_CRE_PRIM", "")

				print("end cre prim")

			if "CRE_POS" in recvBuffer:
				print("cjecl cre pos")
				#Parse data for position
				extracted_data = re.findall("CRE_POS<(\d+),(\d+),(\d+)>END_CRE_POS", data)
				#Register the new data in the player dict
				players[player_id]["pos"] = (extracted_data[0][0],extracted_data[0][1],extracted_data[0][2])

				#REMOVE COMMAND FROM BUFFER...
				recvBuffer = recvBuffer.replace("CRE_POS<"+extracted_data[0][0]+","+extracted_data[0][1]+","+extracted_data[0][2]+">END_CRE_POS", "")

			if "CLOTHES_INDEX" in recvBuffer:
				print("cjecl cloth ind")
				#Parse data for name
				extracted_data = re.findall("CLOTHES_INDEX<(\d+)>END_CLOTHES_INDEX", data)
				#REgister in player dict
				players[player_id]["clothesIndex"] = extracted_data[0]

				#REMOVE COMMAND FROM BUFFER...
				recvBuffer = recvBuffer.replace("CLOTHES_INDEX<"+extracted_data[0]+">END_CLOTHES_INDEX", "")

			if "CLOTHES_PRIM" in recvBuffer: 
				print("cjecl cloth prim")
				#Parse data 
				extracted_data = re.findall("CLOTHES_PRIM<(\d+(?:\.\d+)?),(\d+(?:\.\d+)?),(\d+(?:\.\d+)?)>END_CLOTHES_PRIM", data)
				#Register the new color in the player dict
				players[player_id]["clothesPrim"] = (extracted_data[0][0],extracted_data[0][1],extracted_data[0][2])

				#REMOVE COMMAND FROM BUFFER...
				recvBuffer = recvBuffer.replace("CLOTHES_PRIM<"+extracted_data[0][0]+","+extracted_data[0][1]+","+extracted_data[0][2]+">END_CLOTHES_PRIM", "")

			if "CLOTHES_SECO" in recvBuffer: 
				print("cjecl cloth seco")
				#Parse data 
				extracted_data = re.findall("CLOTHES_SECO<(\d+(?:\.\d+)?),(\d+(?:\.\d+)?),(\d+(?:\.\d+)?)>END_CLOTHES_SECO", data)
				#Register the new color in the player dict
				players[player_id]["clothesSeco"] = (extracted_data[0][0],extracted_data[0][1],extracted_data[0][2])
			
				#REMOVE COMMAND FROM BUFFER...
				recvBuffer = recvBuffer.replace("CLOTHES_SECO<"+extracted_data[0][0]+","+extracted_data[0][1]+","+extracted_data[0][2]+">END_CLOTHES_SECO", "")

			if "CLOTHES_TERT" in recvBuffer: 
				print("cjecl cloth tert")
				#Parse data 
				extracted_data = re.findall("CLOTHES_TERT<(\d+(?:\.\d+)?),(\d+(?:\.\d+)?),(\d+(?:\.\d+)?)>END_CLOTHES_TERT", data)
				#Register the new color in the player dict
				players[player_id]["clothesTert"] = (extracted_data[0][0],extracted_data[0][1],extracted_data[0][2])

				#REMOVE COMMAND FROM BUFFER...
				recvBuffer = recvBuffer.replace("CLOTHES_TERT<"+extracted_data[0][0]+","+extracted_data[0][1]+","+extracted_data[0][2]+">END_CLOTHES_TERT", "")

			if "CLOTHES_QUAD" in recvBuffer: 
				print("cjecl cloth wuad")
				#Parse data 
				extracted_data = re.findall("CLOTHES_QUAD<(\d+(?:\.\d+)?),(\d+(?:\.\d+)?),(\d+(?:\.\d+)?)>END_CLOTHES_QUAD", data)
				#Register the new color in the player dict
				players[player_id]["clothesQuad"] = (extracted_data[0][0],extracted_data[0][1],extracted_data[0][2])

				#REMOVE COMMAND FROM BUFFER...
				recvBuffer = recvBuffer.replace("CLOTHES_QUAD<"+extracted_data[0][0]+","+extracted_data[0][1]+","+extracted_data[0][2]+">END_CLOTHES_QUAD", "")

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

					#REMOVE COMMAND FROM BUFFER....
					recvBuffer = recvBuffer.replace("PUT_TILE_DATA<"+tile_tuple[0]+","+tile_tuple[1]+","+tile_tuple[2]+","+tile_tuple[3]+">END_PUT_TILE_DATA", "")


			conn.sendall("MSG_CONF")
			#We will send these commands every time we get a new message
			#SEND newCre positions
			#for key in newCres.keys():
			#	print(key)

			#print(recvBuffer)

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

def console_input_thread():
	while(True):
		read_input = raw_input("enter")
		if read_input == "t":
			print(world_tiles)

		if read_input == "p":
			print(players)		

		parse_data = re.findall("sp (\d+) (\d+) (\d+)",read_input)
		if parse_data:
			print(world_tiles[ int(parse_data[0][0]) ][int(parse_data[0][1])][int(parse_data[0][2])])


start_new_thread(console_input_thread, ())

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






