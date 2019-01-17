# -*- coding: utf-8 -*-

# Omnitux - educational activities based upon multimedia elements
# Copyright (C) 2008 Olav_2 (olav.olav@yahoo.fr)

# Polish translation by Kot26
# German translation by Manfred Schulenburg
# Portuguese translation by Daniel von Weissenfluh
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

import constants, common, os

text = {}
countries = {}

for language in constants.supported_languages :
	text[language] = {}
	countries[language] = {}

# Languages are sorted by alphabetical order
text['de']['de'] = "Deutsch"	
text['en']['en'] = "English"
text['es']['es'] = "Español"
text['fr']['fr'] = "Français"
text['it']['it'] = "Italiano"
#text['nl']['nl'] = "Nederlands"
text['pl']['pl'] = "Polski"
text['pt']['pt'] = "Português"
text['zh']['zh'] = u"汉语" 

language_sound = {}
language_sound['de']=["default/languages/De-German_-_Deutsch.ogg"]
language_sound['en']=["default/languages/En-us-english.ogg"]
language_sound['es']=["default/languages/Es-sv-espanol.mod.ogg"]
language_sound['fr']=["default/languages/Fr-francais.ogg"]
language_sound['it']=["default/languages/It-italiano.ogg"]
language_sound['nl']=["default/languages/Nl-Nederlands.ogg"]
language_sound['pl']=["default/languages/Pl-polski.ogg"]
language_sound['pt']=["default/languages/Pt-Portugues.ogg"]
language_sound['zh']=[""] # would you have a recording of the sound 'Chinese' to put here ?


# TODO : add missing countries and flags
# here is the list of countries where each language is an official language
# cf http://en.wikipedia.org/wiki/List_of_official_languages
countries['de'] = ['at', 'be', 'de', 'li', 'lu', 'ch']
countries['en'] = ['ag', 'au', 'bs', 'bb', 'bz', 'bw', 'ca', 'cm', 'dm', 'fj', 'gm', 'gh', 'gd', 'gg', 'gy', 'in', 'ie', 'jm',
		   'je', 'ke', 'ki', 'ls', 'lr', 'mg', 'mw', 'mt', 'im', 'mh', 'mu', 'fm', 'na', 'nr', 'an', 'nz', 'ng', 'pk', 'ph',
		   'pw', 'pg', 'rw', 'kn', 'lc', 'vc', 'ws', 'sc', 'sl', 'sg', 'sb', 'za', 'sd', 'sz', 'tz', 'to', 'tt', 'tv', 'ug',
		   'gb', 'us', 'vu', 'zm', 'zw']
countries['es'] = ['ar', 'bo', 'cl', 'co', 'cr', 'cu', 'do', 'ec', 'sv', 'gq', 'gt', 'hn', 'mx', 'ni', 'pa', 'py', 'pe', 'es', 'uy', 've' ]
countries['fr'] = ['be', 'bj', 'bf', 'bi', 'cm', 'ca', 'cf', 'td', 'km', 'ci', 'cd', 'dj', 'fr', 'gq', 'ga', 'gg', 'gn', 'ht', 'je',
		   'lu', 'mg', 'ml', 'mc', 'ne', 'cg', 'rw', 'sn', 'sc', 'lc', 'ch', 'tg', 'vu']
countries['it'] = ['it', 'ch']
countries['nl'] = ['be', 'nl', 'sr']
countries['pl'] = ['pl']
countries['pt'] = ['ao', 'br', 'cv', 'tl', 'gw', 'mz', 'pt', 'st']
countries['zh'] = ['cn', 'sg', 'tw']

countries_prefix = "default/icons/flags/flag_"
countries_suffix = ".svg"



# range 100 - 999 : common stuff
text['de'][100] = "Ja"
text['en'][100] = "Yes"
text['es'][100] = "Sí"
text['fr'][100] = "Oui"
text['it'][100] = "Sì"
#text['nl'][100] = "Ja"
text['pl'][100] = "Tak"
text['pt'][100] = "Sim"
text['zh'][100] = ""

text['de'][101] = "Nein"
text['en'][101] = "No"
text['es'][101] = "No"
text['fr'][101] = "Non"
text['it'][101] = "No"
text['pl'][101] = "Nie"
text['pt'][101] = "Não"
text['zh'][101] = ""


