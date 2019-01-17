# -*- coding: utf-8 -*-

# Omnitux - educational activities based upon multimedia elements
# Copyright (C) 2008 Olav_2 (olav.olav@yahoo.fr)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

import os, os.path, pygame, string

import common

# Omnitux version
version = "1.2.1"
release_file = "release"


namespace = "http://omnitux.sourceforge.net/xml/"


########################################################################
# Graphical user interface setup
# colors and setup of the graphical elements
box_color = (255,255,255)
text_color = (0,0,0)
text_color_grey = (150,150,150)

legend_text_colors = [(150, 0, 150), (0, 127, 240), (240, 0, 0), (0, 152, 20), (161, 79, 209), (219, 129, 55)]

box_alpha = 230

button_box_color = (195,195,250)

flag_outline_color = (95, 95, 95)
flag_outline_width = 1

# height used by an image inside a textbox (1 = all the height is used)
image_in_textbox_ratio = 0.9

line_color = (230, 50, 50)
line_alpha = 100

transparent_color = (10,10,10) # do not use this color !

activated_text_color = (0,0,205)

cursor_color = (255,100,100)

fonts_name = "FreeSansBold.ttf"

# the time to wait after a click on a button in the UI
button_clicked = 30


# an "infinite" number
infinite = 999999999


########################################################################
# game folders

data_folders = [os.path.join(u"..","data")]

# hack for mouse cursors
folder_data_not_unicode = os.path.join("..","data")

folder_icons = u"default/icons/"

folder_music = os.path.join(data_folders[0], u"default", u"music")
folder_fonts = os.path.join(data_folders[0], u"default", u"fonts")

if (os.name == "posix") :
	# Linux / Unix
	home_dir = os.path.join(os.getenv('HOME'), "omnitux")
elif ((os.name == "nt") and (os.getenv('USERPROFILE') != None)) :
	# MS Windows
	home_dir = os.path.join(os.getenv('USERPROFILE'), "omnitux")
	
else :
	home_dir = u".."

folder_log = os.path.join(home_dir, u"log")

log_file = os.path.join(folder_log,"omnitux.log")


# extensions
music_extensions = ["ogg"]

xml_extensions = ["xml"]

image_extensions = ["svg", "png", "jpg", "jpeg", "gif"]

########################################################################
# icons and pictures

main_menu_back = os.path.join(data_folders[0],u"default","backgrounds","GPN-2001-000009_modified.jpg")
main_menu_second_back = "default/backgrounds/iss007e16249.jpg"

omnitux_logo = os.path.join(data_folders[0],u"default",u"icons",u"Omnitux_logo.svg")
omnitux_logo_small = os.path.join(data_folders[0],u"default",u"icons",u"ico",u"Omnitux_logo_for_ico.png")

background_file = os.path.join(data_folders[0],u"default",u"backgrounds",u"map_background.jpg")

mouse_pointer = os.path.join(data_folders[0], u"default", u"mouse_pointers", u"main.svg")
mouse_pointer_drag = os.path.join(data_folders[0], u"default", u"mouse_pointers", u"poing.svg")
mouse_initial_pos = (-50, -50)
mouse_size = (10, 10)

# for small images, the maximum zoom factor
max_zoom = 3

icon_arrow_up = folder_icons + u"jean_victor_balin_arrow_orange_up.svg"
icon_arrow_down =  folder_icons + u"jean_victor_balin_arrow_orange_down.svg"

missing_image = folder_icons + u"missing_image.png"



########################################################################
# supported languages, sorted in alphabetical order
supported_languages = ["de", "en", "es", "fr", "it", "pl", "pt", "zh"]


# in case some label is not translated, fallback to this language
fallback_language = "en"

# max number of image refresh by second
framerate = 70

# number of frames before changing country flags
country_ticks_for_animation = 130

# amount of milliseconds before repeating a key event while the key is held down
key_repeat_delay = 100

# music volume (0 = mute, 1= max)
music_volume = 0.5

# sound buffer length
mixer_buffersize = 3*1024

# duration of fading out sounds
fadeout_sound_duration = 900

# end music event code
ENDMUSICEVENT = pygame.USEREVENT


yes_icon = "default/icons/yes.svg"
no_icon = "default/icons/no.svg"

stop_icon = "default/icons/exit.svg"
stop_icon_pos = (91, 0)
stop_icon_size = (9, 9)

go_next_icon = "default/icons/next.svg"
go_next_icon_pos = (91, 91)
go_next_icon_size = (9, 9)

# attempt to simplify the interface : back now equals exit (same icon, same position on top right)
go_left_icon = "default/icons/exit.svg"
go_left_icon_pos = (91, 0)
go_left_icon_size = (9, 9)


# arcade stuff

score_good_pos = (51, 1)
score_good_size = (9, 5)

