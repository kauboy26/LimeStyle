import sublime
import sublime_plugin

import subprocess
import cgi
from threading import Thread

class LimeStyleCommand(sublime_plugin.TextCommand):

    # This exists so that information can be shared with the EventListener.
    checkstyle_info = {}

    def run(self, edit, flag):
        """
        The method that is called when the keyboard shortcut is triggered.
        :param list flag: A list of flags that checkstyle-6.2.2.jar accepts.
        """
        self.view.show_popup('Running audit (this may take a while)...',
            sublime.HIDE_ON_MOUSE_MOVE, -1)
        t = Thread(target=LimeStyleCommand.limestyle_run, args=(self, flag,))
        t.start()

    def limestyle_run(self, flag):
        """
        The main code behind LimeStyle.
        :param list flag: a list of flags that checkstyle-6.2.2.jar accepts.
        """
        self.clean_views()
        open_java_views = self.get_java_view_list()
        output, points_off, *_ = self.run_checkstyle(
            [view.file_name() for view in open_java_views], flag)
        LimeStyleCommand.checkstyle_info = self.parse_checkstyle_output(output)
        for file in LimeStyleCommand.checkstyle_info.keys():
            view = sublime.active_window().find_open_file(file)
            if view:
                print('file: ', file)
                view.run_command("save")
                mark = []
                print(LimeStyleCommand.checkstyle_info[file].keys())
                for line_num in LimeStyleCommand.checkstyle_info[file].keys():
                    offset = view.text_point(line_num - 1, 0)
                    mark.append(sublime.Region(offset, offset))
                view.add_regions("LimeStyle", mark, "mark", "dot",
                    sublime.HIDDEN)
        self.view.show_popup('<b>Unsaved changes NOT audited.<b><br>Audit done.'
            + 'Errors (potential points off):<b>' + str(points_off) + '<b>',
            sublime.HIDE_ON_MOUSE_MOVE, -1)

    def clean_views(self):
        """
        Removes existing marks with "LimeStyle" key from the gutter.
        """
        print('Cleaning')
        for view in sublime.active_window().views():
            print(view.file_name())
            view.erase_regions("LimeStyle")

    def get_java_view_list(self):
        """
        Returns a list of views that are open .java files that exist on the
        the disk, that is, they are not simply buffers.
        """
        java_view_list = []
        print('called')
        for view in sublime.active_window().views():
            if view.file_name() and view.file_name().endswith('.java'):
                print(view.file_name())
                java_view_list.append(view)
        return java_view_list

    def run_checkstyle(self, file_list, flag):
        """
        Method runs the checkstyle jar on the file list, and returns the unparsed
        output.
        """
        jar_path = __file__[:__file__.rfind('/') + 1] + 'checkstyle-6.2.2.jar'
        cmd = ['java', '-jar', jar_path] + flag + file_list
        output = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # output.communicate() returns a tuple --> (stdout, stderr)
        # output.returncode is the number of points off
        return output.communicate(), output.returncode

    def parse_checkstyle_output(self, checkstyle_output):
        """
        Parses the output, converts it into dictionary with file names as the key.
        Each value is a dictionary, with the line numbers as keys. The value for
        each key is a list with error descriptions.

        In case stderr was not 'None', it is reported.
        """
        stdout, stderr, *_ = checkstyle_output
        checkstyle_info_dict = {}
        if not (stderr is None):
            print('stderr:\n', stderr.decode("utf-8"))
        stdout = stdout.decode("utf-8")
        # the last two lines aren't needed.
        for line in stdout.splitlines()[:-2]:
            file_path, line_num, *description = line.split(':')
            # The line can be of the form file_path:line_num:column_num:desc
            # or file_path:line_num:desc. column_num and desc are combined together
            # into description
            line_num = int(line_num)
            description = ':'.join(description)
            if file_path in checkstyle_info_dict:
                if line_num in checkstyle_info_dict[file_path]:
                    checkstyle_info_dict[file_path][line_num].append(description)
                else:
                    checkstyle_info_dict[file_path][line_num] = [description]
            else:
                checkstyle_info_dict[file_path] = {line_num: [description]}
        return checkstyle_info_dict

class CheckstyleDescriber(sublime_plugin.EventListener):

    def on_hover(self, view, point, hover_zone):
        """
        Called when mouse hovers.
        Displays a popup if an error exists at that line number.
        """
        if hover_zone == sublime.HOVER_GUTTER:
            file_name = view.file_name()
            if file_name in LimeStyleCommand.checkstyle_info:
                line_num = view.rowcol(point)[0] + 1
                # print('line num:', line_num)
                if line_num in LimeStyleCommand.checkstyle_info[file_name]:
                    # print('error linen no')
                    view.show_popup(
                        '<br>'.join([cgi.escape(frag) for frag in
                            LimeStyleCommand.checkstyle_info[file_name][line_num]]),
                        sublime.HIDE_ON_MOUSE_MOVE,
                        point)