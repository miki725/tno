# install latest bootstrap version into tno project

LIB_PATH=../tno/tno/static/lib/bootstrap
FOLDER_NAME=bootstrap-master
ZIP_NAME=bootstrap.zip

echo "Downloading bootstrap"
echo "---------------------"
wget -O $ZIP_NAME https://github.com/twbs/bootstrap/archive/master.zip --quiet
unzip $ZIP_NAME

echo "Removing js tests"
echo "-----------------"
rm -rf $FOLDER_NAME/js/tests $FOLDER_NAME/js/.jshintrc

echo "Copying into django project"
echo "---------------------------"
rm -rf $LIB_PATH
mkdir -p $LIB_PATH
mv $FOLDER_NAME/fonts $FOLDER_NAME/js $FOLDER_NAME/less $LIB_PATH

echo "Cleanup"
echo "-------"
rm -rf bootstrap*
