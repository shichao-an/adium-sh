#!/usr/bin/osascript
# Query contact name with display name (alias)

on run argv
	tell application "Adium"
		set service_name to item 1 of argv
		set account_name to item 2 of argv
		set display_name to item 3 of argv
		set users to get every contact of account account_name of service service_name
		repeat with user in users
			set dname to (display name of user)
			do shell script "echo " & dname
			if (dname = display_name) then
				return name of user
				exit repeat
			end if
		end repeat
	end tell
end run
