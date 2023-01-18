BIN_FILE=cacher
TEMP_DIR=$TMPDIR/mkr-cacher

# Read root dir path
skip_input="false"
while getopts "y:" flag; do
    case "${flag}" in
        y) skip_input="true" ;;
    esac
done

DEF_ROOT_DIR=$(dirname $(dirname $(realpath $0)))
if [ $skip_input != "true" ]; then
    printf "Enter the path to the bot's root directory [default $DEF_ROOT_DIR]\n>>> "
    read root_dir
fi

if [ -z $root_dir ]; then
    root_dir=$DEF_ROOT_DIR
fi

if [ -f $root_dir/bin/$BIN_FILE ]; then
    echo Module already installed. Exiting
    exit
fi


echo Installing module

echo Cloning source code
git clone https://github.com/cubicbyte/mkr-cacher $TEMP_DIR

echo Building module
cd $TEMP_DIR
go build -o $BIN_FILE main.go

mkdir -p $root_dir/bin
mv $BIN_FILE $ROOT_DIR/bin/
cd $ROOT_DIR
rm -rf $TEMP_DIR

echo Done
