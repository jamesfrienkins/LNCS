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
            self.dataset = [['addr1', 'name1', 'status1', 'time1'], ['addr2', 'name2', 'status2', 'time2']]
            self.connected_client = ['pc1', 'pc2']
            self.clientList = {}

        self.file_manager_layout = []

        self.current_connections_layout = [
        [sg.Text(self.fill('Address')), sg.Text(self.fill('Name')), sg.Text(self.fill('Status')), sg.Text(self.fill("Time connected"))],
        [sg.Text('')]
        ]

        self.current_running_apps_layout = [
        [sg.Text('Computer: '), sg.Combo(self.connected_client, enable_events=True, key = 'selected_pc_running_tasks'), sg.Text('        Full apps list: '), sg.Checkbox('', key = 'full_app_list')]
        ]

        for data in self.dataset:
            addr, name, stat, tmcn = data

            row = [sg.Text(self.fill(addr), key = f'addr:{addr}'), sg.Text('  ' + self.fill(name), key = f'name:{addr}'), sg.Text(self.fill(stat), key = f'stat:{addr}'), sg.Text(self.fill(tmcn), key = f'tmcn:{addr}')]

            if self.clientList.get(addr) == None:
                self.clientList[addr] = True

            self.current_connections_layout.append(row)

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
