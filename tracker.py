from NatNetClient import NatNetClient
import DataDescriptions
import MoCapData
import sys
import time

file_name = ""
is_recording = False
start_time = 0
current_position = None
current_orientation = None
current_frame = None
is_running = False
streaming_client = None

# This is a callback function that gets connected to the NatNet client
# and called once per mocap frame.
def receive_new_frame(data_dict):
    global current_frame, file_name 
    order_list=[ "frameNumber", "markerSetCount", "unlabeledMarkersCount", "rigidBodyCount", "skeletonCount",
                "labeledMarkerCount", "timecode", "timecodeSub", "timestamp", "isRecording", "trackedModelsChanged" ]
    dump_args = False
    if dump_args == True:
        out_string = "    "
        for key in data_dict:
            out_string += key + "="
            if key in data_dict :
                out_string += data_dict[key] + " "
            out_string+="/"
        #print(data_dict.keys())
        print(out_string)
    current_frame = data_dict
    #if is_recording:
    #    the_time = time.time() - start_time
    #     file = open(file_name+'_frame_','a')
    #    file.write(str(the_time)+'\t'+str(position[0])+'\t'+str(position[1])+'\t'+str(position[2])+'\t'+str(rotation[0])+'\t'+str(rotation[1])+'\t'+str(rotation[2])+'\n')
    #     file.close()
    pass        
# This is a callback function that gets connected to the NatNet client. It is called once per rigid body per frame
def receive_rigid_body_frame( new_id, position, rotation ):
    global current_position, current_orientation, start_time, file   
    # Some Paul magic which converts the forward position directly into an amplitude of the NF
    # position_x = position[0]
    #position_x = 360*((position_x+0.0110)/(1.012+0.0110))#Deze werkt
    #position_z = position[2]
#    sim.setElementParameters('hand', 'amplitude', position_z*1.15)
#    sim.setElementParameters('hand', 'position', position_x)
    current_position = position
    current_orientation = rotation
    if is_recording:
        the_time = time.time() - start_time
    #    file = open(file_name,'a')
        file.write(str(the_time)+'\t'+str(position[0])+'\t'+str(position[1])+'\t'+str(position[2])+'\t'+str(rotation[0])+'\t'+str(rotation[1])+'\t'+str(rotation[2])+'\n')
    #    file.close()
    #pass

def print_configuration(natnet_client):
    #print("Connection Configuration:")
    #print("  Client:          %s"% natnet_client.local_ip_address)
    #print("  Server:          %s"% natnet_client.server_ip_address)
    #print("  Command Port:    %d"% natnet_client.command_port)
    #print("  Data Port:       %d"% natnet_client.data_port)

    if natnet_client.use_multicast:
        #print("  Using Multicast")
        #print("  Multicast Group: %s"% natnet_client.multicast_address)
        pass
    else:
        #print("  Using Unicast")
        pass

    #NatNet Server Info
    application_name = natnet_client.get_application_name()
    nat_net_requested_version = natnet_client.get_nat_net_requested_version()
    nat_net_version_server = natnet_client.get_nat_net_version_server()
    server_version = natnet_client.get_server_version()

##    print("  NatNet Server Info")
##    print("    Application Name %s" %(application_name))
##    print("    NatNetVersion  %d %d %d %d"% (nat_net_version_server[0], nat_net_version_server[1], nat_net_version_server[2], nat_net_version_server[3]))
##    print("    ServerVersion  %d %d %d %d"% (server_version[0], server_version[1], server_version[2], server_version[3]))
##    print("  NatNet Bitstream Requested")
##    print("    NatNetVersion  %d %d %d %d"% (nat_net_requested_version[0], nat_net_requested_version[1],\
##       nat_net_requested_version[2], nat_net_requested_version[3]))
    #print("command_socket = %s"%(str(natnet_client.command_socket)))
    #print("data_socket    = %s"%(str(natnet_client.data_socket)))


def print_commands(can_change_bitstream):
    outstring = "Commands:\n"
    outstring += "Return Data from Motive\n"
    outstring += "  s  send data descriptions\n"
    outstring += "  r  resume/start frame playback\n"
    outstring += "  p  pause frame playback\n"
    outstring += "     pause may require several seconds\n"
    outstring += "     depending on the frame data size\n"
    outstring += "Change Working Range\n"
    outstring += "  o  reset Working Range to: start/current/end frame = 0/0/end of take\n"
    outstring += "  w  set Working Range to: start/current/end frame = 1/100/1500\n"
    outstring += "Return Data Display Modes\n"
    outstring += "  j  print_level = 0 supress data description and mocap frame data\n"
    outstring += "  k  print_level = 1 show data description and mocap frame data\n"
    outstring += "  l  print_level = 20 show data description and every 20th mocap frame data\n"
    outstring += "Change NatNet data stream version (Unicast only)\n"
    outstring += "  3  Request 3.1 data stream (Unicast only)\n"
    outstring += "  4  Request 4.0 data stream (Unicast only)\n"
    outstring += "t  data structures self test (no motive/server interaction)\n"
    outstring += "c  show configuration\n"
    outstring += "h  print commands\n"
    outstring += "q  quit\n"
    outstring += "\n"
    outstring += "NOTE: Motive frame playback will respond differently in\n"
    outstring += "       Endpoint, Loop, and Bounce playback modes.\n"
    outstring += "\n"
    outstring += "EXAMPLE: PacketClient [serverIP [ clientIP [ Multicast/Unicast]]]\n"
    outstring += "         PacketClient \"192.168.10.14\" \"192.168.10.14\" Multicast\n"
    outstring += "         PacketClient \"127.0.0.1\" \"127.0.0.1\" u\n"
    outstring += "\n"
    #print(outstring)

