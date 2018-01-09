# encoding: utf-8
#请在手机通用设置->键盘里disable自动改正,否则可能导致输入错误
require_relative 'spec_helper'

msg_total = 10

# 生成len长度的字符串
def newpass(len)
  chars = ("a".."z").to_a + ("A".."Z").to_a + ("0".."9").to_a
  newpass = ""
  1.upto(len) { |i| newpass << chars[rand(chars.size-1)] }
  return newpass
end

def sub_topic_by_python_script()
  Process.spawn ("python /Users/xiaoxue/Documents/SSC_长虹软服中心/项目文档/2017/UP平台二期-MQTT消息系统/调试脚本/iOS_sub.py")  #sub_topic_by_run_python_script
end

describe 'MQTT_iOS_Pub',:skip => false do
  it 'pub_topic_iOS' do
    wait { text_exact('Add Connection').click}
    sleep 3
    puts '***** ele add_connection_btn found and clicked *****'
    connect_btn = buttons_exact('Connect')[0]
    puts '***** ele connect_btn found *****'
    sub_topic = textfields_exact('Topic')[0]
    puts '***** ele sub_topic found *****'
    qos_btn_0 = button_exact('0')
    qos_btn_1 = button_exact('1')
    qos_btn_2 = button_exact('2')
    puts '***** ele qos_lever_btn found *****'

    connect_btn.click
    sleep 3
    puts '***** ele connect_btn clicked *****'
    disconect_btn = button_exact('Disconnect')
    wait { disconect_btn }
    puts '***** MQTT broker connected *****'

    # switch to publish frame
    tap(x:200,y:400)

    qos_btn_0 = button_exact('0')
    qos_btn_1 = button_exact('1')
    qos_btn_2 = button_exact('2')
    puts '***** ele qos_lever_btn found *****'
    pub_topic_btn = button_exact('topic')
    puts '***** ele pub_topic_btn found *****'
    pub_msg = textfields[0]
    puts '***** ele pub_msg found *****'
    pub_btn = button_exact('Publish')
    puts '***** ele pub_btn found *****'

    sub_topic_by_python_script()
    sleep 3

    msg_count = 1
    while msg_count <= msg_total do
        topic_pub_iOS = "mqtt/iOS/pub/" + newpass(4)
        msg_pub_iOS = msg_count.to_s + " Degree"

        pub_topic_btn.click
        pub_topic_text = textfields[-1]
        pub_topic_text.clear
        pub_topic_text.type topic_pub_iOS
        puts '***** pub_topic modify *****'
        alert(action:"accept")
        puts '***** alert accept *****'
        # 经测试,采用以下两种方法定位pub_msg输入框,都会导致无法输入,原因不明???
        # last_ele('XCUIElementTypeTextField')
        # 或者
        # eles = find_elements(:class_name, 'XCUIElementTypeTextField')
        # pub_msg = eles[eles.size - 1]

        # Important
        # 以下两行代码如果删除,将导致pub_msg不会输入,原因不明???
        page_class
        puts page(class_name='XCUIElementTypeTextField')

        # pub_msg.click
        pub_msg.clear
        puts '***** ele pub_msg clear *****'
        pub_msg.type msg_pub_iOS
        puts '***** ele pub_msg typed *****'
        expect(pub_msg.text == msg_pub_iOS).to be_truthy
        pub_btn.click
        puts '***** pub_btn clicked *****'

        msg_count +=1
      end
    end
  end
