from time import sleep
import PySimpleGUI as sg
import threading
from win32com.client import CLSIDToClass
import wmi as __wni__


class interface:
    wni = __wni__.WMI()
    keyExit = False
    # window = ''

    def lang(self, key):
        dictionary_lang = {
        0 : ['recomended', 'рекомендовано'], 1 : ['not recomended', 'не рекомендовано'], 2 : ['Addr', 'Адреса'], 3 : ['Name', "Ім'я"], 4 : ['Status', 'Статус'], 5 : ['Time connnected', 'Час підключення'],
        6 : [f'''Current server address: {self.ip}:{self.port} {' ' * 104} ''', f'''Адреса даного сервера: {self.ip}:{self.port} {' ' * 85} '''], 7 : ['Connections', 'Підключення'], 8 : ['File manager', 'Файловий менеджер'],
        9 : ['Running apps', 'Запущені програми'], 10 : ['Actions', 'Дії'], 11 : ['Help', 'Довідник'], 12 : ['About', 'Інформація'], 13 : ['Folder/file;', 'Папка/файл:'], 14 : ['Select file', 'Вибрати файл'], 15 : ['Select folder', 'Вибрати папку'],
        16 : ['Receive files', 'Отримати файли'], 17 : ['Send files', 'Надіслати файли']}
        if self.clang == 'English':
            return dictionary_lang.get(key)[0]
        elif self.clang == 'Ukrainian':
            return dictionary_lang.get(key)[1]
    
    def change_lang(self):
        self.window['addr_1<:>'].update(self.fill(self.lang(2)))
        self.window['addr_2<:>'].update(self.fill(self.lang(2)))
        self.window['addr_3<:>'].update(self.fill(self.lang(2)))
        self.window['addr_4<:>'].update(self.fill(self.lang(2)))

        self.window['name_1<:>'].update(self.fill(self.lang(3)))
        self.window['name_2<:>'].update(self.fill(self.lang(3)))
        self.window['name_3<:>'].update(self.fill(self.lang(3)))
        self.window['name_4<:>'].update(self.fill(self.lang(3)))

        self.window['status_1<:>'].update(self.fill(self.lang(4)))
        self.window['time_1<:>'].update(self.fill(self.lang(5)))

        self.window['main_string<:>'].update(self.lang(6))
        self.window['tab_conn<:>'].update(self.lang(7))
        self.window['tab_file<:>'].update(self.lang(8))
        self.window['tab_apps<:>'].update(self.lang(9))
        self.window['tab_act<:>'].update(self.lang(10))
        self.window['help<:>'].update(self.lang(11))
        self.window['about<:>'].update(self.lang(12))

        for clnt in self.connected_client:
            self.window[f'folder_file_2|{clnt}<:>'].update(self.lang(13))

            self.window[f'select_file<:>{clnt}'].update(self.lang(14))
            self.window[f'select_folder<:>{clnt}'].update(self.lang(15))

        self.window['receive_file_1<:>'].update(self.lang(16))
        self.window['send_file_1<:>'].update(self.lang(17))

    def current_running_apps(self, full_list = True):
        if full_list:
            self.running_apps = []

            for process in self.wni.Win32_Process():
            
                self.running_apps.append(f"{process.ProcessId:<10}" + f"{process.Name}")

    def fill(self, string, n = 25, symbol = " "):
        n = max(len(string), n) - len(string)

        string += symbol * n

        return string

    def __init__(self):
        if True:
            self.clang = 'English'
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
            self.stream_is_running = {}              # in this dictionary there are info about what stream are going
    
            self.dataset = [['192.168.0.7', 'Personal pc 1', 'Connected', '163.7 sec'], ['192.168.0.9', 'Personal pc 2', 'Connected', '85.3 sec'], ['192.168.0.5', 'Personal pc 3', 'Connected', '27.1 sec']]
            self.receive_request = {'addr1':['list1'], 'addr2':['list2']}
            self.languages = ['English', 'Ukrainian']
            self.running_apps = []

            resolution_list = ['960 × 540', '1280 × 720', f'1920 × 1080 ({self.lang(0)})', f'3840 × 2160 {self.lang(1)}']
            fps_list = ['1x', '2x', f'4x ({self.lang(0)})', '8x', f'16x ({self.lang(1)})']

            for data in self.dataset:
                self.client_addr_name[data[0]] = data[1]

                if data[2]:
                    self.connected_client.append(data[0])

        self.client_actions_layout = [
        [sg.Text(self.fill(self.lang(2)), key = 'addr_1<:>'), sg.Text(self.fill(self.lang(3)), key = 'name_1<:>')]
        ]

        self.receive_file_layout = [
        [sg.Text(self.fill(self.lang(2)), key = 'addr_2<:>'), sg.Text(self.fill(self.lang(3)), key = 'name_2<:>')]
        ]

        self.send_file_layout = [
        [sg.Text(self.fill(self.lang(2)), key = 'addr_3<:>'), sg.Text(self.fill(self.lang(3)), key = 'name_3<:>')]
        ]

        self.current_connections_layout = [
        [sg.Text(self.fill(self.lang(2)), key = 'addr_4<:>'), sg.Text(self.fill(self.lang(3)), key = 'name_4<:>'), sg.Text(self.fill(self.lang(4)), key = 'status_1<:>'), sg.Text(self.fill(self.lang(5)), key = 'time_1<:>')],
        [sg.Text('')]
        ]

        self.current_running_apps_layout = [
        [sg.Text('Computer: '), sg.Combo(self.connected_client, enable_events = True, readonly = True, key = 'selected_pc_running_tasks<:>'), sg.Button('Get info', key = 'get_client_running_apps<:>'), sg.Text('Full apps list: '), sg.Checkbox('', key = 'full_app_list<:>')]
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
                row2 = [sg.Text(f'{self.lang(13)}: ', key = f'folder_file_1|{clnt}<:>'), sg.Text(file_to_receive, key = f'file_location_receive<:>{clnt}')]

                self.clientList_request_display[clnt] = True

                self.receive_file_layout.append(row1)
                self.receive_file_layout.append(row2)
            
            file_to_send = self.clientList_send.get(clnt)

            if file_to_send == None:
                file_to_send = ''

            row1 = [sg.Text(self.fill(clnt)), sg.Text(self.fill(self.client_addr_name.get(clnt))), sg.Text(' ' * 20), sg.FolderBrowse(self.lang(14), key = f'select_folder<:>{clnt}'), sg.FileBrowse(self.lang(15), key = f'select_file<:>{clnt}')]
            row2 = [sg.Text(f'{self.lang(13)}: ', key = f'folder_file_2|{clnt}<:>'), sg.Text(file_to_send, key = f'file_location_send<:>{clnt}')]
            row3 = [sg.Text('')]

            self.clientList_send_display[clnt] = True

            self.send_file_layout.append(row1)
            self.send_file_layout.append(row2)
            self.send_file_layout.append(row3)

            row1 = [sg.Combo(resolution_list, default_value = resolution_list[2], readonly = True, key = f'resolution_list<:>{clnt}'), sg.Combo(fps_list, default_value = fps_list[2], readonly = True, key = f'fps_list<:>{clnt}'), sg.Button('Start Stream', key = f'start_stream<:>{clnt}')]
            row2 = [sg.Button('Shutdown', key = f'shutdown<:>{clnt}'), sg.Button('Restart', key = f'restart<:>{clnt}')]
            row3 = [sg.Text('')]

            self.client_actions_layout.append(row1)
            self.client_actions_layout.append(row2)
            self.client_actions_layout.append(row3)
            
        row = [sg.Listbox(values = self.running_apps, size = (840, 555))]

        self.current_running_apps_layout.append(row)

        self.file_manager_layout = [
        [sg.TabGroup([[sg.Tab(self.lang(17), self.send_file_layout, key = 'send_file_1<:>'), sg.Tab(self.lang(16), self.receive_file_layout, key = 'receive_file_1<:>')]],size = (860, 570), key = 'current_file_tab<:>')]
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

    def help_menu(self):
        self.help_layout = [
        [sg.Text('Help menu:')],
        [sg.Multiline('')]
        ]

        return sg.Window('Help', self.help_layout, size = (500, 300), finalize = True)

    def about_menu(self):
        self.about_layout = [
        [sg.Text('About menu:')],
        [sg.Text(' ')],
        [sg.Text('Welcome to LNCS! (Local Network Comunicate System)')],
        [sg.Multiline('This system was created to help students and teachers in learning process. Product can be used by commercialand uncommercial companies')],
        [sg.Text('Created by Safiyanyk Volodymyr.')]
        ]

        return sg.Window('About', self.about_layout, size = (400, 240), finalize = True)

    def main_menu(self):
        layout = [
        [sg.Text(self.lang(6), key = 'main_string<:>'), sg.Combo(self.languages, default_value = self.languages[0], readonly = True, enable_events = True, key = 'chng_lang<:>'), sg.Button(self.lang(11), key = 'help<:>'), sg.Button(self.lang(12), key = 'about<:>')],
        [sg.TabGroup([[sg.Tab(self.lang(7), self.current_connections_layout, key = 'tab_conn<:>'), sg.Tab(self.lang(8), self.file_manager_layout, key = 'tab_file<:>'), sg.Tab(self.lang(9), self.current_running_apps_layout, key = 'tab_apps<:>'), sg.Tab(self.lang(10), self.client_actions_layout, key = 'tab_act<:>')]], size = (880, 585), key = 'current_main_tab<:>')]
        ]

        return sg.Window('LNCS', layout, size = (900, 550), finalize = True)

    def start(self):        
        self.window, self.window_help, self.window_about = self.main_menu(), None, None

        RUN = threading.Thread(target = self.main, args = (), daemon = True)

        run_main = False

        self.change_lang()

        while True:
            if not run_main:
                RUN.start()
                run_main = True
            
            if self.keyExit:
                exit()

            self.event, self.values = self.window.read(timeout = 200)

            if self.event == '__TIMEOUT__':
                continue
            elif self.event == sg.WIN_CLOSED:
                break

            key, clnt = str(self.event).split('<:>')

            if key == 'start_stream':
                if self.stream_is_running.get(clnt) == False or self.stream_is_running.get(clnt) == None:
                    self.window[f'start_stream<:>{clnt}'].update('Close Stream')
                    self.stream_is_running[clnt] = True
                else:
                    self.window[f'start_stream<:>{clnt}'].update('Start Stream')
                    self.stream_is_running[clnt] = False
            elif key == 'about':
                self.about_menu()
            elif key == 'help':
                self.help_menu()
            elif key == 'chng_lang':
                self.clang = self.values.get(key + '<:>')
                self.change_lang()

    def main(self):
        try:
            while True:
                if self.keyExit:
                    exit()
                sleep(0.1)
        except KeyboardInterrupt:
            self.keyExit = True
            exit()

if __name__ == '__main__':
    window = interface()
    window.start()
