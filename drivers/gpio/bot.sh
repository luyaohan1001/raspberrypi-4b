make clean
echo '-> compiling laser.ko kernel module...'
make
echo '-> - done -'

# Determine if laser.ko is already loaded.
if [[ `lsmod | grep 'laser'` != '' ]];
then 
	echo '-> laser.ko already inserted, removing it now...'
	sudo rmmod laser.ko
	echo '-> - done -'
fi


echo '-> inserting laser.ko kernel module...'
sudo insmod laser.ko
echo '-> - done -'