text['de'][102] = "Das 'pygame' Paket ist nicht installiert auf ihrem Computer."
text['en'][102] = "The 'pygame' package is not installed on your computer"
text['es'][102] = "El paquete 'pygame' no está instalado en tu computadora"
text['fr'][102] = "Le package 'pygame' n'est pas installé sur votre système"
text['it'][102] = "Il pacchetto 'pygame' non è installato sul computer"
# text['pl'][102] = "The 'pygame' package is not installed on your computer"
text['pt'][102] = "O pacote 'pygame' não esta instalado no seu computador"
text['zh'][102] = ""

text['de'][103] = "Das 'pygtk' Paket ist nicht installiert auf ihrem Computer."
text['en'][103] = "The 'pygtk' package is not installed on your computer"
text['es'][103] = "El paquete 'pygtk' no está instalado en tu computadora"
text['fr'][103] = "Le package 'pygtk' n'est pas installé sur votre système"
text['it'][103] = "Il pacchetto 'pygtk' non è installato sul computer"
# text['pl'][103] = "The 'pygtk' package is not installed on your computer"
text['pt'][103] = "O pacote 'pygtk' não esta instalalado no seu computador"
text['zh'][103] = ""


text['de'][104] = "Bitte benutzen sie ihren favorisierten Paketmanager zum installieren(yum, yast, synaptic...)."
text['en'][104] = "Please use your favourite package manager to install it (yum, yast, synaptic...)"
text['es'][104] = "Por favor utiliza tu gestor de paquetes favorito para instalarlo (yum, yast, synaptic...)"
text['fr'][104] = "Veuillez l'installer grace à votre gestionnaire de paquetages favori (yum, yast, synaptic...)"
text['it'][104] = "Utilizza il gestore di pacchetti (yum, yast, synaptic...) per installarli"
# text['pl'][104] = "Please use your favourite package manager to install it (yum, yast, synaptic...)"
text['pt'][104] = "Por favor use seu gerenciador de pacote preferido para instalar (yum, yast, synaptic...)"
text['zh'][104] = ""


text['en'][105] = "Options"
text['es'][105] = "Opciones"
text['fr'][105] = "Options"
text['it'][105] = "Opzioni"
text['zh'][105] = ""

text['en'][200] = "Screen resolution"
text['es'][200] = "Resolución de la pantalla"
text['fr'][200] = "Résolution écran"
text['it'][200] = "Risoluzione schermo"
text['zh'][200] = ""

text['en'][201] = "Music volume"
text['es'][201] = "Volumen de la música"
text['fr'][201] = "Volume de la musique"
text['it'][201] = "Volume della musica"
text['zh'][201] = ""


text['fr'][202] = "Affichage"
text['it'][202] = "Schermo"
text['en'][202] = "Display"
text['zh'][202] = ""

text['fr'][203] = "Son"
text['it'][203] = "Suono"
text['en'][203] = "Sound"
text['zh'][203] = ""

text['fr'][204] = "Sons"
text['it'][204] = "Suoni"
text['en'][204] = "Sounds"
text['zh'][204] = ""

text['fr'][205] = "Voix"
text['it'][205] = "Voci"
text['en'][205] = "Voices"
text['zh'][205] = ""

text['fr'][206] = "Divers"
text['it'][206] = "Altri"
text['en'][206] = "Miscellaneous"
text['zh'][206] = ""


text['fr'][207] = "Preferences"
text['it'][207] = "Preferenze"
text['en'][207] = "Preferences"
text['zh'][207] = ""


text['fr'][208] = "Félicitations"
text['it'][208] = "Congratulazioni"
text['en'][208] = "Congratulations"
text['zh'][208] = ""


text['en'][210] = "*** Please restart omnitux to apply the new screen resolution ***"
text['es'][210] = "*** Por favor, reinicie omnitux para aplicar la nueva resolución de pantalla ***"
text['fr'][210] = "*** Veuillez redémarrer omnitux afin d'obtenir la nouvelle résolution d'écran ***"
text['it'][210] = "*** Per ottenere la nuova risoluzione di schermo riavvia omnitux ***"
text['zh'][210] = ""


text['fr'][220] = "Mode arcade"
text['it'][220] = "Modalità Arcade"
text['en'][220] = "\"Arcade\" mode"
text['zh'][220] = ""


text['fr'][250] = "Langue au démarrage"
text['it'][250] = "Lingua Iniziale"
text['en'][250] = "Language at startup"
text['zh'][250] = ""


text['fr'][251] = "Valeur système"
text['it'][251] = "Valori di Sistema"
text['en'][251] = "System value"
text['zh'][251] = ""

