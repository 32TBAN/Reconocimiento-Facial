import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import subprocess
from GuardarRostro import save_face_images
from index import face

class FaceRecognitionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Reconocimiento Facial")

        self.label = tk.Label(root, text="Seleccione una opción:", font=("Arial", 14))
        self.label.pack(pady=20)

        self.register_button = tk.Button(root, text="Registrar rostro", command=self.register_face, width=20, height=2, font=("Arial", 12))
        self.register_button.pack(pady=10)

        self.recognize_button = tk.Button(root, text="Reconocer rostro", command=self.recognize_face, width=20, height=2, font=("Arial", 12))
        self.recognize_button.pack(pady=10)

    def register_face(self):
        top = tk.Toplevel()  # Crea una nueva ventana
        top.title("Opciones de Registro")
        top.geometry("400x400")
        
        label = tk.Label(top, text="Ingrese su nombre:", font=("Arial", 14))
        label.pack(pady=10)

        name_entry = tk.Entry(top, font=("Arial", 12))
        name_entry.pack(pady=5)

        register_button = tk.Button(top, text="Camara", command=lambda: self.register_face_camera(name_entry.get()), width=20, height=2, font=("Arial", 12))
        register_button.pack(pady=10)


        def select_file():
            file_path = filedialog.askopenfilename() 
            video_entry.delete(0, tk.END) 
            video_entry.insert(tk.END, file_path) 

        browse_button = tk.Button(top, text="Seleccionar Video", command=select_file, width=20, height=2, font=("Arial", 12))
        browse_button.pack(pady=10)
    
        video_entry = tk.Entry(top, font=("Arial", 12))
        video_entry.pack(pady=5)

        register_button_video = tk.Button(top, text="Registrar", command=lambda: self.register_face_camera(name_entry.get(),video_entry.get()), width=20, height=2, font=("Arial", 12))
        register_button_video.pack(pady=10)

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

if __name__ == "__main__":
    root = tk.Tk()
    app = FaceRecognitionApp(root)
    root.geometry("400x400") 
    root.mainloop()
