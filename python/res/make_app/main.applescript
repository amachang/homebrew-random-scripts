on run
    do shell script "{{command}}"
end run

on open draggedItems
	repeat with theItem in draggedItems
		do shell script "{{command}}" & space & quoted form of POSIX path of theItem
	end repeat
end open

