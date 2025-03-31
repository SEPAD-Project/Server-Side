#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <microhttpd.h>
#include <cjson/cJSON.h>
#include <ini.h>
#include <direct.h>
#include <windows.h>

#define MAX_LINE 256
#define MAX_PATH 4096

typedef struct {
    char schools_path[MAX_PATH];
    int screen_result_server_port;
} ServerConfig;

ServerConfig config;




static int config_handler(void *user, const char *section,
                         const char *name, const char *value) {
    ServerConfig *cfg = (ServerConfig*)user;
    if (strcmp(section, "Server") == 0) {
        if (strcmp(name, "schools_path") == 0) {
            strncpy(cfg->schools_path, value, MAX_PATH);
        } else if (strcmp(name, "screen_result_server_port") == 0) {
            cfg->screen_result_server_port = atoi(value);
        }
    }
    return 1;
}

int main() {

    if (ini_parse("config.ini", config_handler, &config) < 0) {
        fprintf(stderr, "Failed to load config.ini\n");
        return 1;
    }


    struct MHD_Daemon *daemon;
    daemon = MHD_start_daemon(
        MHD_USE_THREAD_PER_CONNECTION,
        config.screen_result_server_port,
        NULL, NULL, &handler, NULL,
        MHD_OPTION_END);

    if (!daemon) {
        fprintf(stderr, "Failed to start server\n");
        return 1;
    }

    printf("Server running on port %d\n", config.screen_result_server_port);
    printf("Press Enter to stop...\n");
    getchar();

    MHD_stop_daemon(daemon);
    return 0;
}