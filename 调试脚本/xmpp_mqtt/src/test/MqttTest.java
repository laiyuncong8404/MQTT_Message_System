package test;

import java.util.Dictionary;
import org.eclipse.paho.client.mqttv3.*;
import org.eclipse.paho.client.mqttv3.persist.MemoryPersistence;

/**
 * ProjectName: test
 * FileName: MqttTest.java
 * PackageName: test.mqtt
 * Date: 2017-9-29下午5:34:00
 * Author: wolfe_yuan
 * Description: TODO
 * Copyright (c) 2017, wolfe_yuan@163.com All Rights Reserved.
 */
public class MqttTest {

	/**
	 * @param args
	 */
	private static MqttAsyncClient client = null;
	// private static String topic = "d/D3A80000361234512345DHDH/i";

	public static void main(String[] args) {
		String host = "tcp://mqtt.mymlsoft.com:1883";
		String clientId = "a:fa5940c1f3c543a7";
		String topic = "d/D3A80000361234512345DHDH/i";
		MqttConnectOptions options = null;

		try {
			client = new MqttAsyncClient(host, clientId,
					new MemoryPersistence());
			options = new MqttConnectOptions();
			// 设置超时时间 单位为秒
			options.setConnectionTimeout(10);
			// 设置会话心跳时间 单位为秒 服务器会每隔1.5*10秒的时间向客户端发送个消息判断客户端是否在线，
			// 但这个方法并没有重连的机制
			options.setKeepAliveInterval(10);
			// 设置自动重联
			//			options.setAutomaticReconnect(true);
			//			client.connect(options);
			options.setUserName("fa5940c1f3c543a7");
			options.setPassword("eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJ0YW8xLmppYW5nIiwidXNlciI6InRvdSJ9._yv05gR0dAFJeDoEPI8Wo5qB01Gf-cM8_M1SbdoV9jQ"
					.toCharArray());
			client.connect(options, "xmpp-app-to-device", new IMqttActionListener() {

				@Override
				public void onSuccess(IMqttToken arg0) {
					System.out.println("----------onSuccess");
					String device_sn = "D3A80000361234512345DHDH"; 
					String userid = "fa5940c1f3c543a7";
					String payload_msg = "{\"getTemperature\": {\"action\": \"INVOKE_SDK_FUNCTION\", \"functions\": " +
							"	[{\"ParameterList\": [], \"name\": \"getSyncAcStatus\"}]}}";
					byte[] palyload = new byte[1024];
					int count = 0;
					int length = userid.length();
					palyload[0] = ByteUtils.int2OneByte(length);
					count += 1;
					byte[] cid = userid.getBytes();
					System.arraycopy(cid, 0, palyload, count, cid.length);
					count += cid.length;
//					palyload[count] = ByteUtils.int2OneByte(1);
//					count += 1;
					byte[] msg = payload_msg.getBytes();
					System.arraycopy(msg, 0, palyload, count, msg.length);
					System.out.println("----->>>"
							+ ByteUtils.bytesToHexString(palyload));
					System.out.println("------------publish!");
					try {
						client.publish(topic, palyload, 0, true);
					} catch (MqttPersistenceException e) {
						e.printStackTrace();
					} catch (MqttException e) {
						// TODO Auto-generated catch block
						e.printStackTrace();
					}
				}
				@Override
				public void onFailure(IMqttToken arg0, Throwable arg1) {
					// TODO Auto-generated method stub
					System.out.println("----------onFailure");
				}
			});
			byte[] palyload = new byte[1024];
			int count = 0;
			palyload[0] = ByteUtils.int2OneByte(8);
			count += 1;
			byte[] cid = clientId.getBytes();
			System.out.println("cid：" + cid);
			
			System.arraycopy(cid, 0, palyload, count, cid.length);
			count += cid.length;
			byte[] msg = "test_send".getBytes();
			System.arraycopy(msg, 0, palyload, count, msg.length);
			Thread.sleep(5);
			//			client.publish(topic, palyload, 0, true);
			//			System.out.println("------------publish!");
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

}
