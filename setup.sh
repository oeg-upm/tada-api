apt update
apt install cmake g++ -y
apt install zip wget curl git -y


echo "Install coverage... "
apt install gcovr -y

echo "Installing hdt-cpp..."
apt install vim -y 
apt install autoconf -y
apt install libtool -y
apt install pkg-config -y
apt install libserd-0-0 libserd-dev -y
apt install zlib1g-dev -y
apt install automake -y
wget https://github.com/drobilla/serd/archive/v0.30.0.zip
unzip v0.30.0.zip
rm -Rf v0.30.0.zip
cd serd-0.30.0; ./waf configure ; ./waf ; ./waf install;cd ..; rm -Rf serd-0.30.0
wget https://github.com/rdfhdt/hdt-cpp/archive/v1.3.3.zip
unzip v1.3.3.zip
rm v1.3.3.zip 
cd hdt-cpp-1.3.3;./autogen.sh;./configure;make -j2;make install; cd ..;rm -Rf hdt-cpp-1.3.3


echo "Installing easy-logger... "
wget https://github.com/ahmad88me/easy-logger/archive/v1.0.zip
unzip v1.0.zip
rm  v1.0.zip
cd easy-logger-1.0;make install;cd ..;rm -Rf easy-logger-1.0

echo "Installing tabular-parser... "
wget https://github.com/ahmad88me/tabular-parser/archive/v1.3.zip
unzip v1.3.zip
rm v1.3.zip
cd tabular-parser-1.3;make install;cd ..;rm -Rf tabular-parser-1.3

echo "Installing tada-hdt-entity... "
wget https://github.com/oeg-upm/tada-hdt-entity/archive/v1.5.zip
unzip v1.5.zip
rm v1.5.zip
cd tada-hdt-entity-1.5;make install;cd ..;rm -Rf tada-hdt-entity-1.5

echo "update linker caches..."
ldconfig
