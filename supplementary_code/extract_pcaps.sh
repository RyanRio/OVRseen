# PCAPs
# Copy and extract all PCAP files
unzip ~/Desktop/PCAPs.zip -d ../network_traffic/post-processing/
#unzip "../network_traffic/post-processing/PCAPs/Oculus-Free/*.zip" -d ../network_traffic/post-processing/PCAPs/Oculus-Free/
unzip "../network_traffic/post-processing/PCAPs/Oculus-Paid/*.zip" -d ../network_traffic/post-processing/PCAPs/Oculus-Paid/
#unzip "../network_traffic/post-processing/PCAPs/SideQuest/*.zip" -d ../network_traffic/post-processing/PCAPs/SideQuest/
rm -rf ../network_traffic/post-processing/PCAPs/Oculus-Free/
rm -rf ../network_traffic/post-processing/PCAPs/SideQuest/
