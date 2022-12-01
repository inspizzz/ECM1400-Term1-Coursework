import tkinter as tk


class Display(tk.Tk):
	def __init__(self) -> None:
		super().__init__()
		# self.WIDTH = 1000
		# self.HEIGHT = 1000

		# self.geometry(f"{self.WIDTH}x{self.HEIGHT}")
		self.title("display")
		self.protocol("WM_DELETE_WINDOW", self.close)

		self.running = True

	def show(self):
		self.image = tk.PhotoImage(file="london.gif")

		tk.Label(self, image=self.image).pack()


	def close(self):
		self.running = False

	def Update(self):
		while self.running:
			self.update()
			self.update_idletasks()


if __name__ == "__main__":
	disp = Display()
	disp.show()
	disp.Update()

	# root = tk.Tk()
	# image = tk.PhotoImage(file="london.gif")
	# tk.Label(root, image=image).pack()
	# root.mainloop()