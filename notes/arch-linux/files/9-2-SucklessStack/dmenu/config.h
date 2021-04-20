/* dmenu can by also configured in .Xresources file
dmenu.font : font or font set
dmenu.background : normal background color
dmenu.foreground : normal foreground color
dmenu.selbackground : selected background color
dmenu.selforeground : selected foreground color
*/

/* -b  option; if 0, dmenu appears at bottom     */
static int topbar = 1;                      

/* -fn option overrides fonts[0]; default X11 font or font set */
static char *fonts[] = {
	"sans-serif:size=12:antialias=true:autohint=true",
    "JoyPixels:pixelsize=12:antialias=true:autohint=true"
};

/* -p  option; prompt to the left of input field */
static char *prompt      = NULL;      

/* color scheme */
static char *colors[SchemeLast][2] = {
	/*     fg         bg       */
	[SchemeNorm] = { "#b2b2b2", "#111121" },
	[SchemeSel] = { "#dfdfdf", "#50536b" },
	[SchemeOut] = { "#dfdfdf", "#50536b" },
};

/* -l option; if nonzero, dmenu uses vertical list with given number of lines */
static unsigned int lines      = 15;

/* -h option; minimum height of a menu line */
static unsigned int lineheight = 35;
static unsigned int min_lineheight = 8;

/*
 * Characters not considered part of a word while deleting words
 * for example: " /?\"&[]"
 */
static char worddelimiters[] = " ";