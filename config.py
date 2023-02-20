# Config file by:
#        ___   ___ ____
#       |__ \ / _ \___ \
#   __ _   ) | | | |__) |
#  / _` | / /| | | |__ <
# | (_| |/ /_| |_| |__) |
#  \__, |____|\___/____/
#   __/ |            ______
#  |___/            |______|

import os, subprocess
from libqtile import qtile, layout, widget, hook, bar
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.layout.xmonad import MonadTall
from libqtile.layout.max import Max
from libqtile.layout.floating import Floating
from qtile_extras import widget
from qtile_extras.widget.decorations import PowerLineDecoration
from colors import doom_one

# ------Keys----------------------------------------------------------------------------------------------------------------------------------

mod = "mod4"
terminal = "alacritty"

keys = [
    # Launch applications
    Key([mod, "control"], "f", lazy.spawn('brave'), desc="Launch browser"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "r", lazy.spawn('rofi -show run')),

    # Toggle floating and fullscreen
    Key([mod], "f", lazy.window.toggle_fullscreen(), desc="Toggle fullscreen mode"),
    Key([mod, "shift"], "space", lazy.window.toggle_floating(), desc="Toggle fullscreen mode"),

    # Keybindings for resizing windows in MonadTall layout
    Key([mod], "i", lazy.layout.grow()),
    Key([mod], "d", lazy.layout.shrink()),
    Key([mod], "n", lazy.layout.normalize()),
    Key([mod], "o", lazy.layout.maximize()),
    Key([mod, "control"], "space", lazy.layout.flip()),

    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
        # Grow windows. If current window is on the edge of screen and direction
        # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod, "shift"], "c", lazy.window.kill(), desc="Kill focused window"),

    Key([mod], "q", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "shift"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
]

# -----Groups---------------------------------------------------------------------------------------------------------------------------------

groups = [
    Group('1', label='󰈹', matches=[Match(wm_class='Brave')], layout='max'),
    Group('2', label='', matches=[Match(wm_class='Alacritty')], layout='monadtall'),
    Group('3', label='', matches=[Match(wm_class='neovide')], layout='monadtall'),
    Group('4', label='', matches=[Match(wm_class='Thunar, thunderbird, keepassxc')], layout='monadtall'),
    Group('5', label='󱅯', matches=[Match(wm_class='discord')], layout='monadtall'),
    Group('6', label='󰝚', matches=[Match(wm_class='Spotify')], layout='monadtall'),
]

for i in groups: 
    keys.extend([
        Key(
            [mod],
            i.name,
            lazy.group[i.name].toscreen(),
            desc="Switch to group {}".format(i.name),
        ),
        Key(
            [mod, "shift"],
            i.name,
            lazy.window.togroup(i.name, switch_group=True),
            desc="Switch to & move focused window to group {}".format(i.name),
        ),
    ])

# -----Layouts--------------------------------------------------------------------------------------------------------------------------------

layouts = [
    MonadTall(
        border_normal=doom_one['background'],
        border_focus=doom_one['second_fg'],
        margin=8,
        border_width=2,
        single_border_width=2,
        single_margin=8,
    ),
    Max(
        border_normal=doom_one['background'],
        border_focus=doom_one['second_fg'],
        border_width=2,
        margin=8,
    ),
]

floating_layout = Floating(
    border_normal=doom_one['background'],
    border_focus=doom_one['second_fg'],
    border_width=2,
    float_rules=[
        *Floating.default_float_rules,
        Match(wm_class='Blueberry'),
        Match(wm_class='pavucontrol'),
        Match(wm_class='zoom'),
        Match(wm_class='xarchiver'),
    ]
)

# ------Bar-----------------------------------------------------------------------------------------------------------------------------------

widget_defaults = dict(
    font="UbuntuMono Nerd Font",
    fontsize=12,
    padding=8,
    foreground=doom_one['foreground']
)

extension_defaults = widget_defaults.copy()

powerline = {
    "decorations": [
        PowerLineDecoration(path='rounded_left')
    ]
}

screens = [Screen(top=bar.Bar([
    widget.Spacer(
        length=8,
        decorations = [
            PowerLineDecoration(path='rounded_right')
        ],
    ),
    widget.Image(
        filename='~/.config/qtile/mgdoom.png',
        background=doom_one['base0'],
        margin=1,
        decorations = [
            PowerLineDecoration(path='rounded_left')
        ],
    ),
    widget.Spacer(
        length=8,
        decorations = [
            PowerLineDecoration(path='rounded_right')
        ]
    ),
    widget.AnalogueClock(
        second_size=1,
        background=doom_one['base0'],
        padding=0,
        decorations = [
            PowerLineDecoration(path='rounded_left'),
        ],
    ),
    widget.WindowName(
        fontsize=9,
        font='FiraCode Nerd Font',
        fmt='~/{}',
        max_chars=75,
        foreground=doom_one['base8']
    ),
    widget.Spacer(
        length=8,
        decorations = [
            PowerLineDecoration(
                path='rounded_right'
            )
        ]
    ),
    widget.GroupBox(
        fontsize=15,
        font='FiraCode Nerd Font',
        active=doom_one['base7'],
        inactive=doom_one['base4'],
        background=doom_one['base0'],
        disable_drag=True,
        borderwidth=0,
        highlight_method='line',
        highlight_color=doom_one['base0'],
        block_highlight_text_color=doom_one['foreground'],
        decorations = [
            PowerLineDecoration(path='rounded_left')
        ]
    ),
    widget.Spacer(),
    widget.Spacer(
        size=0,
        decorations = [
            PowerLineDecoration(path='rounded_right')
        ]
    ),
    widget.CheckUpdates(
        font='FiraCode Nerd Font',
        background=doom_one['base0'],
        distro='Arch_checkupdates',
        display_format=' {updates}',
        no_update_string=' 0',
        mouse_callbacks={'Button1': lambda: qtile.cmd_spawn('alacritty' + ' -e sudo pacman -Syu')},
        colour_have_updates=doom_one['foreground'],
        colour_no_updates=doom_one['foreground'],
        padding=0,
        decorations = [
            PowerLineDecoration(path='rounded_left')
        ]
    ),
    widget.Spacer(
        length=8,
        decorations = [
            PowerLineDecoration(path='rounded_right')
        ]
    ),
    widget.Clock(
        font='FiraCode Nerd Font',
        format="%Y/%m/%d",
        foreground=doom_one['foreground'],
        padding=0,
        background=doom_one['base0'],
        decorations = [
            PowerLineDecoration(path='rounded_left')
        ]
    ),
    widget.Spacer(
        length=8,
        decorations = [
            PowerLineDecoration(path='rounded_right')
        ]
    ),
    widget.UPowerWidget(
        border_colour=doom_one['base6'],
        border_charge_colour=doom_one['base7'],
        background=doom_one['base0'],
        decorations = [
            PowerLineDecoration(path='rounded_left')
        ]
    ),
    widget.Spacer(
        length=8
    )
    ],
    background='#00000000', size=24, margin=0,
))]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

@ hook.subscribe.startup_once
def autostart():
    home=os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.run([home])

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = True
wl_input_rules = None
wmname = "LG3D"
