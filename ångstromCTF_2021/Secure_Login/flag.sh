while [ ! "`echo $result | grep 'actf'`" ]
do
    result=$(echo -e "\n" | ./login)
done
echo $result