# coding: utf-8
require 'rspec'
require 'appium_lib'

APP_PATH = File.expand_path(File.join(File.dirname(__FILE__), '..', '/apps/com.changhong.emqx_debug.app'))

def desired_caps
  {
    caps: {
      app:              APP_PATH,
      noReset:          false,
      fullReset:        false,
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
      wait_timeout: 60
    }
  }
end

def setup_driver
	return if $driver
	Appium::Driver.new(desired_caps, true)
end

# def setup_driver
# 	return if $driver
# 	appium_txt  = File.expand_path(File.join(File.dirname(__FILE__), 'appium.txt'))
# 	@caps = Appium.load_appium_txt file: appium_txt, verbose: true
# 	Appium::Driver.new (@caps)
# end

def promote_methods
    # Appium.promote_appium_methods RSpec
	# Appium.promote_appium_methods Object
	 Appium.promote_appium_methods RSpec::Core::ExampleGroup
end


RSpec.configure do |config|
	config.run_all_when_everything_filtered = true
	config.alias_it_should_behave_like_to :include_shared
	# config.include Appium::Ios

	config.before (:suite) do
		setup_driver
		$driver.start_driver
		promote_methods
	end

	 config.before (:all) do
	 	set_wait (120)
	 end

	config.after (:suite) do
		$driver.driver_quit
	end
end
