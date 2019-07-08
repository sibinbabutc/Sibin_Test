#/bin/sh
if [ "$1" = "mount" ]; then
    mount --bind $2 $3
elif [ "$1" = "umount" ]; then
    umount $2
else
    echo 'Unsuported command'
fi