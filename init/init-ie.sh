# install latest html5shiv and respond.js version into tno project

LIB_PATH=../tno/tno/static/lib/html5shiv
NAME=html5shiv.js

echo "Prepping project for html5shiv"
echo "------------------------------"
rm -rf $LIB_PATH
mkdir -p $LIB_PATH

echo "Downloading html5shiv"
echo "---------------------"
wget -O $LIB_PATH/$NAME https://raw.github.com/aFarkas/html5shiv/master/src/$NAME --quiet


LIB_PATH=../tno/tno/static/lib/respond
NAME=respond.js

echo "Prepping project for respond.js"
echo "-------------------------------"
rm -rf $LIB_PATH
mkdir -p $LIB_PATH

echo "Downloading respond.js"
echo "----------------------"
wget -O $LIB_PATH/$NAME https://raw.github.com/scottjehl/Respond/master/src/$NAME --quiet
