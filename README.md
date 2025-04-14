Nome do sistema: EagleEyes | Reconhecimento Facial em Vídeo com Interface Gráfica

Descrição geral:
 
Este sistema permite ao usuário selecionar imagens de treinamento (rostos conhecidos) e aplicar reconhecimento facial em um vídeo, destacando os rostos encontrados e nomeando-os conforme os dados treinados. Todo o processo é feito por meio de uma interface gráfica desenvolvida com CustomTkinter.
____________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________
Tecnologias Utilizadas:
Python


OpenCV – manipulação de vídeo e frames


Face Recognition – detecção e reconhecimento facial


CustomTkinter – interface gráfica estilizada


Pillow – manipulação de imagens


Threading – execução em paralelo para não travar a interface


____________________________________________________________________________________________________________________________________________________________________________________________________________________
Fluxo do Sistema:

Selecionar imagens de treino
 ➜ Usuário escolhe imagens que contêm os rostos conhecidos.


Selecionar vídeo para processamento
 ➜ Vídeo onde os rostos serão detectados.


Executar processamento
 ➜ Roda o algoritmo de reconhecimento facial em cada frame:


Detecta rostos


Compara com os rostos das imagens de treino


Nomeia (ou marca como "Desconhecido")


Atualiza a interface com preview ao vivo


Exibir resultado
 ➜ Mostra o vídeo processado diretamente na interface.


Salvar vídeo final
 ➜ Permite exportar o resultado em .mp4.

(Será adicionado um Fluxograma Visual na pasta do trabalho)

________________________________________________________________________________________________________________
Resumo por partes

1. Imports e configuração

➜Importa bibliotecas como cv2, face_recognition, PIL, tkinter, customtkinter, etc.


➜Configura a aparência da interface em modo escuro (dark).


➜Cria pastas onde vão ficar: imagens de treino, uploads e resultados.


________________________________________________________________________________________________________________
 2. Interface gráfica

➜Cria a janela principal com layout moderninho.


➜Define fontes e um frame bonitão com imagem de fundo.


➜Define variáveis pra guardar o caminho do vídeo e a proporção do vídeo.


________________________________________________________________________________________________________________
3. Funções principais

➜➜carregar_faces_conhecidos()
 Lê as imagens da pasta de treino e extrai os "encodings" (características do rosto).


➜➜selecionar_imagens()
 Permite o usuário selecionar imagens do PC e salva na pasta treino.


➜➜selecionar_video()
 Escolhe um vídeo do PC e guarda o caminho.


➜➜processar_video()
 Lê frame por frame do vídeo, detecta rostos, compara com os conhecidos e desenha retângulos + nomes. Salva um novo vídeo em resultado/output.mp4.


➜➜exibir_video_final()
 Mostra o vídeo processado na interface, frame por frame.


➜➜salvar_video()
 Abre uma janela pra escolher onde salvar o vídeo final.


➜➜executar_processamento()
 Junta tudo: carrega rostos, processa vídeo e exibe o resultado. Roda isso em uma thread separada pra interface não travar.


________________________________________________________________________________________________________________
Botões e Labels
Três botões principais:


➜Escolher imagens de treino


➜Selecionar vídeo


➜Iniciar processamento


➜Um botão de salvar (só fica ativo depois do processamento).


➜Labels para status e vídeo.

