#!/bin/zsh

# Move some files & directories from ~ to somewhere else
export ZDOTDIR="$HOME/.config/zsh"

# Environment variables
export EDITOR="vim"
export TERMINAL="st"
export BROWSER="opera"
export TERM="rxvt-256color"
export PATH="/home/daniel/.local/bin:$PATH"

# Source ~/.config/user-dirs.dirs (if exists)
userdirs_file="$HOME/.config/user-dirs.dirs"
[ -f "$userdirs_file" ] && source "$userdirs_file"

# Source /etc/locale.conf (if exists)
locale_file="/etc/locale.conf"
[ -f "$locale_file" ] && source "$locale_file"

