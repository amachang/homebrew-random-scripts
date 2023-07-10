{% if droppable %}

on run
    tell application "Finder"
        do shell script "{{command}}" & space & quoted form of POSIX path of (insertion location as alias)
    end tell

end run

on open draggedItems
	repeat with theItem in draggedItems
		do shell script "{{command}}" & space & quoted form of POSIX path of theItem
	end repeat
end open

{% else %}

on run
    do shell script "{{command}}"
end run

{% endif %}
