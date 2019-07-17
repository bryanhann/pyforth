old=`stat -f "%m" main.py`
while true ; do
    sleep .1
    new=`stat -f "%m" main.py`
    [ "$old" == "$new" ] && continue
    echo change
    old=$new
    clear
    python3 main.py
done
