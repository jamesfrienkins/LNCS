from typing import Text
import PySimpleGUI as sg
import threading
from PySimpleGUI.PySimpleGUI import running_windows
import wmi as __wni__



class interface:
    wni = __wni__.WMI()

    def fill(self, string, n = 20, symbol = " "):
        n = max(len(string), n) - len(string)

        string += symbol * n

        return string

    def current_running_apps(self, full_list = True):
        if full_list:
            self.running_apps = []

            for process in self.wni.Win32_Process():
            
                self.running_apps.append([f"{process.ProcessId:<10}", f"{process.Name}"])
            
    def __init__(self):
        self.running_apps = []

        if True:
            self.ip = '192.168.0.1'
            self.port = '55555'
            self.dataset = []                        # this massive is used to get info about clients [ip, name, status, time]
            self.connected_client = []               # in this massive there info about only CURRENTLY connected clients
            self.clientList_connection = {}          # in this dictionary there are info about displaying clients that are (or was) connected to server (only display info) (ip):(binary value)
            self.clientList_send = {}                # in this dictionary there are info about files for sending in format: (ip):([location_1, location_2])
            self.clientList_send_display = {}        # in this dictionary there are info about displaying clients that can receive files (ip):(binary value)
            self.clientList_request_display = {}     # in this dictionary there are info about displaying clients that wait to send file to server (only display info) (ip):(binary value)
            self.receive_request = {}                # in this dictionary there are info about in format: (ip):([location_1, location_2])
            self.client_addr_name = {}               # in this dictionary there are info about ip addresses and names of clients in format (ip):(name)

            self.dataset = [['addr1', 'name1', 'status1', 'time1'], ['addr2', 'name2', 'status2', 'time2']]
            self.receive_request = {'addr1':['list1'], 'addr2':['list2']}

            for data in self.dataset:
                self.client_addr_name[data[0]] = data[1]

                if data[2]:
                    self.connected_client.append(data[0])

        self.receive_file_layout = [
        [sg.Text(self.fill('Address')), sg.Text('Name')]
        ]

        self.send_file_layout = [
        [sg.Text(self.fill('Address')), sg.Text('Name')]
        ]

        self.current_connections_layout = [
        [sg.Text(self.fill('Address')), sg.Text(self.fill('Name')), sg.Text(self.fill('Status')), sg.Text(self.fill("Time connected"))],
        [sg.Text('')]
        ]

        self.current_running_apps_layout = [
        [sg.Text('Computer: '), sg.Combo(self.connected_client, enable_events=True, key = 'selected_pc_running_tasks'), sg.Button('Get info', key = 'get_client_running_apps'), sg.Text('Full apps list: '), sg.Checkbox('', key = 'full_app_list')]
        ]

        for data in self.dataset:               # displaying current connections
            addr, name, stat, tmcn = data

            row = [sg.Text(self.fill(addr), key = f'addr:{addr}'), sg.Text('  ' + self.fill(name), key = f'name:{addr}'), sg.Text(self.fill(stat), key = f'stat:{addr}'), sg.Text(self.fill(tmcn), key = f'tmcn:{addr}')]
            
            if self.clientList_connection.get(addr) == None:
                self.clientList_connection[addr] = True

                self.current_connections_layout.append(row)
            
        print(self.connected_client)

        for clnt in self.connected_client:      # displaying receive and send file layout
            files_to_receive = self.receive_request.get(clnt)
            file_to_receive = ''
            print(clnt, files_to_receive)
            
            if files_to_receive != None:
                for location in files_to_receive:
                    file_to_receive += location + '; '

                row1 = [sg.Text(self.fill(clnt)), sg.Text(self.fill('  ' + self.client_addr_name.get(clnt))), sg.Button('Receive', key = f'receive_file:{clnt}'), sg.Button('Dismiss', key = 'dismiss_file:{clnt}')]
                row2 = [sg.Text('Folder/file: '), sg.Text(file_to_receive, key = f'file_location_receive:{clnt}')]

                self.clientList_request_display[clnt] = True

                self.receive_file_layout.append(row1)
                self.receive_file_layout.append(row2)
            
            file_to_send = self.clientList_send.get(clnt)

            if file_to_send == None:
                file_to_send = ''

            row1 = [sg.Text(self.fill(clnt)), sg.Text(self.fill('  ' + self.client_addr_name.get(clnt))), sg.Text(''), sg.FolderBrowse('Select folder', key = f'select_folder:{clnt}'), sg.FileBrowse('Select file', key = f'select_file:{clnt}')]
            row2 = [sg.Text('Folder/file: '), sg.Text(file_to_send, key = f'file_location_send:{clnt}')]

            self.clientList_send_display[clnt] = True

            self.send_file_layout.append(row1)
            self.send_file_layout.append(row2)

        self.file_manager_layout = [
        [sg.TabGroup(    [[sg.Tab('Send file', self.send_file_layout), sg.Tab('Receive file', self.receive_file_layout)]],size = (860, 570)    )]
        ]

        self.layout = [
        [sg.Text(f'Current server address: {self.ip}:{self.port}')],
        [sg.TabGroup(   [[sg.Tab('Connections', self.current_connections_layout), sg.Tab('File manager', self.file_manager_layout), sg.Tab('Running apps', self.current_running_apps_layout)]], size = (880, 585)   )]
        ]
    
        self.window = sg.Window('LNCS', self.layout, size = (900, 600))

    def __run_window__(self):
        while True:
            event, values = self.window.read(timeout = 20)

            if event == sg.WIN_CLOSED:
                break

    def start(self):
        try:
            RUN = threading.Thread(target = self.__run_window__, args = (), daemon = True)
            RUN.start()

            while True:
                pass
        except KeyboardInterrupt:
            pass



window = interface()
window.__run_window__()
