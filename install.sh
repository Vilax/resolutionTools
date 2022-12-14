#!/bin/sh

# This script download all programs requires to run the Fourier Shell Occupancy algorithm

# The first step is to download Xmipp-lite and compile it (Xmipp lite is a xmipp version without CUDA, python, just resolution related algorithms)

echo "Cloning xmipp-lite repository..."
git clone https://github.com/I2PC/xmipp.git && cd xmipp

echo " "
echo " "
echo "Compiling xmipp..."
echo " "

chmod +x xmipp
./xmipp
cd ..

echo " "
echo " "
echo "Creating a virtual enviroment..."

ifvenv=$(pip list | grep virtualenv)
if [ "$ifvenv" != "*virtualenv*" ];
then
pip install virtualenv
fi

python3 -m venv env
. env/bin/activate
pip install --upgrade pip
pip install pyqt5
pip install matplotlib

# Editing paths
INITFILE="config.ini"
rm ${INITFILE}
XMIPP_PATH="/xmipp/build"

echo "[EXTERNAL_PROGRAMS]" >> $INITFILE
echo "XMIPP_PATH = ${PWD}${XMIPP_PATH}" >> $INITFILE


EXECUTABLEFILE="localResolutiontools"
echo "cd $(pwd)" >> $EXECUTABLEFILE
echo "$source ./xmipp/build/xmipp.bashrc" >> $EXECUTABLEFILE
echo "$(pwd)/main.py" >> $EXECUTABLEFILE
chmod +x ${EXECUTABLEFILE}

