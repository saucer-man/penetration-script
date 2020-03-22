curl --silent https://www.threatcrowd.org/searchApi/v2/domain/report/\?domain=$1 | jq .subdomains | grep -o "\w.*$1" > tmp.txt
curl --silent https://api.hackertarget.com/hostsearch/\?q\=$1 | grep -o "\w.*$1" >> tmp.txt
curl --silent https://crt.sh/?q=%.test.com | grep -oP "\<TD\>\K.*\.$1" | sed -e 's/\<BR\>/\n/g' | grep -oP "\K.*\.$1" | sed -e 's/[\<|\>]//g'  >> tmp.txt
curl --silent https://crt.sh/?q=%.%.$1 | grep -oP "\<TD\>\K.*\.test.com" | sed -e 's/\<BR\>/\n/g' | sed -e 's/[\<|\>]//g' >> tmp.txt
curl --silent https://crt.sh/?q=%.%.%.$1 | grep "$1" | cut -d '>' -f2 | cut -d '<' -f1 | grep -v " " | sort -u >> tmp.txt
curl --silent https://crt.sh/?q=%.%.%.%.$1 | grep "$1" | cut -d '>' -f2 | cut -d '<' -f1 | grep -v " " | sort -u >> tmp.txt
curl --silent https://certspotter.com/api/v0/certs?domain=$1 | grep  -o '\[\".*\"\]' | sed -e 's/\[//g' | sed -e 's/\"//g' | sed -e 's/\]//g' | sed -e 's/\,/\n/g' >> tmp.txt
curl --silent https://findsubdomains.com/subdomains-map/$1 | grep -oP "\"name\" : \"\K\S+" | sed -e 's/\",//g' >> tmp.txt
if [[ $# -eq 2 ]]; then
    cat tmp.txt | sed -e "s/\*\.$1//g" | sort -u > $2
else
    cat tmp.txt | sed -e "s/\*\.$1//g" | sort -u
fi
rm -f tmp.txt
