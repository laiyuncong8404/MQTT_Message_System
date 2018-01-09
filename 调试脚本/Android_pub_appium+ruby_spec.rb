# encoding: utf-8

require 'rspec'
require 'appium_lib'

APP_PATH = File.expand_path(File.join(File.dirname(__FILE__),'/apps/EMQ-sample-debug-79ChangHongTester01.apk'))

topic_sub_android = "mqtt/Android/#"
msg_total = 20
# 生成len长度的字符串
def newpass(len)
  chars = ("a".."z").to_a + ("A".."Z").to_a + ("0".."9").to_a
  newpass = ""
  1.upto(len) { |i| newpass << chars[rand(chars.size-1)] }
  return newpass
end

def sub_topic_by_python_script()
  Process.spawn ("python /Users/xiaoxue/Documents/SSC_长虹软服中心/项目文档/2017/UP平台二期-MQTT消息系统/调试脚本/Android_sub.py")	#sub_topic_by_run_python_script
end


def desired_caps
  {
    caps: {
      app:               APP_PATH,
      appActivity:      '.MainActivity',
      appPackage:       'io.emqtt.sample',
      platformName:     'android',
      # deviceName:       '274b3f06',#MI 3真机
      deviceName:        'AVD_Nexus5', 
      avd:               'AVD_Nexus5',
      noSign:           true, #Skip checking and signing of app with debug keys
      noReset:          false,
      fullReset:        false, 
      unicodeKeyboard:  true,
      resetKeyboard:    true

    },
    appium_lib: {
      port: 4723,
      wait: 20,
      wait_interval: 1,
      wait_timeout: 60
    }
  }
end

describe 'EMQTT' do
  before(:all) do
    @driver = Appium::Driver.new(desired_caps, true).start_driver
    Appium.promote_appium_methods RSpec::Core::ExampleGroup
  end
  after(:all) do
    @driver_quit
  end
 
  it 'pub_topic' do
    pub_item = find_element(:id, 'io.emqtt.sample:id/navigation_notifications')
    pub_item.click
    pub_topic = find_element(:id, 'io.emqtt.sample:id/topic')
    pub_msg = find_element(:id, 'io.emqtt.sample:id/message')
    pub_btn = find_element(:id, 'io.emqtt.sample:id/subscribe_btn')

    sub_topic_by_python_script()

    msg_count = 1
    while msg_count <= msg_total do
        topic_pub_android = "mqtt/Android/pub/" + newpass(4)
        msg_pub_android = msg_count.to_s + " Degree"

        pub_topic.click
        pub_topic.clear
        pub_topic.type topic_pub_android

        pub_msg.click
        pub_msg.clear
        pub_msg.type msg_pub_android
        pub_btn.click

        msg_count +=1
        expect(pub_msg.text == msg_pub_android).to be true
      end
    end
  end
