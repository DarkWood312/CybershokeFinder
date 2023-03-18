from tkinter import *
import customtkinter
from cyberfinder import main, text_expressing


class OptionsFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Server
        self.serverlabel = customtkinter.CTkLabel(self, text='Server filters: ', width=250)
        self.serverlabel.grid(column=0, row=0, sticky=N)

        self.mode = customtkinter.CTkEntry(self, placeholder_text='Mode:', width=250)
        self.mode.grid(column=0, row=1, sticky=N, padx=5)

        self.country = customtkinter.CTkEntry(self, placeholder_text='Country:', width=250)
        self.country.grid(column=0, row=2, sticky=N)

        self.prime = customtkinter.CTkEntry(self, placeholder_text='Prime (1 or 0):', width=250)
        self.prime.grid(column=0, row=3, sticky=N)

        self.players_count = customtkinter.CTkEntry(self, placeholder_text='Players count (num or expression):',
                                                    width=250)
        self.players_count.grid(column=0, row=4, sticky=N)

        self.maxplayers = customtkinter.CTkEntry(self, placeholder_text='Maxplayers (num or expression): ', width=250)
        self.maxplayers.grid(column=0, row=5, sticky=N)

        self.faceit_avg = customtkinter.CTkEntry(self, placeholder_text='Faceit avg (num or expression): ', width=250)
        self.faceit_avg.grid(column=0, row=6, sticky=N)

        self.faceit_limiter_enable = customtkinter.CTkEntry(self, placeholder_text='Faceit limiter (1 or 0): ',
                                                            width=250)
        self.faceit_limiter_enable.grid(column=0, row=7, sticky=N)

        # Players
        self.playerlabel = customtkinter.CTkLabel(self, text='Players filters: ')
        self.playerlabel.grid(column=1, row=0, sticky=N)

        self.group = customtkinter.CTkEntry(self, placeholder_text='Group: ', width=250)
        self.group.grid(column=1, row=1, sticky=N, padx=5)

        self.name = customtkinter.CTkEntry(self, placeholder_text='Nickname: ', width=250)
        self.name.grid(column=1, row=2, sticky=N, padx=5)

        self.points = customtkinter.CTkEntry(self, placeholder_text='Points (num or expression): ', width=250)
        self.points.grid(column=1, row=3, sticky=N)

        self.player_country = customtkinter.CTkEntry(self, placeholder_text='Country: ', width=250)
        self.player_country.grid(column=1, row=4, sticky=N)

        self.faceit_level = customtkinter.CTkEntry(self, placeholder_text='Faceit level (num or expression): ',
                                                   width=250)
        self.faceit_level.grid(column=1, row=5, sticky=N)

        self.cybershoke_level = customtkinter.CTkEntry(self, placeholder_text='Cybershoke level (num or expression): ',
                                                       width=250)
        self.cybershoke_level.grid(column=1, row=6, sticky=N)

        self.steamid64 = customtkinter.CTkEntry(self, placeholder_text='SteamID64: ', width=250)
        self.steamid64.grid(column=1, row=7, sticky=N)

        self.kills = customtkinter.CTkEntry(self, placeholder_text='Kills (num or expression): ', width=250)
        self.kills.grid(column=1, row=8, sticky=N)

        self.headshots = customtkinter.CTkEntry(self, placeholder_text='Headshots (num or expression): ', width=250)
        self.headshots.grid(column=1, row=9, sticky=N)

        self.deaths = customtkinter.CTkEntry(self, placeholder_text='Deaths (num or expression): ', width=250)
        self.deaths.grid(column=1, row=10, sticky=N)

        self.time = customtkinter.CTkEntry(self, placeholder_text='Time (num or expression): ', width=250)
        self.time.grid(column=1, row=11, sticky=N)

        self.faceit_elo = customtkinter.CTkEntry(self, placeholder_text='Faceit elo (num or expression): ', width=250)
        self.faceit_elo.grid(column=1, row=12, sticky=N)

        self.rank = customtkinter.CTkEntry(self, placeholder_text='Rank (num or expression): ', width=250)
        self.rank.grid(column=1, row=13, sticky=N)


class OutputFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.output_label = customtkinter.CTkLabel(self, text='Output will be here', wraplength=400)
        self.output_label.pack(fill=BOTH)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        customtkinter.set_appearance_mode('dark')
        customtkinter.set_default_color_theme('dark-blue')

        self.title("CybershokeFinder")
        self.grid_columnconfigure((0, 1), weight=1)
        # self.iconphoto(True,
        #                PhotoImage(file='C:/Users/sasha/Projects/PyCharmProjects/CybershokeFinderV2/src/cybershoke.ico'))

        self.options_frame = OptionsFrame(self, width=300)
        self.options_frame.pack(anchor=N, side=LEFT)

        self.save_checkbox = customtkinter.CTkCheckBox(self, height=10, width=100, checkbox_width=10, border_width=1,
                                                       checkbox_height=10, text="Save to 'output.txt' file?")
        self.save_checkbox.place(x=80, rely=0.85, anchor=S)

        self.start_btn = customtkinter.CTkButton(master=self, command=self.start_btn, text='Start', height=10,
                                                 width=100)
        self.start_btn.place(x=70, rely=0.95, anchor=S)

        self.maximum = customtkinter.CTkEntry(self, placeholder_text='-1', height=15, width=30)
        self.maximum.place(x=140, rely=0.95, anchor=S)

    def start_btn(self):
        opt = self.options_frame
        prime = ''

        if opt.prime.get() == 1:
            prime = True
        elif opt.prime.get() == 0:
            prime = False

        filters = {'server': {
            'mode': opt.mode.get(),
            'country': opt.country.get(),
            'prime': opt.prime.get(),  # bool
            'players_count': opt.players_count.get(),  # int
            'maxplayers': opt.maxplayers.get(),  # int
            'status': 'Online',
            'faceit_avg': opt.faceit_avg.get(),  # int
            'faceit_limiter_enable': opt.faceit_limiter_enable.get()  # int
        }, 'players': {
            'group': opt.group.get(),
            'name': opt.name.get(),
            'points': opt.points.get(),  # int
            'country': opt.player_country.get(),
            'faceit_level': opt.faceit_level.get(),  # int
            'cybershoke_level': opt.cybershoke_level.get(),  # int
            'steamid64': opt.steamid64.get(),
            'kills': opt.kills.get(),  # int
            'headshots': opt.headshots.get(),  # int
            'deaths': opt.deaths.get(),  # int
            'time': opt.time.get(),  # int
            'FACEIT_elo': opt.faceit_elo.get(),  # int
            'rank': opt.rank.get()  # int
        }}

        maximum = -1 if (self.maximum.get() == '' or not (str(self.maximum.get()).isdigit())) else int(
            self.maximum.get())
        output_text = text_expressing(main(filters, maximum=maximum))

        window = customtkinter.CTkToplevel()
        window.title('CyberOutput')

        output_textbox = customtkinter.CTkTextbox(window, width=500, height=300)
        output_textbox.insert('0.0', output_text)
        output_textbox.pack(expand=True, fill=BOTH, side=LEFT)

        if self.save_checkbox.get():
            with open('CyberOutput.txt', 'w', encoding='utf-8') as f:
                f.write(output_text)


if __name__ == "__main__":
    app = App()
    app.mainloop()
