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


char* sanitize_path(const char *str) {
    char *result = _strdup(str);
    for (int i = 0; result[i]; i++) {
        if (result[i] == ' ') result[i] = '_';
        if (result[i] == '/') result[i] = '\\';
    }
    return result;
}


void mkdir_p(const char *path) {
    char tmp[MAX_PATH];
    char *p = NULL;
    size_t len;

    snprintf(tmp, sizeof(tmp), "%s", path);
    len = strlen(tmp);
    if (len > 0 && tmp[len - 1] == '\\') {
        tmp[len - 1] = '\0';
    }
    
    for (p = tmp + 1; *p; p++) {
        if (*p == '\\') {
            *p = '\0';
            _mkdir(tmp);
            *p = '\\';
        }
    }
    _mkdir(tmp);
}

static int handler(void *cls, struct MHD_Connection *connection,
                  const char *url, const char *method,
                  const char *version, const char *upload_data,
                  size_t *upload_data_size, void **con_cls) {

    if (strcmp(method, "POST") == 0 && strcmp(url, "/save") == 0) {

        char *buffer = malloc(*upload_data_size + 1);
        memcpy(buffer, upload_data, *upload_data_size);
        buffer[*upload_data_size] = '\0';

        cJSON *root = cJSON_Parse(buffer);
        if (!root) {
            const char *error_msg = "{\"error\":\"Invalid JSON\"}";
            struct MHD_Response *response = MHD_create_response_from_buffer(
                strlen(error_msg), (void*)error_msg, MHD_RESPMEM_PERSISTENT);
            MHD_queue_response(connection, 400, response);
            MHD_destroy_response(response);
            free(buffer);
            return MHD_NO;
        }


        if (!cJSON_HasObjectItem(root, "school") ||
            !cJSON_HasObjectItem(root, "class") ||
            !cJSON_HasObjectItem(root, "student_id") ||
            !cJSON_HasObjectItem(root, "windows")) {
            const char *error_msg = "{\"error\":\"Missing parameters\"}";
            struct MHD_Response *response = MHD_create_response_from_buffer(
                strlen(error_msg), (void*)error_msg, MHD_RESPMEM_PERSISTENT);
            MHD_queue_response(connection, 400, response);
            MHD_destroy_response(response);
            cJSON_Delete(root);
            free(buffer);
            return MHD_NO;
        }


        char *school = sanitize_path(cJSON_GetObjectItem(root, "school")->valuestring);
        char *class = sanitize_path(cJSON_GetObjectItem(root, "class")->valuestring);
        char *student_id = cJSON_GetObjectItem(root, "student_id")->valuestring;
        cJSON *windows = cJSON_DetachItemFromObject(root, "windows");

        char path[MAX_PATH];
        snprintf(path, MAX_PATH, "%s\\%s\\%s", 
                config.schools_path, school, class);
        mkdir_p(path);


        char filename[MAX_PATH];
        snprintf(filename, MAX_PATH, "%s\\%s.json", path, student_id);
        
        FILE *fp = fopen(filename, "w");
        if (!fp) {
            const char *error_msg = "{\"error\":\"File creation failed\"}";
            struct MHD_Response *response = MHD_create_response_from_buffer(
                strlen(error_msg), (void*)error_msg, MHD_RESPMEM_PERSISTENT);
            MHD_queue_response(connection, 500, response);
            MHD_destroy_response(response);
        } else {
            char *json_str = cJSON_Print(windows);
            fwrite(json_str, 1, strlen(json_str), fp);
            fclose(fp);
            free(json_str);
        }


        cJSON_Delete(root);
        free(buffer);
        free(school);
        free(class);
        free(windows);


        const char *success_msg = "{\"status\":\"success\"}";
        struct MHD_Response *response = MHD_create_response_from_buffer(
            strlen(success_msg), (void*)success_msg, MHD_RESPMEM_PERSISTENT);
        MHD_queue_response(connection, 200, response);
        MHD_destroy_response(response);
        return MHD_YES;
    }
    else if (strcmp(method, "GET") == 0 && strcmp(url, "/get") == 0) {

        const char *school = MHD_lookup_connection_value(connection, MHD_GET_ARGUMENT_KIND, "school");
        const char *class = MHD_lookup_connection_value(connection, MHD_GET_ARGUMENT_KIND, "class");
        const char *student_id = MHD_lookup_connection_value(connection, MHD_GET_ARGUMENT_KIND, "student_id");

        if (!school || !class || !student_id) {
            const char *error_msg = "{\"error\":\"Missing parameters\"}";
            struct MHD_Response *response = MHD_create_response_from_buffer(
                strlen(error_msg), (void*)error_msg, MHD_RESPMEM_PERSISTENT);
            MHD_queue_response(connection, 400, response);
            MHD_destroy_response(response);
            return MHD_NO;
        }


        char *sanitized_school = sanitize_path(school);
        char *sanitized_class = sanitize_path(class);
        
        char filename[MAX_PATH];
        snprintf(filename, MAX_PATH, "%s\\%s\\%s\\%s.json",
                config.schools_path,
                sanitized_school,
                sanitized_class,
                student_id);


        FILE *fp = fopen(filename, "r");
        if (!fp) {
            const char *error_msg = "{\"error\":\"Data not found\"}";
            struct MHD_Response *response = MHD_create_response_from_buffer(
                strlen(error_msg), (void*)error_msg, MHD_RESPMEM_PERSISTENT);
            MHD_queue_response(connection, 404, response);
            MHD_destroy_response(response);
            free(sanitized_school);
            free(sanitized_class);
            return MHD_NO;
        }

        fseek(fp, 0, SEEK_END);
        long fsize = ftell(fp);
        fseek(fp, 0, SEEK_SET);

        char *content = malloc(fsize + 1);
        fread(content, 1, fsize, fp);
        fclose(fp);
        content[fsize] = 0;


        struct MHD_Response *response = MHD_create_response_from_buffer(
            fsize, content, MHD_RESPMEM_MUST_FREE);
        MHD_add_response_header(response, "Content-Type", "application/json");
        MHD_queue_response(connection, 200, response);
        MHD_destroy_response(response);
        
        free(sanitized_school);
        free(sanitized_class);
        return MHD_YES;
    }


    const char *error_msg = "{\"error\":\"Not found\"}";
    struct MHD_Response *response = MHD_create_response_from_buffer(
        strlen(error_msg), (void*)error_msg, MHD_RESPMEM_PERSISTENT);
    MHD_queue_response(connection, 404, response);
    MHD_destroy_response(response);
    return MHD_NO;
}

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