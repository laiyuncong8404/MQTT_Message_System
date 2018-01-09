# encoding: utf-8
#请在手机通用设置->键盘里disable自动改正,否则可能导致输入错误
require_relative 'spec_helper'

msg_total = 10
topic_sub_iOS = "mqtt/iOS/#"

def pub_topic_by_python_script()
  Process.spawn ("python /Users/xiaoxue/Documents/SSC_长虹软服中心/项目文档/2017/UP平台二期-MQTT消息系统/调试脚本/iOS_pub.py")  #sub_topic_by_run_python_script
end

describe 'MQTT_iOS_Sub',:skip => false do
  it 'sub_topic_iOS' do

    wait { text_exact('Add Connection').click}
    puts '***** ele add_connection_btn found and clicked *****'
    sleep 3
    server_name = textfields('10.3.93.241')[0]
    puts '***** ele server_name found *****'
    host = textfields('10.3.93.241')[1]
    puts '***** ele host found *****'
    port = textfield_exact('1883')
    puts '***** ele port found *****'
    clean_session_switch = find_element(:class, 'XCUIElementTypeSwitch')
    puts '***** ele clean_session_switch found *****'
    connect_btn = buttons_exact('Connect')[0]
    puts '***** ele connect_btn found *****'
    sub_topic = textfields_exact('Topic')[0]
    puts '***** ele sub_topic found *****'
    qos_btn_0 = button_exact('0')
    qos_btn_1 = button_exact('1')
    qos_btn_2 = button_exact('2')
    puts '***** ele qos_lever_btn found *****'

    connect_btn.click
    sub_topic.click
    sub_topic.clear
    sub_topic.type topic_sub_iOS
    buttons_exact('Subscript')[0].click
    puts "***** ele Subscript found and clicked *****"

    pub_topic_by_python_script()
    sleep 40
    #测试Gestures方法
    degree_text = text_exact('15 Degree')
    puts '***** text found *****'
    swipe(direction:'down')
    # scroll(direction:'up', element:degree_text)
    puts '***** scroll action performed *****'


    expect(text_exact(msg_total.to_s + ' Degree').displayed?).to be_truthy
    expect(button_exact(topic_sub_iOS).displayed?).to be_truthy
  end
end
