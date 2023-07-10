{% if droppable %}

on run
    tell application "Finder"
        set currentDir to POSIX path of (insertion location as alias)
        my execCommand("{{command}}" & space & quoted form of currentDir, currentDir)
    end tell
end run

on open draggedItems
    tell application "Finder"
        repeat with theItem in draggedItems
            set currentDir to POSIX path of (insertion location as alias)
            my execCommand("{{command}}" & space & quoted form of POSIX path of theItem, currentDir)
        end repeat
    end tell
end open

{% else %}

on run
    tell application "Finder"
        set currentDir to POSIX path of (insertion location as alias)
        my execCommand("{{command}}", currentDir)
    end tell
end run

{% endif %}

on execCommand(command, currentDir)
    set zshCommand to "source ~/.zshrc ; cd" & space & quoted form of currentDir & ";" & command
    do shell script "/bin/zsh -c" & space & quoted form of zshCommand
end execCommmand

