# encoding: utf-8
require 'rspec'
require 'pp'
require 'fileutils'


testCases = Dir.glob("../spec/**/*_spec.rb")
# puts testCases
# puts "-"*100

# reports in separate files

# for i in testCases
# 	caseFile = ([i].to_s.split('/')[-1]).to_s[0..-11]
# 	puts "Now run caseFile " + caseFile + "_spec.rb"
# 	caseName = []
# 	for j in (0..testCases.length-1)
# 		newTestCase = (testCases[j].split('/')[-1]).to_s #只取spec文件的完整文件名
# 		caseName[j] = newTestCase[0..-9] #只取spec的文件名
# 		if caseFile == caseName[j] #只运行case文件名和报告文件名一致的用例
# 			system "rspec -f h #{i} > Reports/#{caseName[j]}_#{Time.now.strftime("%Y%m%d_%H%M%S")}.html"
# 		end
# 	end
# end
reports_path = File.join(File.dirname(__FILE__), "Reports")
FileUtils.mkdir_p reports_path if not File.exist? reports_path

# Seprate report

for i in testCases
	caseFile = ([i].to_s.split('/')[-1]).to_s[0..-11]
	puts "Now run caseFile " + i
	system "rspec -f h #{i} > Reports/#{caseFile}_#{Time.now.strftime("%Y%m%d_%H%M%S")}.html"
end


# All in one report file

# system "rspec -f html > Reports/#{Time.now.strftime("%Y%m%d_%H%M%S")}.html"
