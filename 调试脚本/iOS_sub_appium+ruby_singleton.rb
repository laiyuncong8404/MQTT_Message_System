# encoding: utf-8
#请在手机通用设置->键盘里disable自动改正,否则可能导致输入错误
require 'rspec'
require 'appium_lib'

APP_PATH = File.expand_path(File.join(File.dirname(__FILE__),'/apps/com.changhong.emqx_debug.app'))

def pub_topic_by_python_script()
  Process.spawn ("python /Users/xiaoxue/Documents/SSC_长虹软服中心/项目文档/2017/UP平台二期-MQTT消息系统/调试脚本/iOS_pub.py")  #sub_topic_by_run_python_script
end

def desired_caps
  {
    caps: {
      app:              APP_PATH,
      noReset:          false,
      fullReset:        false,
      # webDriverAgentUrl:'http://localhost:8100',
      # newCommandTimeout:3600,
      platformName:     'iOS',
      platformVersion:  '10.3.1',
      deviceName:       'iPhone 6',
      udid:             '78973E12-B4CB-460E-A223-904AC41704B4',
      automationName:   'XCUITest',
    },
    appium_lib: {
      port: 4723,
      wait: 20,
      wait_interval: 1,
      wait_timeout: 120
    }
  }
end


Appium::Driver.new(desired_caps, true).start_driver
module Emqx
  module IOS
    Appium.promote_singleton_appium_methods Emqx
	topic_sub_iOS = "mqtt/iOS/#"

    wait { text_exact('Add Connection').click}
    puts '***** ele add_connection_btn found and clicked *****'
    sleep 3
    server_name = textfields('10.3.93.241')[0]
    puts '**** ele server_name found ****'
    host = textfields('10.3.93.241')[1]
    puts '***** ele host found *****'
    port = textfield_exact('1883')
    puts '***** ele port found *****'
    connect_btn = buttons_exact('Connect')[0]
    puts '***** ele connect_btn found *****'
    sub_topic = textfields_exact('Topic')[0]
    puts '***** ele sub_topic found *****'
    # qos_btn_0 = button_exact('0')
    # qos_btn_1 = button_exact('1')
    # qos_btn_2 = button_exact('2')

    connect_btn.click
    sub_topic.click
    sub_topic.clear
    sub_topic.type topic_sub_iOS
    buttons_exact('Subscript')[0].click
    puts "***** ele Subscript found and clicked *****"
    raise Exception unless ( exists { button_exact(topic_sub_iOS) } )
    pub_topic_by_python_script()
    sleep 40
    # 测试Gestures方法
    degree_text = text_exact('15 Degree')
    puts '***** text found *****'
    swipe(direction:'down')
    scroll(direction:'up', element:degree_text, to_visible:false)
    driver_quit
    puts 'test done succuss'
  end
end

