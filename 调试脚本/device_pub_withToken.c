/*******************************************************************************
 *                                                                             *
 *       Copyright (c) 2013-2017 EMQ Enterprise, Inc. All Rights Reserved.     *
 *                                                                             *
 *******************************************************************************/

#include "emqx_sdk.h"

#include <time.h> 
#include <string.h> 
#include <stdarg.h>
#include "emqx_adapter.h"


#define EXPECTED_COUNT  20
#define BUFFER_SIZE  1024

static int msg_count = 0;
static char sock_receive_buf[BUFFER_SIZE];
static char sock_send_buf[BUFFER_SIZE];


void simple_log(char * fmt, va_list ap)
{
    printf(" >%ld : ", TimerNow());
    vprintf(fmt, ap);
}


// #define PRINT_BUFFER_SIZE  64
// int msg_arrived(char* topic, int topic_len, char* payload, int payloadlen, int qos, MqttBool retain)
// {
//     char buffer[PRINT_BUFFER_SIZE+1];
//     int  size = topic_len > PRINT_BUFFER_SIZE ? PRINT_BUFFER_SIZE : topic_len;

//     memcpy(&buffer[0], topic, size);
//     buffer[size] = 0;  // make topic 0-terminated

//     msg_count++;
//     MqttLogout("get topic=%s, payloadlen=%d, payload=%s, msg_count=%d\n", 
//         buffer, payloadlen, payload, msg_count);
// }

int msg_published(char * topic, char * payload)
{
    MqttLogout("msg of %s has been sent, free its payload memory 0x%x\n", payload);
    free(payload);
}

MqttBool quit_condition(void)
{
    if(msg_count > EXPECTED_COUNT)
        return MQTT_TRUE;
    else
        return MQTT_FALSE;
}

void mqtt_task(void *arg)
{
    EmqxSdkInit init = {0};

    printf("\n emqtt_sdk_version is %s \n", emqtt_sdk_version());
    printf("\n");

    // init.callbackMsgArrived = msg_arrived;
    init.callbackMsgPublished = msg_published;
    init.cleanSession = MQTT_TRUE;
    init.clientId = "d:changhongDevice_Pub";
    init.host = "mqtt.mymlsoft.com";
    init.port = 1883;
    init.keepAliveInterval = 10;
    init.logout = simple_log;
    init.username = "changhongDevice_Pub";
    init.password = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJ0YW8xLmppYW5nIiwidXNlciI6ImNoYW5naG9uZ0RldmljZV9QdWIifQ.9TG4uKfejGV9taFJ1P1b_53OCZIsIJTxeaRGBmz88AI";
    init.quitnow = quit_condition;
    init.sock_rbuf = &sock_receive_buf[0];
    init.sock_rbuf_len = BUFFER_SIZE;
    init.sock_wbuf = &sock_send_buf[0];
    init.sock_wbuf_len = BUFFER_SIZE;
    // init.subscribedTopic[0] = "a/b/#";
    // init.subscribedTopic[1] = "d/+/e";
    // init.subscribedTopicNum = 2;
    // init.subscribeQos = 1;
    init.will.topicName = "warning";
    init.will.message = "device is down";
    init.will.message_size = strlen(init.will.message);
    init.will.qos = 1;
    init.will.retained = 0;

    /* loop forever until quit_condition() return TRUE */
    emqtt_loop(&init);
}

#define  PAYLOAD_SIZE  2
/* 
 * IMPORTANT: run main function in a standalone thread(task), 
 * since main() has a dead loop 
 */
int main()
{
    char * payload = NULL;
    Thread mqttThread;
    
    ThreadStart(&mqttThread, mqtt_task, NULL);

    while(msg_count <= EXPECTED_COUNT)
    {
        TimerSleep(1000);
        payload = malloc(PAYLOAD_SIZE+2);
        payload[0] = '0' + (msg_count%10);
        payload[1] = 'e';
        payload[2] = '\0';  /* terminate payload string with 0, in order to print it */

        if( emqtt_send("mqtt/device/pub/", payload, PAYLOAD_SIZE, 1, MQTT_FALSE) == MQTT_FALSE )
        {
            MqttLogout("send message fail, queue is full\n");
            free(payload);
        }
        else
        {
            printf ("msg_count = %d \n", msg_count);
        }
        msg_count++;  
    }
    
    return 0;
}
