#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>

#ifdef WIN32
#include <io.h>
#define F_OK 0
#define access _access
#endif

int main() {
    int retries = 0;

    printf("Waiting for commands..\n");
    system("./adb/adb kill-server");
    system("./adb/adb start-server");
    system("./adb/adb devices > /dev/null");        // opens prompt on device

    while(1){
        if(access("./toggle_airplane", F_OK) == 0) {
            FILE *ptr = fopen("./toggle_airplane", "r");
            int wait = 0;
            if (!ptr) {
                perror("file can't be opened");
            } else {
                char ch = fgetc(ptr);
                if (ch != EOF)
                    wait = 1;
                fclose(ptr);
            }
            
            system("./adb/adb shell svc data disable");
            system("./adb/adb shell cmd connectivity airplane-mode enable");
            system("./adb/adb shell settings put global airplane_mode_on 1");
            system("./adb/adb shell am broadcast -a android.intent.action.AIRPLANE_MODE");
            usleep(1000*100); // sleep for 100ms
            system("./adb/adb shell cmd connectivity airplane-mode disable");
            system("./adb/adb shell svc data enable");
            system("./adb/adb shell settings put global airplane_mode_on 0");
            system("./adb/adb shell am broadcast -a android.intent.action.AIRPLANE_MODE");

            if(wait) {
                printf("sleeping for 5s\n");
                sleep(5);
                remove("./toggle_airplane");
            } else {
                remove("./toggle_airplane");
            }
        }
    }

    system("./adb/adb kill-server");
}