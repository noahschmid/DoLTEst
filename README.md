# DoLTEst
An extension to the [DoLTEst testing framework](https://github.com/SysSec-KAIST/DoLTEst) to speed up testing time by automatically toggling airplane mode 
on the UE after each test case (only works on Android phones). Without toggling airplane mode, phones will sometimes not send attach requests for a 
longer period of time which causes a delay.

# Prerequisites
You need to install [Vagrant](https://www.vagrantup.com/) to spin up the required VM and if running on another OS than Linux, you also need the ADB SDK for 
[Windows](https://dl.google.com/android/repository/platform-tools-latest-windows.zip) or [Mac](https://dl.google.com/android/repository/platform-tools-latest-darwin.zip).

# Install
First compile the phone manager program using `make`. Then run `vagrant up` to create and start the VM. This might take a couple of minutes if run for the first time. You can then ssh into the machine using `vagrant ssh`. 
It will automatically mount the repository folder under /vagrant in the VM.

# Usage
This project builds up on [DoLTEst](https://github.com/SysSec-KAIST/DoLTEst), so we assume a familiarity with the testing process using DoLTEst.
Open up three terminals, and ssh into the VM in two of them. Run `sudo ./phone_manager` in the third one.
In the VM terminals, navigate to `/vagrant` and call the scritps `run_enb.sh` and `run_epc.sh` (one script in each terminal) to start the tests.
