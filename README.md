# P2P network overlay using Information Centric Networking Protocols (NDN)

On Pi 1 Cd into the project folder.<br />
Run the command:  source .tmux/ndn-rovers <br />
This starts the diver network.\newline
On Pi 9 Cd into the project folder. <br />
Run the command: source .tmux/ndn-bases<br />
Run the command on both Pi's: tmux attach
This allows you to interface with the nodes in the network.<br />
To see a list of selectable node press ctrl+b then w.<br />
Select a node with the arrow keys and press enter to use the nodes terminal.<br />
The nodes command lines prompts to ‘Ask the network for information:’. Type in some data name from this list of data names at the end of this document. If an invalid name is typed the data won’t send. NOTE: These are the sensors currently operating: ("temperature", "volcanic_activity", "position", "humidity", "lidar", "pressure", "light", "soil_composition", "battery", "radiation", "camera", "power"). Power and Position on the bases, the rest on the rovers (position on rovers too).<br />
Wait for the data to return. You can track the routing by switching to other nodes.<br />
To exit tmux, press ctrl+b then d. <br />
To kill the network and all running ports, enter the command: tmux kill-server
