#!/usr/bin/env bash

# update
sudo apt-get update

# utils
sudo apt-get install -y \
    firefox \
    tmux \
    tig \
    python-pip \
    python3-pip \
    gtk+3.0 \
    pavucontrol \
    adb \
    cmake \
    swig

pip3 install \
   numpy==1.19.5 \
   matplotlib==3.3.4 \
   PyQt5==5.9.2 \
   pandas==1.1.5 \
   tabulate==0.8.9 \
   tqdm==4.48.0 \
   click==7.1.2


# sdr tools
sudo apt-get -y install git swig doxygen build-essential libboost-all-dev libtool libusb-1.0-0 libusb-1.0-0-dev libudev-dev libncurses5-dev libfftw3-bin libfftw3-dev \
   libfftw3-doc libcppunit-1.14-0 libcppunit-dev libcppunit-doc ncurses-bin cpufrequtils python-numpy python-numpy-doc python-numpy-dbg python-scipy python-docutils qt4-bin-dbg \
   qt4-default qt4-doc libqt4-dev libqt4-dev-bin python-qt4 python-qt4-dbg python-qt4-dev python-qt4-doc python-qt4-doc libqwt6abi1 libfftw3-bin libfftw3-dev libfftw3-doc ncurses-bin \
   libncurses5 libncurses5-dev libncurses5-dbg libfontconfig1-dev libxrender-dev libpulse-dev swig g++ automake autoconf libtool python-dev libfftw3-dev libcppunit-dev libboost-all-dev \
   libusb-dev libusb-1.0-0-dev fort77 libsdl1.2-dev python-wxgtk3.0 libqt4-dev python-numpy ccache python-opengl libgsl-dev python-cheetah python-mako python-lxml doxygen qt4-default \
   qt4-dev-tools libusb-1.0-0-dev libqwtplot3d-qt5-dev pyqt4-dev-tools python-qwt5-qt4 wget libxi-dev gtk2-engines-pixbuf r-base-dev python-tk liborc-0.4-0 liborc-0.4-dev \
   libasound2-dev python-gtk2 libzmq3-dev libzmq5 python-requests python-sphinx libcomedi-dev python-zmq libqwt-dev libqwt6abi1 python-six libgps-dev libgps23 gpsd gpsd-clients \
   python-gps python-setuptools


sudo apt-get install -y build-essential pkg-config libboost-dev \
   libboost-date-time-dev libboost-system-dev libboost-filesystem-dev \
   libboost-thread-dev libboost-chrono-dev libboost-serialization-dev \
   libboost-program-options-dev libboost-test-dev liblog4cpp5-dev \
   libuhd-dev gnuradio-dev gr-osmosdr libblas-dev liblapack-dev \
   libarmadillo-dev libgflags-dev libgoogle-glog-dev libhdf5-dev \
   libgnutls-openssl-dev libmatio-dev libpugixml-dev libpcap-dev \
   libprotobuf-dev protobuf-compiler libgtest-dev googletest \
   python3-mako python3-six


# sdr dongles
sudo apt-get install -y \
    hackrf \
    uhd-host \
    rtl-sdr

sudo uhd_images_downloader

cd /etc/udev/rules.d
sudo wget https://raw.githubusercontent.com/keenerd/rtl-sdr/master/rtl-sdr.rules
sudo wget https://raw.githubusercontent.com/EttusResearch/uhd/master/host/utils/uhd-usrp.rules
sudo wget https://raw.githubusercontent.com/mossmann/hackrf/master/host/libhackrf/53-hackrf.rules
sudo udevadm control --reload-rules
sudo usermod -a -G plugdev vagrant

sudo apt-get install -y build-essential cmake libfftw3-dev libmbedtls-dev libboost-program-options-dev libconfig++-dev libsctp-dev

cd /home/vagrant/

git clone git@github.com:SysSec-KAIST/DoLTEst.git
cd /home/vagrant/DoLTEst
mkdir build && cd build
cmake ..
make -j 8

