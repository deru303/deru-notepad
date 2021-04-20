/* fonts */
static char font[]			 = "monospace:size=10";
static char fontsymbols[]    = "Symbols Nerd Font:size=10";
static char *fonts[]   = { font, fontsymbols };

/* wm appearance */
static unsigned int borderpx   = 1;    		    /* border pixel of windows */
static unsigned int snap       = 0;   		    /* snap pixel */
static int showbar             = 1;    		    /* 0 means no bar */
static int topbar              = 1;    		    /* 0 means bottom bar */
static int horizpadbar   = 2;        		/* horizontal padding for statusbar */
static int vertpadbar    = 5;        		/* vertical padding for statusbar */

/* swallowing */
static int swallowfloating    = 0;        /* 1 means swallow floating windows by default */

/* gaps */
static int smartgaps          = 0;        /* 1 means no outer gap when there is only one window */
static unsigned int gappih    = 10;       /* horiz inner gap between windows */
static unsigned int gappiv    = 10;       /* vert inner gap between windows */
static unsigned int gappoh    = 10;       /* horiz outer gap between windows and screen edge */
static unsigned int gappov    = 10;       /* vert outer gap between windows and screen edge */

/* colors */
static char normbgcolor[]           = "#222222";
static char normbordercolor[]       = "#444444";
static char normfgcolor[]           = "#bbbbbb";
static char selfgcolor[]            = "#eeeeee";
static char selbordercolor[]        = "#005577";
static char selbgcolor[]            = "#005577";
static char *colors[][3] = {
       /*               fg           bg           border   */
       [SchemeNorm] = { normfgcolor, normbgcolor, normbordercolor },
       [SchemeSel]  = { selfgcolor,  selbgcolor,  selbordercolor  },
};

/* tagging */
static const char *tags[] = { "1", "2", "3", "4", "5", "6", "7", "8", "9" };

/* specific window rules */
static const Rule rules[] = {
	/* xprop(1):
	 *	WM_CLASS(STRING) = instance, class
	 *	WM_NAME(STRING) = title
	 */
	/* class     instance  title           tags mask  isfloating  isterminal  noswallow  monitor */
	{ "Firefox", NULL,     NULL,           1 << 8,    0,          0,          -1,        -1 },
	{ "St",      NULL,     NULL,           0,         0,          1,           0,        -1 },
	{ NULL,      NULL,     "Event Tester", 0,         0,          0,           1,        -1 }, /* xev */
};

/* layout(s) */
static float mfact     = 0.55; /* factor of master area size [0.05..0.95] */
static int nmaster     = 1;    /* number of clients in master area */
static int resizehints = 0;    /* 1 means respect size hints in tiled resizals */

#define FORCE_VSPLIT 1  /* nrowgrid layout: force two clients to always split vertically */
#include "vanitygaps.c"

static const Layout layouts[] = {
	/* symbol     arrange function */
	{ "[]=",      tile },    /* first entry is default */
	{ "><>",      NULL },    /* no layout function means floating behavior */
	{ "[M]",      monocle },
	{ "|M|",      centeredmaster },
	{ ">M>",      centeredfloatingmaster },
};

/* key definitions */
#define MODKEY Mod4Mask
#define ALT Mod1Mask
#define TAGKEYS(KEY,TAG) \
	{ MODKEY,                       KEY,      view,           {.ui = 1 << TAG} }, \
	{ MODKEY|ControlMask,           KEY,      toggleview,     {.ui = 1 << TAG} }, \
	{ MODKEY|ShiftMask,             KEY,      tag,            {.ui = 1 << TAG} }, \
	{ MODKEY|ControlMask|ShiftMask, KEY,      toggletag,      {.ui = 1 << TAG} },
