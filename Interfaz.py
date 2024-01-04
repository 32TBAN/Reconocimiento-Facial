import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import subprocess
from GuardarRostro import save_face_images
from index import face
from DetectarObjeto import cap_object

class FaceRecognitionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Reconocimiento Facial")

        self.root.configure(bg="#CBE1CC") 

        window_width = 400
        window_height = 400
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.label = tk.Label(root, text="Seleccione una opción:", font=("Arial", 14),bg="#CBE1CC")
        self.label.pack(pady=20)

        self.register_button = tk.Button(root, text="Registrar rostro", command=self.register_face, width=20, height=2, font=("Arial", 12),
                                        bg="#FEECD9", fg="black", relief="flat", borderwidth=0)
        self.register_button.pack(pady=10)
        self.register_button.bind("<Enter>", lambda event: self.register_button.config(bg="#1C1832", fg="white"))
        self.register_button.bind("<Leave>", lambda event: self.register_button.config(bg="#FEECD9", fg="black"))

        self.recognize_button = tk.Button(root, text="Reconocer rostro", command=self.recognize_face, width=20, height=2, font=("Arial", 12), 
                                        bg="#F2F2F2", fg="black", relief="flat", borderwidth=0)
        self.recognize_button.pack(pady=10)
        self.recognize_button.bind("<Enter>", lambda event: self.recognize_button.config(bg="#1C1832", fg="white"))
        self.recognize_button.bind("<Leave>", lambda event: self.recognize_button.config(bg="#F2F2F2", fg="black"))

        self.recognize2_button = tk.Button(root, text="Reconocer objetos", command=self.recognize_object, width=20, height=2, font=("Arial", 12), 
                                        bg="#FEECD9", fg="black", relief="flat", borderwidth=0)
        self.recognize2_button.pack(pady=10)
        self.recognize2_button.bind("<Enter>", lambda event: self.recognize2_button.config(bg="#1C1832", fg="white"))
        self.recognize2_button.bind("<Leave>", lambda event: self.recognize2_button.config(bg="#FEECD9", fg="black"))

    def register_face(self):
        self.root.withdraw() 
        top = tk.Toplevel()  # Crea una nueva ventana
        top.title("Opciones de Registro")
        top.geometry("400x400")
        top.configure(bg="#CBE1CC") 

        window_width = 400
        window_height = 400
        screen_width = top.winfo_screenwidth()
        screen_height = top.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        top.geometry(f"{window_width}x{window_height}+{x}+{y}")

        label = tk.Label(top, text="Ingrese su nombre:", font=("Arial", 14),bg="#CBE1CC")
        label.pack(pady=10)

        name_entry = tk.Entry(top, font=("Arial", 12))
        name_entry.pack(pady=5)

        register_button = tk.Button(top, text="Camara", command=lambda: self.register_face_camera(name_entry.get()), width=20, height=2,
                                    font=("Arial", 12),bg="#E3EDF9", fg="black", relief="flat", borderwidth=0)
        register_button.pack(pady=10)
        register_button.bind("<Enter>", lambda event: register_button.config(bg="#1C1832", fg="white"))
        register_button.bind("<Leave>", lambda event: register_button.config(bg="#E3EDF9", fg="black"))

        def select_file():
            file_path = filedialog.askopenfilename() 
            video_entry.delete(0, tk.END) 
            video_entry.insert(tk.END, file_path) 

        browse_button = tk.Button(top, text="Seleccionar Video", command=select_file, width=20, height=2, font=("Arial", 12),
                                bg="#FFFFFF", fg="black", relief="flat", borderwidth=0)
        browse_button.pack(pady=10)
        browse_button.bind("<Enter>", lambda event: browse_button.config(bg="#1C1832", fg="white"))
        browse_button.bind("<Leave>", lambda event: browse_button.config(bg="#FFFFFF", fg="black"))

        video_entry = tk.Entry(top, font=("Arial", 12))
        video_entry.pack(pady=5)

        register_button_video = tk.Button(top, text="Registrar", command=lambda: self.register_face_camera(name_entry.get(),video_entry.get()), 
                                        width=20, height=2, font=("Arial", 12),bg="#FEECD9", fg="black", relief="flat", borderwidth=0)
        register_button_video.pack(pady=10)
        register_button_video.bind("<Enter>", lambda event: register_button_video.config(bg="#1C1832", fg="white"))
        register_button_video.bind("<Leave>", lambda event: register_button_video.config(bg="#FEECD9", fg="black"))

        def close_register_window():
            top.destroy()  # Cierra la ventana de registro
            self.root.deiconify()  # Muestra la ventana principal nuevamente

        top.protocol("WM_DELETE_WINDOW", close_register_window) 

    def register_face_camera(self, person_name,video_path=None):
        if person_name:
            if video_path:
                save_face_images(person_name, video_path)
            else:
                save_face_images(person_name)
            messagebox.showinfo("Registrar rostro", f"Se ha registrado el rostro de {person_name}")
            script_path = 'Entrenar.py'
            subprocess.call(['python', script_path])
        else:
            messagebox.showwarning("Registrar rostro", "Ingrese un nombre válido")

    def recognize_face(self):
        file_path = filedialog.askopenfilename()  
        if file_path:
            face(file_path)
        else:
            face()

    def recognize_object(self):
        file_path = filedialog.askopenfilename()  
        if file_path:
            cap_object(file_path)
        else:
            cap_object()

if __name__ == "__main__":
    root = tk.Tk()
    app = FaceRecognitionApp(root)
    root.geometry("400x400") 
    root.mainloop()
