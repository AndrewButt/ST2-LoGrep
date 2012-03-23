import sublime, sublime_plugin

class PromptLoGrepCommand(sublime_plugin.WindowCommand):

	def run(self):
		self.window.show_input_panel("Enter Search:", "", self.on_done, None, None)
		pass

	def on_done(self, searchstring):
		try:
			if self.window.active_view():
				self.window.active_view().run_command("grep", {"searchstring": searchstring} )
		except ValueError:
			pass

class LogrepCommand(sublime_plugin.TextCommand):

	def run(self, edit, searchstring):
		foundText = []
		for region in self.view.sel():			
			if region.empty():
				#No selections, process all body
				foundText = self.view.find_all(searchstring, sublime.IGNORECASE)
			else:
				#regions contain multiple liens, we are only looking
				#for the line which contains our searchstring
				region = self.view.split_by_newlines(region)

				for subregion in region: #subregion is a single line
					tline = self.view.substr(self.view.line(subregion))					
					if tline.find(searchstring) is not -1:
						foundText.append(self.view.line(subregion))

		regions = []
		for item in foundText:
			#Create [region] containing one region per LINE
			currLine = self.view.line(item)
			if currLine not in regions:
			 	regions.append(currLine)

		results = ""
		if len(regions) > 0:
			
			for subregion in regions:
				results = results + self.view.substr(subregion) + '\n'

			window = sublime.active_window()
			syntax = self.view.settings().get('syntax')
			#Will need to change to for Mac/Unix.. how to tell?
			filename = self.view.file_name().split("\\")[-1]
			edit = self.view.begin_edit()
			resultWindow = window.new_file()

			window.focus_view(resultWindow)
			resultWindow.set_name("results_" + filename)
			resultWindow.set_syntax_file(syntax)
			resultWindow.insert(edit,0,results)
			self.view.end_edit(edit)