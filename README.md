# P2P network overlay using Information Centric Networking Protocols (NDN)

This is Project 3 for the Scalable Computing module.

## Instructions to run code:

All nodes in the Rovers network are configured to run on Pi 1, and the Bases network on Pi 9.

1. On Pi 1 Cd into the project folder.<br />
2. To start the Rovers network, run the command:  source .tmux/ndn-rovers <br />

3. On Pi 9 Cd into the project folder. <br />
4. To start the Bases network, run the command: source .tmux/ndn-bases<br />

5. On both Pi's, run the command: tmux attach

    This allows you to interface with the nodes in the network.<br />

6. Press ctrl+b then w to see the list of selectable nodes on each Pi.<br />

7. Select a node with the arrow keys and press enter to access the node's terminal.<br />

    The nodes command lines prompts to ‘Ask the network for information:’. 
8. Type in some data name from the list below, or enter a sensor to receive data from (eg. "/bases/base2/power" or "/rovers/rover5/humidity").

    Queryable data: "temperature", "volcanic_activity", "position", "humidity", "lidar", "pressure", "light", "soil_composition", "battery", "radiation", "camera", "power", "repair_kit", "position".

9. Wait for the data to return. You can track the routing by switching to other nodes.<br />
10. To exit tmux, press ctrl+b then d. 
11. To kill the network and all running ports, enter the command: tmux kill-server
