#History settings
export PROMPT_COMMAND='res=$?;history -a;cat ~/.bash_history|tail -2 >> ~/.command_history;echo -e "res:$res\tpwd:`pwd`\tdate:`date +%s`\t" >> ~/.command_history'
HISTTIMEFORMAT="%Y/%m/%dT%T%z "
HISTIGNORE='rm -rf ~/.bash_history:rm -rf ~/.command_history'