import PySimpleGUI as sg
from time import sleep

class interface:
    sg.theme('Dark Blue 3')

    display_current_connections_layout = []
    send_files_layout = []
    
    def current_connections(self, info = []):
        self.display_current_connections_layout.append([sg.Text(' Address '), sg.Text(' Computer name '), sg.Text(' Status '), sg.Text(' Time connected ')])

        if info != []:
            for row in info:
                for data in row:
                    addr, name, status, time_conn = data

                    self.display_current_connections_layout.append([sg.Text(addr), sg.Text(name), sg.Text(status), sg.Text(time_conn)])
    def send_file(self, info = []):
        self.send_files_layout.append([sg.Text('Browse folder:'), sg.FolderBrowse(key = 'browse_folder'), sg.Button('Add', key = 'add_folder')])
        self.send_files_layout.append([sg.Text('Browse file:'), sg.FileBrowse(key = 'browse_file'), sg.Button('Add', key = 'add_file')])
        self.send_files_layout.append([sg.Text('')])
        self.send_files_layout.append([sg.Text('   Address '), sg.Text(' Computer name ')])

        if info != []:
            for row in info:
                for data in row:
                    addr, name, _, _ = data

                    self.send_files_layout.append(sg.Checkbox(key = addr), sg.Text(addr), sg.Text(name))


    def start(self):
        layout = [[sg.TabGroup([[sg.Tab('Connections', self.display_current_connections_layout), sg.Tab('File manager', self.send_files_layout)]])]]
        window = sg.Window('LNCS', layout)
        window.read()
        window.close()

window = interface()

window.send_file()
window.current_connections()

window.start()