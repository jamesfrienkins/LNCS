import PySimpleGUI as sg
import threading
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
            self.clientList_send_display = {}        # in this dictionary there are info about displaying clients that can recieve files (ip):(binary value)
            self.clientList_request_display = {}     # in this dictionary there are info about displaying clients that wait to send file to server (only display info) (ip):(binary value)
            self.recieve_request = {}                # in this dictionary there are info about in format: (ip):([location_1, location_2])
            self.clnt_addr_name = {}                 # in this dictionary there are info about ip addresses and names of clients in format (ip):(name)

            self.dataset = [['addr1', 'name1', 'status1', 'time1'], ['addr2', 'name2', 'status2', 'time2']]

            for data in self.dataset:
                self.clnt_addr_name[data[0]] = data[1]
                self.clientList_connection[data[0]] = data[2]

                if data[2]:
                    self.connected_client.append(data[0])

        self.recieve_file_layout = [
        [sg.Text(self.fill('Address')), sg.Text('Name'))]
        ]

        self.send_file_layout = [
        [sg.Text(self.fill('Address')), sg.Text('Name'))]
        ]

        self.file_manager_layout = [
        [sg.TabGroup(    [[sg.Tab('Send file'), self.send_file_layout), sg.Tab('Recieve file', self.recieve_file_layout)]]    )]
        ]

        self.current_connections_layout = [
        [sg.Text(self.fill('Address')), sg.Text(self.fill('Name')), sg.Text(self.fill('Status')), sg.Text(self.fill("Time connected"))],
        [sg.Text('')]
        ]

        self.current_running_apps_layout = [
        [sg.Text('Computer: '), sg.Combo(self.connected_client, enable_events=True, key = 'selected_pc_running_tasks'), sg.Text('        Full apps list: '), sg.Checkbox('', key = 'full_app_list')]
        ]

        for data in self.dataset:               # displaying current connections
            addr, name, stat, tmcn = data

            row = [sg.Text(self.fill(addr), key = f'addr:{addr}'), sg.Text('  ' + self.fill(name), key = f'name:{addr}'), sg.Text(self.fill(stat), key = f'stat:{addr}'), sg.Text(self.fill(tmcn), key = f'tmcn:{addr}')]

            if self.clientList_connection.get(addr) == None:
                self.clientList_connection[addr] = True

                self.current_connections_layout.append(row)

        for clnt in self.connected_client:      # displaying recieve file layout
            files_to_receive = self.recieve_request.get(clnt)

            for location in files_to_receive:
                file_to_receive += location + '; '

            row1 = [sg.Text(self.fill(clnt)), sg.Text(self.fill(self.client_addr_name.get(clnt)), sg.Button('Recieve', key = f'recieve_file:{clnt}), sg.Button('Dismiss', key = 'dismiss_file:{clnt})]
            row2 = [sg.Text('Folder/file: ), sg.Text('', key = f'file_location:{clnt}')]

            self.clientList_request_display[clnt] = True

            self.recieve_file_layout.append(row1)
            self.recieve_file_layout.append(row2)

        for clnt in self.connected_client:
            row1 = [sg.Text(self.fill(clnt), sg.Text(self.fill(self.client_addr_name.get(clnt)), sg.Text('')]
            row2 = [sg.FileBrowser('Select file', key = f'select_file:{clnt}'), sg.FolderBrowser('Select folder', key = f'select_folder:{clnt}')]

            self.clientList_send_display[clnt] = True

            self.send_file_layout.append(row1)
            self.send_file_layout.append(row2)

        self.layout = [
        [sg.Text(f'Current server address: {self.ip}:{self.port}')],
        [sg.TabGroup(   [[sg.Tab('Connections', self.current_connections_layout), sg.Tab('File manager', self.file_manager_layout), sg.Tab('Running apps', self.current_running_apps_layout)]]   )]
        ]
    
        self.window = sg.Window('LNCS', self.layout)

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
