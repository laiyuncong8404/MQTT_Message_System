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
    printf(" >%d : ", TimerNow());
    vprintf(fmt, ap);
}


#define PRINT_BUFFER_SIZE  64
int msg_arrived(char* topic, int topic_len, char* payload, int payloadlen, int qos, MqttBool retain)
{
    char buffer[PRINT_BUFFER_SIZE+1];
    int  size = topic_len > PRINT_BUFFER_SIZE ? PRINT_BUFFER_SIZE : topic_len;

    memcpy(&buffer[0], topic, size);
    buffer[size] = 0;  // make topic 0-terminated

    msg_count++;
    MqttLogout("get topic=%s, payloadlen=%d, payload=%s, msg_count=%d\n", 
        buffer, payloadlen, payload, msg_count);
}

// int msg_published(char * topic, char * payload)
// {
//     MqttLogout("msg of %s has been sent, free its payload memory 0x%x\n", payload);
//     free(payload);
// }

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

    printf(emqtt_sdk_version());
    printf("\n\n");

    init.callbackMsgArrived = msg_arrived;
    // init.callbackMsgPublished = msg_published;
    init.cleanSession = MQTT_TRUE;
    init.clientId = "changhongDeviceSub";
    init.host = "10.3.93.241";
    init.port = 1883;
    init.keepAliveInterval = 10;
    init.logout = simple_log;
    // init.username = "admin";
    // init.password = "public";
    init.quitnow = quit_condition;
    init.sock_rbuf = &sock_receive_buf[0];
    init.sock_rbuf_len = BUFFER_SIZE;
    init.sock_wbuf = &sock_send_buf[0];
    init.sock_wbuf_len = BUFFER_SIZE;
    init.subscribedTopic[0] = "mqtt/device/#";
    init.subscribedTopic[1] = "d/+/e";
    init.subscribedTopicNum = 2;
    init.subscribeQos = 1;
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
    // int start = 0, i = 0, size = 0, loop = 0;
    // char * payload = NULL;
    Thread mqttThread;
    
    ThreadStart(&mqttThread, mqtt_task, NULL);

    while(msg_count < EXPECTED_COUNT)
    {
        TimerSleep(1000);
    }
    
    return 0;
}


 
