import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import subprocess
from GuardarRostro import save_face_images
from index import face
from DetectarObjeto import cap_object


class FaceRecognitionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Reconocimiento")
        self.root.configure(bg="#F4F6F7")
        self.root.geometry("500x450")

        title = tk.Label(
            root,
            text="Sistema de Reconocimiento",
            font=("Arial", 18, "bold"),
            bg="#F4F6F7",
            fg="#1C1832"
        )
        title.pack(pady=20)

        main_frame = tk.Frame(root, bg="#F4F6F7")
        main_frame.pack(pady=10)

        self.create_button(main_frame, "📷 Registrar rostro", self.register_face, "#A3E4D7").pack(pady=10)
        self.create_button(main_frame, "🙂 Reconocer rostro", self.recognize_face, "#AED6F1").pack(pady=10)
        self.create_button(main_frame, "🎯 Reconocer objetos", self.recognize_object, "#F9E79F").pack(pady=10)

        self.status = tk.Label(root, text="Listo", anchor="w", bg="#D5DBDB", fg="black")
        self.status.pack(fill="x", side="bottom")

    def create_button(self, parent, text, command, color):

        btn = tk.Button(
            parent,
            text=text,
            command=command,
            font=("Arial", 12, "bold"),
            width=22,
            height=2,
            bg=color,
            fg="black",
            relief="flat"
        )
        btn.bind("<Enter>", lambda e: btn.config(bg="#1C1832", fg="white"))
        btn.bind("<Leave>", lambda e: btn.config(bg=color, fg="black"))
        return btn

    def register_face(self):
        self.status.config(text="Abriendo registro de rostro...")
        top = tk.Toplevel(self.root)
        top.title("Registrar Rostro")
        top.geometry("400x350")
        top.configure(bg="#F4F6F7")

        tk.Label(top, text="Nombre:", font=("Arial", 12), bg="#F4F6F7").pack(pady=5)
        name_entry = tk.Entry(top, font=("Arial", 12))
        name_entry.pack(pady=5)

        tk.Label(top, text="(Opcional) Seleccionar video:", font=("Arial", 12), bg="#F4F6F7").pack(pady=5)
        video_entry = tk.Entry(top, font=("Arial", 12))
        video_entry.pack(pady=5)

        tk.Button(top, text="Examinar", command=lambda: self.select_file(video_entry)).pack(pady=5)

        tk.Button(top, text="Registrar", bg="#A3E4D7",
                  command=lambda: self.register_face_camera(name_entry.get(), video_entry.get())).pack(pady=15)

    def select_file(self, entry):
        file_path = filedialog.askopenfilename()
        if file_path:
            entry.delete(0, tk.END)
            entry.insert(tk.END, file_path)

    def register_face_camera(self, person_name, video_path=None):
        if person_name:
            if video_path:
                save_face_images(person_name, video_path)
            else:
                save_face_images(person_name)
            messagebox.showinfo("Registro", f"Se registró el rostro de {person_name}")
            self.status.config(text="Entrenando modelo...")
            subprocess.call(['python', 'Entrenar.py'])
            self.status.config(text="Modelo entrenado con éxito")
        else:
            messagebox.showwarning("Registro", "Ingrese un nombre válido")

    def recognize_face(self):
        self.status.config(text="Reconociendo rostro...  (q para salir)")
        file_path = filedialog.askopenfilename()
        face(file_path if file_path else None)
        self.status.config(text="Listo")

    def recognize_object(self):
        self.status.config(text="Reconociendo objetos... (q para salir)")
        file_path = filedialog.askopenfilename()
        cap_object(file_path if file_path else None)
        self.status.config(text="Listo")


if __name__ == "__main__":
    root = tk.Tk()
    app = FaceRecognitionApp(root)
    root.mainloop()