text['fr'][252] = "Choix utilisateur : "
text['it'][252] = "Scelte utente : "
text['en'][252] = "User value : "
text['zh'][252] = ""

text['fr'][253] = "Langues"
text['it'][253] = "Lingue"
text['en'][253] = "Languages"
text['zh'][253] = ""


text['de'][1020] = "Iglu"
text['en'][1020] = "Igloo"
text['es'][1020] = "Iglú"
text['fr'][1020] = "Igloo"
text['it'][1020] = "Igloo"
text['pl'][1020] = "Iglo"
text['pt'][1020] = "Iglu"
text['zh'][1020] = ""


text['de'][1102] = "Die Multimedia-Dateien kommen von verschiedenen Autoren. Bitte vergleichen sie die dazugehörigen .txt-Dateien."
text['en'][1102] = "Multimedia files come from various authors, please check the associated .txt files."
text['es'][1102] = "Los archivos multimedia fueron creados por varios autores, por favor revisa los archivos .txt asociados."
text['fr'][1102] = "Les fichiers multimedia ont été créés par de nombreux auteurs, voir les fichiers .txt associés."
text['it'][1102] = "I file multimediali sono stati realizzati da vari autori, puoi verificarli dai file .txt associati."
text['pl'][1102] = "Pliki multimedialne pochodzą od wielu autorów, więcej informacji w dołączonych plikach .txt."
text['pt'][1102] = "Os arquivos de multimídia foram criados por vários autores. Verifique os arquivos .txt associados."
text['zh'][1102] = ""



text['de'][1103] = "Musik von Denis RICHARD (www.jamendo.com)"
text['en'][1103] = "Music by Denis RICHARD (www.jamendo.com)"
text['es'][1103] = "Música por Denis RICHARD (www.jamendo.com)"
text['fr'][1103] = "Musique de Denis RICHARD (www.jamendo.com)"
text['it'][1103] = "Musica di Denis RICHARD (www.jamendo.com)"
text['pl'][1103] = "Muzyka Denis'a RICHARD'A (www.jamendo.com)"
text['pt'][1103] = "Música de Denis RICHARD (www.jamendo.com)"
text['zh'][1103] = ""


text['de'][1105] = "Spiel verlassen ?"
text['en'][1105] = "Quit Game ?"
text['es'][1105] = "¿ Salir del juego ?"
text['fr'][1105] = "Terminer le jeu ?"
text['it'][1105] = "Vuoi uscire dal gioco ?"
text['pl'][1105] = "Koniec gry ?"
text['pt'][1105] = "Sair do jogo ?"
text['zh'][1105] = ""


text['de'][1106] = "Schwierigkeitsgrad auswählen"
text['en'][1106] = "Select level"
text['es'][1106] = "Elegir nivel"
text['fr'][1106] = "Choisir le niveau"
text['it'][1106] = "Scegli il Livello"
text['pl'][1106] = "Wybierz poziom"
text['pt'][1106] = "Selecione o nível"
text['zh'][1106] = ""


sound = {}

# sounds played to "reward" a good answer

sound[1000] = ["default/sound/32235__fredgalist__AltoSax1.ogg", "default/sound/17901__zippi1__sound_smile2.ogg"]

# sounds played after a mistake :

sound[1001] = [
"default/sound/46709_boney_man_Snare044.ogg",
"default/sound/36896__icmusic__bt_three_tone.ogg",
"default/sound/73581__Benboncan__Sad_Trombone.ogg",
"default/sound/67454__Splashdust__negativebeep.ogg",
"default/sound/49945__simon.rue__misslyckad_bana_v2.ogg"
]


voice = {}

for language in constants.supported_languages :
	voice[language] = {}

# voices played to "reward" a good answer

voice['de'][1000] = [
"default/sound/De/De_prima.ogg",
"default/sound/De/De_gut_gemacht.ogg",
"default/sound/De/De_richtig.ogg",
"default/sound/De/De_glueckwunsch.ogg",
"default/sound/De/De_ja.ogg",
"default/sound/De/De_sehr_gut.ogg",
"default/sound/De/De_perfekt.ogg",
"default/sound/De/De_ausgez.ogg"
]

voice['en'][1000] = ["default/sound/En-us/31712__FreqMan__real_good.ogg", "default/sound/En-us/Good-eng-6c844e92.ogg", "default/sound/En-us/En-us-yes.ogg"]


voice['es'][1000] = []


