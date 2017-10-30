for a in $(hostname -I)
do
	if [ "${#a}" -lt 16 ]; then
		sudo nmap -sn $(echo $a | grep -E '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}' | rev | cut -d . -f2- | rev).*
	fi
done
