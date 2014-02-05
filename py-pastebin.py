#!/usr/bin/env python
#
# File:				pastebin.py
# Author:			Pavel Pinkava <pin2k.cz@gmail.com>
# Version:			1.0
# Last Modification:		04/02/2014
# Description:			This simple python script will upload 
#				content of the file to pastebin.com
#				and returns url generated by pastebin.com
# 
# This script has been written for my education purposes.
#

import urllib
import sys
import getopt

# Script Settings
#
# Needs to add API_DEV_KEY or API_USER_KEY
API_DEV_KEY = "739e47b14723a3ae0ab898b859121d32"
API_USER_KEY = ""

# Default values for expiration and syntax
# Expiration: [N]ever, [1H]our, [1D]ay, [1W]eek, [2W]eeks, [1M]onth
# Syntax: autoconf, cmake, php, python, perl, c, cpp, html5, etc...
default_expiration = "1M"
default_syntax = "text"

# Global variables
params = {}

def insert_code(filename):
	
	"Insert content of file as one of parameter."
	
	try:
		with open(filename, 'r') as content:
			file_content = content.read()
		return file_content
	except IOError:
		print "Error: File doesn't exist"
		sys.exit(2)

def send_request(file_content):
	
	"Set params and send them to pastebin api php script via urllib"

	params['api_dev_key'] = API_DEV_KEY
	params['api_paste_private'] = "0"
	params['api_user_key'] = API_USER_KEY
	params['api_paste_code'] = insert_code(file_content)
	params['api_option'] = "paste"
	params['api_paste_format'] = "text"
	params['api_paste_expire_date'] = "1M"
	
	try:
	
		response = urllib.urlopen('http://pastebin.com/api/api_post.php', urllib.urlencode(params))
		url = response.read()
		return url
	except KeyboardInterrupt:
		print "Application interrupted by keyboard"
		sys.exit(0)

def usage():
	
	"Print usage of the script (help)"
	
	print "Pastebin file content uploader, version 0.1"
	print "Pavel Pinkava <pin2k.cz@gmail.com>"
	print "Usage: " +sys.argv[0]+ " -f <file>\n"
	print "\t-f,--file\tRead content of given file"
	print "\t-e,--expire\tSet up the expiration date (read manual for more options)"
	print "\t-n,--name\tSet up document name for pastebin"
	print "\t-s,--syntax\tSet up syntax for file content (php,bash -- see manual)"
	sys.exit(2)

# Function: main(argv)
#
# Main function gets params and parse them with getopt parser

def main(argv):
	
	"Main function gets arguments, parse them via getopt"

	try:
		opts,args = getopt.getopt(argv, 'f:e:n:s:h', ['file=','expire=','name=','syntax=','help'])
	except getopt.GetoptError:
		usage()
	
	for opt, arg in opts:
		if opt in ('-h', '--help'):
			usage()

		if opt in ('-f', '--file'):
			filename = arg
		else:
			usage()

		if opt in ('-e', '--expire'):
			expiration = arg
		else:
			expiration = default_expiration

		if opt in ('-s', '--syntax'):
			syntax = arg
		else:
			syntax = default_syntax

		if opt in ('-n', '--name'):
			name = arg
		else:
			name = "Untitled"

	url = send_request(filename)
	print url

if __name__ == "__main__":
	
	"Execute application"

	main(sys.argv[1:])

