# coding: utf-8
require 'rspec'
require 'appium_lib'

module Example
    def setup_driver
		return if $driver
		appium_txt  = File.expand_path(File.join(File.dirname(__FILE__), 'appium.txt'))
		@caps = Appium.load_appium_txt file: appium_txt, verbose: true
		Appium::Driver.new (@caps)
    end   
    def promote_appium_methods
        Appium.promote_appium_methods Example
    end
end

RSpec.configure do |config|
    config.include (Example)
	config.run_all_when_everything_filtered = true
	config.alias_it_should_behave_like_to :include_shared
	config.before (:suite) do
		setup_driver
		$driver.start_driver
        promote_appium_methods
	end

	config.before (:all) do
		set_wait (120)
	end

	config.after (:suite) do
		$driver.driver_quit
	end
end