voice['fr'][1000] = [
"default/sound/Fr/Fr_bravo.ogg",
"default/sound/Fr/Fr_c_est_bien.ogg",
"default/sound/Fr/Fr_exactement.ogg",
"default/sound/Fr/FR_felicitations.ogg",
"default/sound/Fr/Fr_oui.ogg",
"default/sound/Fr/Fr_tres_bien.ogg"]

voice['it'][1000] = [
"default/sound/It/bel_lavoro.ogg",
"default/sound/It/bene.ogg",
"default/sound/It/ok.ogg",
"default/sound/It/perfetto.ogg",
"default/sound/It/molto_bene.ogg",
"default/sound/It/sii.ogg"]

voice['pl'][1000] = [
"default/sound/Pl/Pl-brawo.ogg",
"default/sound/Pl/Pl-dobrze.ogg", 
"default/sound/Pl/Pl-dokladnie.ogg",
"default/sound/Pl/Pl-doskonale.ogg",  
"default/sound/Pl/Pl-gratulacje.ogg",
"default/sound/Pl/Pl-swietnie.ogg",
]

voice['pt'][1000] = [
"default/sound/Pt/Pt-bravo.ogg",
"default/sound/Pt/Pt-exatemente.ogg",
"default/sound/Pt/Pt-isso_mesmo.ogg",
"default/sound/Pt/Pt-muito_bem.ogg",
"default/sound/Pt/Pt-parabens.ogg"
]

voice['zh'][1000] = []



# sounds played after a mistake

voice['de'][1001] = [
"default/sound/De/De_nochmal.ogg",
"default/sound/De/De_leider_nicht.ogg"
]

voice['en'][1001] = [
]


voice['es'][1001] = [
]


voice['fr'][1001] = [
"default/sound/Fr/Fr_Non.ogg",
"default/sound/Fr/Fr_essaie_encore.ogg",
"default/sound/Fr/Fr_erreur.ogg"
]

voice['it'][1001] = [
]

voice['pl'][1001] = [
"default/sound/Pl/Pl-to_nie_tak.ogg",
"default/sound/Pl/Pl-sprobuj_jeszcze_raz.ogg",
"default/sound/Pl/Pl-sprobuj_inaczej.ogg"
]

voice['pt'][1001] = [
"default/sound/Pt/Pt-nao.ogg",
"default/sound/Pt/Pt-pensa_um_pouco.ogg",
"default/sound/Pt/Pt-resposta_errada.ogg",
"default/sound/Pt/Pt-tenta_denovo.ogg"
]

voice['zh'][1001] = [
]





def get_text(language, key, variables = None) :
	
	text_result = ""
	
	try :
		text_result = text[language][key]
		
	except KeyError :
		common.warn("Missing translation in language " + language + " for key " + str(key))

		try :
			text_result = text[constants.fallback_language][key]
			
		except KeyError :
			for lang in constants.supported_languages :
				try :
					text_result = text[lang][key]
				except KeyError :
					foo = 0
				finally :
					break
					
			if (text_result == "") :
				text_result = "Missing translation in i18n.py file"
	
	if (variables != None) :
		index = 0
		for variable in variables :
			(before, foo, after) = text_result.rpartition("[" + str(index) + "]")
			text_result = before + variable + after
			
			index = index + 1

	return text_result


def get_text_from_dict(dict, language) :
	
	text_result = ""
	
	try :
		text_result = dict[language] 
	except KeyError :
		common.warn("Missing translation in language "+language)
		
		try :
			text_result = dict[constants.fallback_language]
			
		except KeyError :
			
			for lang in constants.supported_languages :
				try :
					text_result = dict[language]
				except KeyError :
					foo = 0
				finally :
					break
					
			if (text_result == "") :
				text_result = "Missing translation"			
	
	return text_result

def bool_to_text(language, boolean) :

	if (boolean == True) :
		return text[language][100]

	else :
		return text[language][101]
	

class i18n_dict() :
	
	def __init__(self, xml_node) :
		
		self.text_dict = {}
	
		for language in constants.supported_languages :
			self.text_dict[language] = {}


		# loading the dictionary
		dict_nodes = xml_node.getElementsByTagName("dict")

		for dict_node in dict_nodes :
			key = dict_node.getAttribute("key")
			lang = dict_node.getAttribute("lang")
			value = dict_node.getAttribute("value")

			self.add(lang, key, value)


	def add(self, language, key, text) :
		
		self.text_dict[language][key] = text

	def get(self, language, key) :

		try :
			text = self.text_dict[language][key]

		except KeyError :

			text = ""

		return text
