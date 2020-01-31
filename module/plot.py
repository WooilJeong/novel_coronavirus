class corona():

    def __init__(self, data_nm):

        # set dataset
        self.data_nm = data_nm
        self.dataset = globals()[self.data_nm].copy()

        # set date index
        self.dataset.index = self.dataset['Last Update']
        self.dataset.index = self.dataset.index.astype("category")
        self.objects = list(self.dataset.index)
        self.y_pos = np.arange(len(self.objects))

    def plot_confirmed(self):

        plt.figure(figsize=(15,5))
        plt.title(self.data_nm+'(Confirmed)', size='25', weight='bold')
        plt.plot(self.y_pos, self.dataset['Confirmed'], color='dodgerblue', linewidth=3, marker='o')
        plt.xticks(self.y_pos, self.objects, rotation=45)
        plt.xlabel('Reported Time', size='20')
        plt.ylabel('Count', size='20')
        plt.show()

    def plot_deaths_recovered(self):

        plt.figure(figsize=(15,5))
        plt.title(self.data_nm+'(Deaths, Recovered)', size='25', weight='bold')
        plt.plot(self.y_pos, self.dataset['Deaths'], color='tomato', label='Deaths', linewidth=3, marker='o')
        plt.plot(self.y_pos, self.dataset['Recovered'], color='orange', label='Recovered', linewidth=3, marker='o')
        plt.legend(loc='upper left')
        plt.xticks(self.y_pos, self.objects, rotation=45)
        plt.xlabel('Reported Time', size='20')
        plt.ylabel('Count', size='20')
        plt.show()

    def plot_dc_rc(self):
        plt.figure(figsize=(15,5))
        plt.title(self.data_nm+'(D/C, R/C)', size='25', weight='bold')
        plt.plot(self.y_pos, self.dataset['D/C'], color='tomato', label='D/C', linewidth=3, marker='o')
        plt.plot(self.y_pos, self.dataset['R/C'], color='orange', label='R/C', linewidth=3, marker='o')
        plt.ylim(0, 100)
        plt.legend(loc='upper left')
        plt.xticks(self.y_pos, self.objects, rotation=45)
        plt.xlabel('Reported Time', size='20')
        plt.ylabel('Indicator values(%)', size='20')
        plt.show()

    def plot_world_confirmed(self):
        plt.figure(figsize=(20,10))
        plt.title('World Confirmed Trend('+self.data_nm+')', size='25', weight='bold')
        for i in self.dataset.columns[1:]:
            plt.plot(self.y_pos, self.dataset[i], label=i, linewidth=3, marker='o')
        plt.legend(loc='upper left')
        plt.xticks(self.y_pos, self.objects, rotation=45)
        plt.xlabel('Reported Time', size='20')
        plt.ylabel('Confirmed Count', size='20')
        plt.show()
