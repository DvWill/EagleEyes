import os
import cv2
import face_recognition
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import shutil
from threading import Thread
from time import sleep
import customtkinter as ctk
from customtkinter import CTkFont, CTkImage

# Inicializar a janela do CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Cria pastas necessárias
os.makedirs("treino", exist_ok=True)
os.makedirs("uploads", exist_ok=True)
os.makedirs("resultado", exist_ok=True)

# Variáveis globais
pausado = False
proporcao_video = (800, 450)  # Valor padrão

# Janela principal
janela = ctk.CTk()
janela.title("Reconhecimento Facial em Vídeo")
janela.geometry("1000x750")
janela_font = CTkFont(family="Orbitron", size=16)

# Frame principal
frame = ctk.CTkFrame(janela, corner_radius=10)
frame.pack(expand=True, fill="both", padx=20, pady=20)

# Fundo
try:
    imagem_fundo = Image.open("logo.png").convert("RGBA")
    imagem_ctk = CTkImage(light_image=imagem_fundo, size=(1250, 750))
    fundo_label = ctk.CTkLabel(master=frame, image=imagem_ctk, text="")
    fundo_label.place(x=0, y=0, relwidth=1, relheight=1)
except Exception as e:
    print(f"[AVISO] Erro ao carregar imagem de fundo: {e}")

# Variáveis
video_path_var = tk.StringVar()

# Barra de progresso
progress_bar = ctk.CTkProgressBar(frame, width=400)
progress_bar.set(0)
progress_bar.pack(pady=5)

# Botão pausa
def toggle_pausar():
    global pausado
    pausado = not pausado
    pausar_btn.configure(text="Continuar" if pausado else "Pausar")

pausar_btn = ctk.CTkButton(frame, text="Pausar", command=toggle_pausar,
                           fg_color="gray", text_color="white", width=250, font=janela_font, state="disabled")
pausar_btn.pack(pady=5)

# Status
status_label = ctk.CTkLabel(frame, text="Aguardando ações...", text_color="white", font=janela_font)
status_label.pack(pady=10)

# Área de vídeo
video_label = ctk.CTkLabel(frame, text="")
video_label.pack(pady=10)

# Funções
def carregar_faces_conhecidos(pasta_treino="treino"):
    encodings, nomes = [], []
    for nome_arquivo in os.listdir(pasta_treino):
        caminho = os.path.join(pasta_treino, nome_arquivo)
        imagem = face_recognition.load_image_file(caminho)
        try:
            encoding = face_recognition.face_encodings(imagem)[0]
            encodings.append(encoding)
            nomes.append(os.path.splitext(nome_arquivo)[0])
        except IndexError:
            print(f"[AVISO] Nenhum rosto encontrado em {nome_arquivo}")
    return encodings, nomes

def selecionar_imagens():
    caminhos = filedialog.askopenfilenames(title="Escolha imagens de treino")
    if caminhos:
        if os.path.exists("treino"):
            shutil.rmtree("treino")
        os.makedirs("treino", exist_ok=True)
        for img in caminhos:
            shutil.copy(img, "treino")
        status_label.configure(text=f"{len(caminhos)} imagem(ns) adicionada(s) para treino.")

def selecionar_video():
    caminho = filedialog.askopenfilename(title="Escolha o vídeo")
    if caminho:
        video_path_var.set(caminho)
        status_label.configure(text="Vídeo selecionado.")

def processar_video(caminho_video, encodings, nomes):
    global pausado
    cap = cv2.VideoCapture(caminho_video)
    nome_saida = "resultado/output.mp4"

    largura = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    altura = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    codec = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(nome_saida, codec, fps, (largura, altura))

    frame_count = 0
    progress_bar.set(0)
    pausar_btn.configure(state="normal")

    while True:
        if pausado:
            sleep(0.1)
            janela.update()
            continue

        ret, frame = cap.read()
        if not ret:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        locais_rostos = face_recognition.face_locations(rgb_frame)
        encodings_rostos = face_recognition.face_encodings(rgb_frame, locais_rostos)

        for (top, right, bottom, left), encoding_rosto in zip(locais_rostos, encodings_rostos):
            comparacoes = face_recognition.compare_faces(encodings, encoding_rosto)
            nome = "Desconhecido"
            if True in comparacoes:
                primeiro_match = comparacoes.index(True)
                nome = nomes[primeiro_match]

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, nome, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        out.write(frame)

        # Exibir frame na interface
        frame_redimensionado = cv2.resize(frame, proporcao_video)
        img = Image.fromarray(cv2.cvtColor(frame_redimensionado, cv2.COLOR_BGR2RGB))
        imgtk = CTkImage(light_image=img, size=proporcao_video)
        video_label.configure(image=imgtk)
        video_label.image = imgtk

        # Atualizar progresso
        frame_count += 1
        progresso = frame_count / total_frames
        progress_bar.set(progresso)

        janela.update_idletasks()
        janela.update()

    cap.release()
    out.release()
    pausar_btn.configure(state="disabled")
    return nome_saida

def exibir_video_final(caminho_video):
    cap = cv2.VideoCapture(caminho_video)

    def atualizar_frame():
        ret, frame = cap.read()
        if not ret:
            cap.release()
            status_label.configure(text="Vídeo finalizado.")
            return

        frame = cv2.resize(frame, proporcao_video)
        img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        imgtk = CTkImage(light_image=img, size=proporcao_video)
        video_label.configure(image=imgtk)
        video_label.image = imgtk
        video_label.after(30, atualizar_frame)

    atualizar_frame()

def salvar_video():
    caminho = "resultado/output.mp4"
    if os.path.exists(caminho):
        destino = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")])
        if destino:
            shutil.copy(caminho, destino)
            messagebox.showinfo("Sucesso", f"Vídeo salvo em {destino}")
    else:
        messagebox.showerror("Erro", "Nenhum vídeo processado ainda.")

def executar_processamento():
    def tarefa():
        caminho_video = video_path_var.get()
        if not caminho_video or not os.listdir("treino"):
            messagebox.showwarning("Aviso", "Adicione imagens de treino e selecione um vídeo!")
            return

        status_label.configure(text="Processando vídeo...")
        encodings, nomes = carregar_faces_conhecidos()
        caminho_resultado = processar_video(caminho_video, encodings, nomes)

        status_label.configure(text="Exibindo resultado final...")
        exibir_video_final(caminho_resultado)

        salvar_btn.configure(state="normal")

    Thread(target=tarefa).start()

# Título
ctk.CTkLabel(frame, text="Reconhecimento Facial em Vídeo", font=janela_font).pack(pady=15)

# Botões
ctk.CTkButton(frame, text="Selecionar Imagens de Treino", command=selecionar_imagens,
              fg_color="black", text_color="white", width=250, font=janela_font).pack(pady=10)

ctk.CTkButton(frame, text="Selecionar Vídeo", command=selecionar_video,
              fg_color="black", text_color="white", width=250, font=janela_font).pack(pady=5)

ctk.CTkButton(frame, text="Iniciar Processamento", command=executar_processamento,
              fg_color="#ff00ff", text_color="white", hover_color="#ff33ff", width=250, font=janela_font).pack(pady=15)

salvar_btn = ctk.CTkButton(frame, text="Salvar Vídeo", command=salvar_video,
                           fg_color="#444", text_color="white", width=250, font=janela_font, state="disabled")
salvar_btn.pack(pady=10)

# Loop principal
janela.mainloop()
