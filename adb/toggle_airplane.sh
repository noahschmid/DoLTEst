./adb kill-server
./adb start-server
./adb shell settings put global airplane_mode_on 1
./adb shell am broadcast -a android.intent.action.AIRPLANE_MODE
sleep 2
./adb shell settings put global airplane_mode_on 0
./adb shell am broadcast -a android.intent.action.AIRPLANE_MODE
./adb kill-server