def add_lists(totals, totals_tmp):
    totals[0]+=totals_tmp[0]
    totals[1]+=totals_tmp[1]
    totals[2]+=totals_tmp[2]
    return totals

def variables(voorwerp):

    voorwerp = voorwerp
    return voorwerp

def request_data_descriptions(s_client):
    # Request the model definitions
    s_client.send_request(s_client.command_socket, s_client.NAT_REQUEST_MODELDEF,    "",  (s_client.server_ip_address, s_client.command_port) )

def test_classes():
    totals = [0,0,0]
    print("Test Data Description Classes")
    totals_tmp = DataDescriptions.test_all()
    totals=add_lists(totals, totals_tmp)
    print("")
    print("Test MoCap Frame Classes")
    totals_tmp = MoCapData.test_all()
    totals=add_lists(totals, totals_tmp)
    print("")
    print("All Tests totals")
    print("--------------------")
    print("[PASS] Count = %3.1d"%totals[0])
    print("[FAIL] Count = %3.1d"%totals[1])
    print("[SKIP] Count = %3.1d"%totals[2])

def my_parse_args(arg_list, args_dict):
    # set up base values
    arg_list_len=len(arg_list)
    if arg_list_len>1:
        args_dict["serverAddress"] = arg_list[1]
        if arg_list_len>2:
            args_dict["clientAddress"] = arg_list[2]
        if arg_list_len>3:
            if len(arg_list[3]):
                args_dict["use_multicast"] = True
                if arg_list[3][0].upper() == "U":
                    args_dict["use_multicast"] = False

    return args_dict

def init_tracker():
    global is_running, streaming_client
 #NatNetCliet shizzle

    optionsDict = {}
    optionsDict["clientAddress"] = "127.0.0.1"
    optionsDict["serverAddress"] = "127.0.0.1"
    optionsDict["use_multicast"] = True

    # This will create a new NatNet client
    optionsDict = my_parse_args(sys.argv, optionsDict)

    streaming_client = NatNetClient()
    streaming_client.set_client_address(optionsDict["clientAddress"])
    streaming_client.set_server_address(optionsDict["serverAddress"])
    streaming_client.set_use_multicast(optionsDict["use_multicast"])

    # Configure the streaming client to call our rigid body handler on the emulator to send data out.
    streaming_client.new_frame_listener = receive_new_frame
    streaming_client.rigid_body_listener = receive_rigid_body_frame
    
    # Start up the streaming client now that the callbacks are set up.
    # This will run perpetually, and operate on a separate thread.
    streaming_client.set_print_level(0)
    is_running = streaming_client.run()
    if not is_running:
        print("ERROR: Could not start streaming client.")
        try:
            sys.exit(1)
        except SystemExit:
            print("...")
        finally:
            print("exiting")

    
    time.sleep(1)
    if streaming_client.connected() is False:
        #print("ERROR: Could not connect properly.  Check that Motive streaming is on.")
        try:
            sys.exit(2)
        except SystemExit:
            print("...")
        finally:
            print("exiting")

            
    print_configuration(streaming_client)
    print("\n")
    print_commands(streaming_client.can_change_bitstream_version())

    tmpCommands=["TimelinePlay",
                "TimelineStop",
                "SetPlaybackStartFrame,0",
                "SetPlaybackStopFrame,1000000",
                "SetPlaybackLooping,0",
                "SetPlaybackCurrentFrame,0",
                "TimelineStop"]
    for sz_command in tmpCommands:
        return_code = streaming_client.send_command(sz_command)
        print("Command: %s - return_code: %d"% (sz_command, return_code) )
    time.sleep(1)
    
    return streaming_client

def do_command(sz_command):
    global streaming_client

    return_code = streaming_client.send_command(sz_command)
    print("Command: %s - return_code: %d"% (sz_command, return_code) )
    return return_code

def start_recording(name):
    global file_name, is_recording, file
    file_name = name
    short_name = name.split('.')[0]
    try:
        #outfile=open(file_name,'w')
        file = open(file_name,'a')
        is_recording = True
        do_command("SetRecordTakeName," + short_name )
        do_command("StartRecording")
        return file    #was outfile
    except:
        return None
        pass

def stop_recording():
    global file_name, is_recording, file
    is_recording = False
    do_command("StopRecording")
    time.sleep(1)
    file.close()
    file_name = ""
    

if __name__=="__main__":
    s_client = init_tracker()

    print_configuration(s_client)
    print("\n")
    print_commands(s_client.can_change_bitstream_version())
    
    # start_recording('testopti.txt')
    # time.sleep(3)
    # stop_recording()

    # time.sleep(5)
    do_command('LiveMode')            
    try:
        count=1000
        while count>0:
            if current_position != None:
                print(current_position)
            count-=1
    except:
        pass
    finally:
        is_looping = False
        is_running = False
        is_recording = False
        s_client.shutdown()
