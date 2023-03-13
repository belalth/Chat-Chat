from pathlib import Path
import threading
from tkinter import messagebox, Tk, Canvas, Text, Button, PhotoImage
from Socket import Socket


class Gui:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.username = None
        self.gui_ready = False
        self.socket = Socket(self.server_ip, self.server_port)

        try:
            self.socket.connect()
            self.mini_win()
            self.clients_list = self.socket.receive()[12:]

        except Exception as e:
            messagebox.showerror("Error Connection")
            print(e)
            exit(1)

        gui_thread = threading.Thread(target=self.gui)
        receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
        receive_thread.start()
        gui_thread.start()

    def mini_win(self):
        output_path = Path(__file__).parent
        assets_path = output_path / Path(r"assets/frame1")

        def relative_to_assets(path: str) -> Path:
            return assets_path / Path(path)

        self.login_gui = Tk()
        self.login_gui.geometry("533x300")
        self.login_gui.configure(bg="#FFFFFF")

        canvas = Canvas(
            self.login_gui,
            bg="#FFFFFF",
            height=300,
            width=533,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        canvas.place(x=0, y=0)

        image_image_1 = PhotoImage(
            file=relative_to_assets("image_1.png"))
        canvas.create_image(
            266.0,
            150.0,
            image=image_image_1
        )

        entry_image_1 = PhotoImage(
            file=relative_to_assets("entry_1.png"))
        canvas.create_image(
            262.0,
            158.0,
            image=entry_image_1
        )
        self.entry_1 = Text(
            font=("Arial", 15),
            bd=0,
            bg="#F0E5DC",
            fg="#000716",
            highlightthickness=0
        )
        self.entry_1.place(
            x=134.0,
            y=143.0,
            width=256.0,
            height=48.0
        )

        canvas.create_rectangle(
            0.0,
            63.0,
            539.0,
            116.0,
            fill="#A5876B",
            outline="")

        button_image_1 = PhotoImage(
            file=relative_to_assets("button_1.png"))
        self.button_1 = Button(
            image=button_image_1,
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
            command=lambda: self.get_result()
        )
        self.button_1.place(
            x=195.0,
            y=194.0,
            width=138.0,
            height=50.0
        )

        canvas.create_text(
            74.0,
            72.0,
            anchor="nw",
            text="Please Enter your Username",
            fill="#F9F0E8",
            font=("Itim Regular", 30 * -1)
        )
        self.login_gui.bind('<Return>', lambda event: self.button_1.invoke())

        self.login_gui.protocol("WM_DELETE_WINDOW", self.get_result)
        self.login_gui.resizable(False, False)
        self.login_gui.mainloop()

    def get_result(self):
        self.username = self.entry_1.get("1.0", "end-1c").strip()
        if self.username != "":
            self.login_gui.destroy()
            self.socket.send(self.username)

    def gui(self):
        OUTPUT_PATH = Path(__file__).parent
        ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame0")

        def relative_to_assets(path: str) -> Path:
            return ASSETS_PATH / Path(path)

        self.window = Tk()
        self.window.geometry("700x500")
        self.window.configure(bg="#FFFFFF")

        self.canvas = Canvas(
            self.window,
            bg="#FFFFFF",
            height=500,
            width=700,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )

        self.canvas.place(x=0, y=0)
        image_image_1 = PhotoImage(
            file=relative_to_assets("image_1.png"))
        self.canvas.create_image(
            350.0,
            252.0,
            image=image_image_1
        )

        entry_image_1 = PhotoImage(
            file=relative_to_assets("entry_1.png"))
        self.canvas.create_image(
            351.5,
            266.0,
            image=entry_image_1
        )
        self.text_area = Text(
            state="disabled",
            bd=0,
            bg="#F8F0E8",
            fg="#000716",
            highlightthickness=0
        )
        self.text_area.place(
            x=69.0,
            y=101.0,
            width=565.0,
            height=328.0
        )

        entry_image_2 = PhotoImage(
            file=relative_to_assets("entry_2.png"))
        self.canvas.create_image(
            287.0,
            463.0,
            image=entry_image_2
        )
        self.message_text_field = Text(
            bd=0,
            bg="#F3DDC9",
            fg="#000716",
            highlightthickness=0
        )
        self.message_text_field.place(
            x=46.0,
            y=450.0,
            width=482.0,
            height=48.0
        )

        self.canvas.create_rectangle(
            0.0,
            0.0,
            700.0,
            53.0,
            fill="#A5876B",
            outline="")

        button_image_1 = PhotoImage(
            file=relative_to_assets("button_1.png"))
        self.button_send = Button(
            image=button_image_1,
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
            command=lambda: (self.socket.send(self.username + ":" + " " + self.message_text_field.get("1.0", "end-1c").strip())
                             , self.message_text_field.delete("1.0", "end-1c"))

        )
        self.window.bind('<Return>', lambda event: self.button_send.invoke())

        self.button_send.place(
            x=554.0,
            y=438.0,
            width=138.0,
            height=50.0
        )

        self.canvas.create_text(
            58.0,
            4.0,
            anchor="nw",
            text=f"Hi {self.username} ! Enjoy Chatting  :)",
            fill="#F9F0E8",
            font=("Arial", 30 * -1)
        )

        image_image_2 = PhotoImage(
            file=relative_to_assets("image_2.png"))
        self.canvas.create_image(
            31.0,
            28.0,
            image=image_image_2
        )

        self.canvas.create_rectangle(
            81.0,
            59.0,
            620.0,
            92.0,
            fill="#F4DECA",
            outline="")
        self.active_users = self.canvas.create_text(
            180.0,
            65.0,
            text=self.clients_list,
            anchor="nw",
            fill="#05B113",
            font=("Itim Regular", 20 * -1)
        )
        self.gui_ready = True
        self.window.protocol("WM_DELETE_WINDOW", self.kill)
        self.window.resizable(False, False)
        self.window.mainloop()

    def receive_messages(self):
        while True:
            try:
                message = self.socket.receive()
                if self.gui_ready:
                    if message.startswith("CLIENTS_LIST"):
                        self.clients_list = message[12:]
                        self.canvas.itemconfigure(self.active_users, text=self.clients_list)

                    else:
                        self.text_area.configure(state='normal')
                        self.text_area.insert("end", message)
                        self.text_area.insert("end", '\n')
                        self.text_area.configure(state='disabled')
                        self.text_area.see("end")

            except Exception as e:
                print(e)
                self.kill()

    def kill(self):
        self.socket.close()
        self.window.destroy()
        exit(1)


if __name__ == "__main__":
    Gui("localhost", 7000)
