#!/usr/bin/osascript

on run argv
	tell application "Adium"
		set account_name to item 1 of argv as string
		set display_name to item 2 of argv
		set users to get every contact of account account_name
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