#define STACKKEYS(MOD,ACTION) \
	{ MOD, XK_j,     ACTION##stack, {.i = INC(+1) } }, \
	{ MOD, XK_k,     ACTION##stack, {.i = INC(-1) } }, \
	{ MOD, XK_v,     ACTION##stack, {.i = 0 } }, \

/* helper for spawning shell commands in the pre dwm-5.0 fashion */
#define SHCMD(cmd) { .v = (const char*[]){ "/bin/sh", "-c", cmd, NULL } }

/* commands */
static const char *termcmd[]  	    = { "st", NULL };
static const char scratchpadname[]  = "scratchpad";
static const char *scratchpadcmd[]  = { "st", "-t", scratchpadname, "-g", "120x25", NULL };

/* Xresources entries binding */
ResourcePref resources[] = {
		{ "normfgcolor",		STRING,	&normfgcolor },
		{ "normbgcolor",		STRING,	&normbgcolor },
		{ "normbordercolor",	STRING,	&normbordercolor },
		{ "selfgcolor",			STRING,	&selfgcolor },
		{ "selbgcolor",			STRING,	&selbgcolor },
		{ "selbordercolor",		STRING,	&selbordercolor },

		{ "font",               STRING, &font },
		{ "fontsymbols",        STRING, &fontsymbols },

		{ "borderpx",			INTEGER, &borderpx },
		{ "snap",				INTEGER, &snap },
		{ "showbar",			INTEGER, &showbar },
		{ "topbar",				INTEGER, &topbar },
		{ "nmaster",			INTEGER, &nmaster },
		{ "resizehints",		INTEGER, &resizehints },
		{ "mfact",				FLOAT,	&mfact },

		{ "gappih",				INTEGER, &gappih },
		{ "gappiv",				INTEGER, &gappiv },
		{ "gappoh",				INTEGER, &gappoh },
		{ "gappov",				INTEGER, &gappov },

		{ "swallowfloating",	INTEGER, &swallowfloating },
};

/* key bindings */
static Key keys[] = {
	/* modifier                     key        function        argument */
    { MODKEY,                       XK_period, spawn,          SHCMD("$HOME/.local/bin/rofi-emoji.sh") },
    { ShiftMask,                    XK_F4,     spawn,          SHCMD("$HOME/.local/bin/rofi-powermenu.sh") },
    { MODKEY,                       XK_d,      spawn,          SHCMD("rofi -show run") },
    { MODKEY,                       XK_e,      spawn,          SHCMD("rofi -modi drun -show drun -show-icons -drun-display-format '{name}'") },
    { MODKEY,                       XK_Return, spawn,          SHCMD("st") },
    { MODKEY,                       XK_Print,  spawn,          SHCMD("$HOME/.local/bin/rofi-screenshot.sh") },
    { MODKEY,                       XK_o,      spawn,          SHCMD("pactl set-sink-volume @DEFAULT_SINK@ -5% && kill -43 $(pidof dwmblocks)") },
    { MODKEY,                       XK_p,      spawn,          SHCMD("pactl set-sink-volume @DEFAULT_SINK@ +5% && kill -43 $(pidof dwmblocks)") },
    { MODKEY|ShiftMask,             XK_o,      spawn,          SHCMD("pactl set-sink-volume @DEFAULT_SINK@ 0% && kill -43 $(pidof dwmblocks)") },
    { MODKEY|ShiftMask,             XK_p,      spawn,          SHCMD("pactl set-sink-volume @DEFAULT_SINK@ 100% && kill -43 $(pidof dwmblocks)") },
    { MODKEY,                       XK_u,      spawn,          SHCMD("xbacklight -dec 3 && pkill -RTMIN+9 dwmblocks") },
    { MODKEY,                       XK_i,      spawn,          SHCMD("xbacklight -inc 3 && pkill -RTMIN+9 dwmblocks") },
    { MODKEY|ShiftMask,             XK_u,      spawn,          SHCMD("xbacklight -set 1 && pkill -RTMIN+9 dwmblocks") },
    { MODKEY|ShiftMask,             XK_i,      spawn,          SHCMD("xbacklight -set 100 && pkill -RTMIN+8 dwmblocks") },
    { ALT|ShiftMask,           	    XK_F4,     spawn,          SHCMD("wmctrl -lp | awk '{print $3}' | xargs kill") }, //kill all windows

    { MODKEY,                       XK_space,  setlayout,      {.v = &layouts[0]} }, //tile
    { MODKEY,                       XK_c,      setlayout,      {.v = &layouts[3]} }, //centered master

	{ MODKEY,                       XK_h,      setmfact,       {.f = -0.05} }, //make master smaller
	{ MODKEY,                       XK_l,      setmfact,       {.f = +0.05} }, //make master bigger
    
    { MODKEY,                       XK_semicolon, zoom,        {0} }, //"promote" window to master

    { MODKEY,                       XK_grave,  togglescratch,  {.v = scratchpadcmd } },
	{ MODKEY,                       XK_b,      togglebar,      {0} },
	STACKKEYS(MODKEY,                          focus)
	STACKKEYS(MODKEY|ShiftMask,                push)
	{ MODKEY,                       XK_Tab,    view,           {0} },
	{ MODKEY,                       XK_s,      togglesticky,   {0} },
	{ MODKEY,                       XK_q,      killclient,     {0} },
	{ ALT,                          XK_F4,     killclient,     {0} },
	{ MODKEY|ShiftMask,             XK_space,  togglefloating, {0} },
	{ MODKEY,                       XK_f,      togglefullscr,  {0} },
	{ MODKEY,                       XK_0,      view,           {.ui = ~0 } },
	{ MODKEY|ShiftMask,             XK_0,      tag,            {.ui = ~0 } },
	TAGKEYS(                        XK_1,                      0)
	TAGKEYS(                        XK_2,                      1)
	TAGKEYS(                        XK_3,                      2)
	TAGKEYS(                        XK_4,                      3)
	TAGKEYS(                        XK_5,                      4)
	TAGKEYS(                        XK_6,                      5)
	TAGKEYS(                        XK_7,                      6)
	TAGKEYS(                        XK_8,                      7)
	TAGKEYS(                        XK_9,                      8)
};

/* button definitions */
/* click can be ClkTagBar, ClkLtSymbol, ClkStatusText, ClkWinTitle, ClkClientWin, or ClkRootWin */
static Button buttons[] = {
	/* click                event mask      button          function        argument */
	{ ClkLtSymbol,          0,              Button1,        setlayout,      {0} },
	{ ClkLtSymbol,          0,              Button3,        setlayout,      {.v = &layouts[2]} },
	{ ClkStatusText,        0,              Button2,        spawn,          {.v = termcmd } },
	{ ClkClientWin,         MODKEY,         Button1,        movemouse,      {0} },
	{ ClkClientWin,         MODKEY,         Button2,        togglefloating, {0} },
	{ ClkClientWin,         MODKEY,         Button3,        resizemouse,    {0} },
	{ ClkTagBar,            0,              Button1,        view,           {0} },
	{ ClkTagBar,            0,              Button3,        toggleview,     {0} },
	{ ClkTagBar,            MODKEY,         Button1,        tag,            {0} },
	{ ClkTagBar,            MODKEY,         Button3,        toggletag,      {0} },
};