score_good_icon = "default/icons/SM_1.svg"

score_good_icon_pos = (60, 1)
score_good_icon_size = (3, 5)


score_wrong_pos = (63, 1)
score_wrong_size = (9, 5)

score_wrong_icon = "default/icons/SM_2.svg"

score_wrong_icon_pos = (72, 1)
score_wrong_icon_size = (3, 5)


timer_pos = (75, 1)
timer_size = (9, 5)

timer_icon = "default/icons/Anonymous_Architetto_--_Clessidra.svg"

timer_icon_pos = (84, 1)
timer_icon_size = (3, 5)


default_music_files = [ "default/music/01 - 01 Varius (dans ma Savane).wav.ogg", 
			"default/music/02 - 02 Caravelius (l'eau c'est la vie).wav.ogg",
			"default/music/03 - 03 Africa 1 (le reve de la Mer).wav.ogg",
			"default/music/04 - 04 Ne Medohounkou (a GreAnDe).wav.ogg",
			"default/music/05 - 05 Gibus (le Singe).wav.ogg",
			"default/music/06 - 06 Africa 2 (les Enfants).wav.ogg"]


######################
# setup for main menu

tag_defs_filename = "tag_defs.xml"

igloo_icon = "default/awards/igloo.svg"

igloo_pos = (0,71)
igloo_size = (29,29)

main_flag_pos_y = 66
main_flag_size = (10, 5)

legend_text_pos = (0, 83)
legend_text_size = (100, 10)

# default difficulty icons

level_icons = {}

level_icons["1"] = "default/icons/level/1.svg"
level_icons["2"] = "default/icons/level/2.svg"
level_icons["3"] = "default/icons/level/3.svg"
level_icons["4"] = "default/icons/level/4.svg"


##################
# setup for igloo
igloo_background_file = "default/awards/snow.png"

igloo_file = "default/awards/johnny_automatic_igloo.svg"

folder_award_tuxes = "default/awards/tuxes/"


# initial topleft position of the tuxes which got out of the igloo (coordinates in igloo_file)
tux_initial_pos = (673, 208)

# height of tuxes (relative to igloo_file)
tux_height = 80

# speed of the tuxes going out of the igloo in pixels
tux_speed = 2

# x pos of the mast holding the flags (in pixels in original image)
flag_mast_pos_x_px = 33.5

######################
# setup for high score

highscore_background_file = "default/highscore/high_score.svg"

highscore_dir = os.path.join(home_dir, "highscores")

# only top 10 scores will be saved
max_highscores = 10

highscore_pos = (10, 10)
highscore_size = (80, 60)




##########################
# setup for user options 

user_options_filename = "user_settings.xml"


# options icon on main menu
options_icon_pos = (0.5 , 2)
options_icon_size = (8, 6)
options_icon_file = "default/options/purzen_A_cartoon_moon_rocket.svg"



#########################
# setup for background files by activity

background_file = {}
background_mode = {}

background_file['association'] = os.path.join(data_folders[0],u"default",u"backgrounds",u"Whimsy.JPG")
background_mode['association'] = "FILL"


####################
# setup for puzzles
puzzle_alpha = 150 # used for transparent images

background_file['puzzle'] = os.path.join(data_folders[0],u"default",u"backgrounds",u"Whimsy.JPG")
background_mode['puzzle'] = "FILL"


puzzle_tux_image = os.path.join(u"default", u"awards", u"tuxes", u"batux-tux-g1-hd-alpha.png")



########################
# setup for memory cards
memory_wait_time = 500 # waiting time when a tuple is found

background_file['memory_cards'] = os.path.join(data_folders[0],u"default",u"backgrounds",u"Whimsy.JPG")
background_mode['memory_cards'] = "FILL"

###########################
# setup for differences
background_file['differences'] = os.path.join(data_folders[0],u"default",u"backgrounds",u"dark_green.svg")
background_mode['differences'] = "FILL"


###########################
# setup for image transform
background_file['transform'] = os.path.join(data_folders[0],u"default",u"backgrounds",u"dark_green.svg")
background_mode['transform'] = "FILL"


#############################
# setup for learning activity
background_file['learning'] = os.path.join(data_folders[0],u"default",u"backgrounds",u"dark_green.svg")
background_mode['learning'] = "FILL"



#######################
# setup for display_big images
big_pos = (3, 2)
big_size = (94, 96)


#################
# setup for GTK+
hpad = 7
vpad = 15

UN_image_filename = "default/icons/flags/Flag_of_the_United_Nations.svg"


######################################
# Constant stuff which can be modified

if ("OMNITUX_DATA" in os.environ.keys()) :

	new_data_folder = os.environ["OMNITUX_DATA"]

	data_folders.append(new_data_folder)
