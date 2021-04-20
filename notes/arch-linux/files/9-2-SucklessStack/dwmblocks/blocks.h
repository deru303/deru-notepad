//Modify this file to change what commands output to your statusbar, and recompile using the make command.
static const Block blocks[] = {
	/*Icon*/	/*Command*/		/*Update Interval*/	/*Update Signal*/
	{" ", "echo 'Artix Linux'", 120, 9},

	{"直 ", "$HOME/.local/bin/status-wifi.sh", 5, 9},

	{" ", "xbacklight -get | awk '{print int($1+0.5) \"%\"}'", 5, 9},

	{" ", "$HOME/.local/bin/status-battery.sh", 5, 9},

	{" ", "pamixer --get-volume | awk '{print $1\"%\"}'", 5, 9},

	{" ", "date '+%R'", 5, 9},

	{" ", "date '+%d.%m.%Y, %A'", 5, 9}
};

//sets delimeter between status commands. NULL character ('\0') means no delimeter.
static char delim[] = "      ";
static unsigned int delimLen = 6;
