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

import pygame
from pygame.locals import *
			
import ui, constants, common


class Page_display_big(ui.Page) :

	def __init__(self, globalvars, text, image_file, associated_sounds) :
		self.text = text
		self.image_file = image_file
		self.associated_sounds = associated_sounds

		ui.Page.__init__(self, globalvars, None)


	def update(self) :
		ui.Page.update(self)

		self.big_image = ui.Image(self, constants.big_pos, constants.big_size, self.image_file)
		self.append(self.big_image)

		self.next_icon = ui.Image(self, constants.go_next_icon_pos, constants.go_next_icon_size, constants.go_next_icon)
		self.append(self.next_icon)



class Run_Display_Big(common.Run_Screen) :


	def __init__(self, globalvars, text, image_file, associated_sounds) :

		common.info("Running display big")

		common.Run_Screen.__init__(self, globalvars)

		self.current_page = Page_display_big(globalvars, text, image_file, associated_sounds)


		self.current_page.draw()
		pygame.display.flip()
		
		while self.running :
			
			common.Run_Screen.run_pre(self)

			for key_event in self.key_events :
				if key_event.key == K_SPACE :
					running = False


			if (self.mouse_clicked == True) :

				clicked = self.current_page.was_something_clicked(self.mouse_pos, self.mousebutton)
					
				if (clicked != None) :
					(component_clicked, foo, some_dirty_rects) = clicked

					self.dirty_rects = self.dirty_rects + some_dirty_rects
						
					if (component_clicked == self.current_page.next_icon) :
						self.running = False
						

			common.Run_Screen.run_post(self)		
