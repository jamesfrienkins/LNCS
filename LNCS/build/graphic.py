from time import sleep
import PySimpleGUI as sg
import socket
import threading
import wmi as __wni__



class interface:
    wni = __wni__.WMI()
    keyExit = False

    def current_running_apps(self, full_list = True):
        if full_list:
            self.running_apps = []

            for process in self.wni.Win32_Process():
            
                self.running_apps.append(f"{process.ProcessId:<10}" + f"{process.Name}")

    def fill(self, string, n = 20, symbol = " "):
        n = max(len(string), n) - len(string)

        string += symbol * n

        return string
            
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

            self.dataset = [['192.168.0.7', 'Personal pc 1', 'Connected', '163.7 sec'], ['192.168.0.9', 'Personal pc 2', 'Connected', '85.3 sec'], ['192.168.0.5', 'Personal pc 3', 'Connected', '27.1 sec']]
            self.receive_request = {'addr1':['list1'], 'addr2':['list2']}

            for data in self.dataset:
                self.client_addr_name[data[0]] = data[1]

                if data[2]:
                    self.connected_client.append(data[0])

        self.client_actions_layout = [
        [sg.Text('Computer: '), sg.Combo(self.connected_client, enable_events = True, key = 'selected_client_actions'), sg.Button('Get actions', key = 'get_client_actions')]
        ]
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
        [sg.Text('Computer: '), sg.Combo(self.connected_client, enable_events = True, key = 'selected_pc_running_tasks'), sg.Button('Get info', key = 'get_client_running_apps'), sg.Text('Full apps list: '), sg.Checkbox('', key = 'full_app_list')]
        ]

        for data in self.dataset:               # displaying current connections
            addr, name, stat, tmcn = data

            row = [sg.Text(self.fill(addr), key = f'addr<:>{addr}'), sg.Text(self.fill(name), key = f'name<:>{addr}'), sg.Text(self.fill(stat), key = f'stat<:>{addr}'), sg.Text(self.fill(tmcn), key = f'tmcn<:>{addr}')]
            
            if self.clientList_connection.get(addr) == None:
                self.clientList_connection[addr] = True

                self.current_connections_layout.append(row)
            
        for clnt in self.connected_client:      # displaying receive and send file layout
            files_to_receive = self.receive_request.get(clnt)
            file_to_receive = ''
            
            if files_to_receive != None:
                for location in files_to_receive:
                    file_to_receive += location + '; '

                row1 = [sg.Text(self.fill(clnt)), sg.Text(self.fill(self.client_addr_name.get(clnt))), sg.Button('Receive', key = f'receive_file<:>{clnt}'), sg.Button('Dismiss', key = 'dismiss_file<:>{clnt}')]
                row2 = [sg.Text('Folder/file: '), sg.Text(file_to_receive, key = f'file_location_receive<:>{clnt}')]

                self.clientList_request_display[clnt] = True

                self.receive_file_layout.append(row1)
                self.receive_file_layout.append(row2)
            
            file_to_send = self.clientList_send.get(clnt)

            if file_to_send == None:
                file_to_send = ''

            row1 = [sg.Text(self.fill(clnt)), sg.Text(self.fill(self.client_addr_name.get(clnt))), sg.Text(''), sg.FolderBrowse('Select folder', key = f'select_folder<:>{clnt}'), sg.FileBrowse('Select file', key = f'select_file<:>{clnt}')]
            row2 = [sg.Text('Folder/file: '), sg.Text(file_to_send, key = f'file_location_send<:>{clnt}')]

            self.clientList_send_display[clnt] = True

            self.send_file_layout.append(row1)
            self.send_file_layout.append(row2)
        
        self.current_running_apps()
    
        row = [sg.Listbox(values = self.running_apps, size = (840, 555))]

        self.current_running_apps_layout.append(row)

        print(self.running_apps)


        self.file_manager_layout = [
        [sg.TabGroup([[sg.Tab('Send file', self.send_file_layout), sg.Tab('Receive file', self.receive_file_layout)]],size = (860, 570), key = 'current_file_tab')]
        ]

        self.layout = [
        [sg.Text(f'Current server address: {self.ip}:{self.port}')],
        [sg.TabGroup([[sg.Tab('Connections', self.current_connections_layout), sg.Tab('File manager', self.file_manager_layout), sg.Tab('Running apps', self.current_running_apps_layout), sg.Tab('Actions', self.client_actions_layout)]], size = (880, 585), key = 'current_main_tab')]
        ]
    
    def update_values(self, dataset_ = None, receive_request_ = None):
        if dataset_ != None:
            self.dataset = dataset_
        if receive_request_ != None:
            self.receive_request = receive_request_

    def update_window(self):
        try:
            target = self.values.get('current_main_tab')

            if target == 'Connections':
                for data in self.dataset:
                    clnt_addr, _, clnt_stat, clnt_tmcn = data

                    self.window[f'stat<:>{clnt_addr}'].update(self.fill(clnt_stat))
                    self.window[f'tmcn<:>{clnt_addr}'].update(self.fill(clnt_tmcn))

            elif target == 'File manager':
                pass
            elif target == 'Running apps':
                pass
            elif target == 'Actions':
                pass
        except:
            pass

    def start(self):
        self.window = sg.Window('LNCS', self.layout, size = (900, 600), finalize = True)

        RUN = threading.Thread(target = self.main, args = (), daemon = True)

        run_main = False

        while True:
            if self.keyExit:
                exit()

            self.event, self.values = self.window.read(timeout = 200)

            if not run_main:
                RUN.start()
                run_main = True

            if self.event == sg.WIN_CLOSED:
                break

    def main(self):
        try:
            t = 0
            while True:
                if self.keyExit:
                    exit()
                t += 0.1
                # self.update_values(dataset_=[['addr1', 'name1', 'status1', str(t)], ['addr2', 'name2', 'status2', str(t)]])
                # self.update_window()
                sleep(0.1)
        except KeyboardInterrupt:
            exit()


if __name__ == '__main__':
    window = interface()
    window.start()