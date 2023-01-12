BIN_FILE=cacher
TEMP_DIR="mkr-cacher"
ROOT_DIR=$(realpath --relative-to=$TMPDIR/$TEMP_DIR ..)
mkdir -p bin/

if [ -f bin/$BIN_FILE ]; then
    echo Module already installed. Exiting
    exit
fi


echo Installing module

echo Clonning source code
git clone https://github.com/cubicbyte/mkr-cacher $TMPDIR/$TEMP_DIR

echo Building module
cd $TMPDIR/$TEMP_DIR
go build -o $BIN_FILE

mv $BIN_FILE $ROOT_DIR/bin/
cd $ROOT_DIR
rm -rf $TMPDIR/$TEMP_DIR

echo Done
