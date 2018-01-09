# encoding: utf-8

require 'rspec'
require 'appium_lib'

APP_PATH = File.expand_path(File.join(File.dirname(__FILE__),'/apps/EMQ-sample-debug-79ChangHongTester02.apk'))

topic_sub_android = "mqtt/Android/#"
topic_pub_android = "mqtt/Android/"
msg_total = 10

def newpass( len )
  chars = ("a".."z").to_a + ("A".."Z").to_a + ("0".."9").to_a
  newpass = ""
  1.upto(len) { |i| newpass << chars[rand(chars.size-1)] }
  return newpass
end

def pub_topic_by_python_script()
  system ("python /Users/xiaoxue/Documents/SSC_长虹软服中心/项目文档/2017/UP平台二期-MQTT消息系统/调试脚本/Android_pub.py")	#pub_topic_by_run_python_script
end

def desired_caps
  {
    caps: {
      app:               APP_PATH,
      appActivity:      '.MainActivity',
      appPackage:       'io.emqtt.sample',
      platformName:     'android',
      # deviceName:       '353BCJJYKXXF',#MeiZu MX真机
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

  it 'sub_topic' do
    subscribe_item = find_element(:id, 'io.emqtt.sample:id/navigation_dashboard')
    subscribe_item.click
    sub_topic = find_element(:class_name, 'android.widget.EditText')
    sub_topic.clear
    sub_topic.type topic_sub_android
    sub_btn = find_element(:id, 'io.emqtt.sample:id/subscribe_btn')
    sub_btn.click
    expect(sub_topic.text == topic_sub_android).to be true
  end

  it 'message_check' do
    text('Message').click
    set_wait (1)

    pub_topic_by_python_script()

    msgs = find_elements(:class_name, 'android.widget.TextView')
    for i in msgs
      puts i.text
    end

    expect(text(topic_pub_android).displayed?).to be true
    expect(text_exact('10 Degree').displayed?).to be true

    # methods for MeiZu MX
    # expect(msgs[4].text).to start_with(topic_pub_android)
    # expect(msgs[6].text == "100 Degree").to be true
    # find_element(:id, 'com.android.systemui:id/dismiss_btn').click
    #
  end
end
