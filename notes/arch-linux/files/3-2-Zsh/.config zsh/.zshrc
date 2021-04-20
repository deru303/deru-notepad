# Enable colors and change prompt:
autoload -U colors && colors
PS1="%{$fg[blue]%}%B%n@%m %b%. \$ "

# Disable beep
unsetopt beep

# Some utilities
setopt autocd		# Automatically cd into typed directory.
stty stop undef		# Disable ctrl-s to freeze terminal.
setopt interactive_comments

# History in cache directory:
HISTSIZE=5000
SAVEHIST=5000
HISTFILE=~/.cache/zsh/history
HISTDUP=erase            # Erase duplicates in the history file
setopt appendhistory     # Append history to the history file (no overwriting)
setopt sharehistory      # Share history across terminals
setopt incappendhistory  # Immediately append to the history file, not just when a term is killed

# Aliases
alias_file="$HOME/.config/shell/aliasrc"
[ -f "$alias_file" ] && source "$alias_file"

# Basic auto/tab complete:
autoload -U compinit
zstyle ':completion:*' menu select
zmodload zsh/complist
compinit
_comp_options+=(globdots)		# Include hidden files.
zstyle ':completion:*' insert-tab false

# Vim keybinding
bindkey -M menuselect 'h' vi-backward-char
bindkey -M menuselect 'k' vi-up-line-or-history
bindkey -M menuselect 'l' vi-forward-char
bindkey -M menuselect 'j' vi-down-line-or-history
bindkey -v '^?' backward-delete-char

# Custom prompts for root and ssh
if [ "$EUID" -eq "0" ]; then
    PS1="%{$fg[red]%}%B%n@%m %b%. # "
elif [ -n "$SSH_CLIENT" ] || [ -n "$SSH_TTY" ]; then
    PS1="%{$fg[green]%}%B%n@%m %b%. \$ "
fi

# Remove mode switching delay.
KEYTIMEOUT=5

# Change cursor shape for different vi modes.
function zle-keymap-select {
  if [[ ${KEYMAP} == vicmd ]] ||
     [[ $1 = 'block' ]]; then
    echo -ne '\e[1 q'

  elif [[ ${KEYMAP} == main ]] ||
       [[ ${KEYMAP} == viins ]] ||
       [[ ${KEYMAP} = '' ]] ||
       [[ $1 = 'beam' ]]; then
    echo -ne '\e[5 q'
  fi
}
zle -N zle-keymap-select

_fix_cursor() {
   echo -ne '\e[5 q'
}

precmd_functions+=(_fix_cursor)

# Fix delete key
bindkey "^[[3~" delete-char
