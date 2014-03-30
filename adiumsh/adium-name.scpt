#!/usr/bin/osascript
# Query contact name with display name (alias)

on run argv
	tell application "Adium"
		set service_name to item 1 of argv
		set account_name to item 2 of argv
		set display_name to item 3 of argv
		set users to get every contact of account account_name of service service_name
		return (name of first contact whose display name is display_name) of account account_name of service service_name
	end tell
end run
