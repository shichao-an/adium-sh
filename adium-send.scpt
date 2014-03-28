#!/usr/bin/osascript

on run argv
	tell application "Adium"
		set buddy to item 1 of argv
		set user to get contact buddy
		if not (exists (chats whose contacts contains user)) then
			if not (exists (first chat window)) then
				tell account of user
					set new_chat to make new chat with contacts {user} with new chat window
				end tell
			else
				set existing_window to first chat window
				tell account of user
					set new_chat to make new chat with contacts {user} in window existing_window
				end tell
			end if
		else
			set new_chat to first chat whose contacts contains user
		end if
			send new_chat message item 2 of argv
	end tell
end run
