#pip install opencv-python

import cv2

# Inicializa a câmera
cap = cv2.VideoCapture(0)

# Função para definir a cor conforme a proximidade
def get_proximity_color(area):
    if area > 50000:  # Muito próximo
        return (0, 0, 255)    # Vermelho
    elif area > 25000:        # Médio próximo
        return (0, 255, 255)  # Amarelo
    else:                     # Distante
        return (0, 255, 0)    # Verde

while True:
    ret, frame = cap.read()
    if not ret:
        print("Falha ao capturar imagem.")
        break

    # Converte para escala de cinza e aplica um leve blur
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Limiarização para identificar contornos
    _, thresh = cv2.threshold(blurred, 70, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Identificação e filtragem de contornos
    for contour in contours:
        area = cv2.contourArea(contour)
        
        # Filtro adicional: Contornos grandes no centro da imagem
        if area > 2000:
            x, y, w, h = cv2.boundingRect(contour)
            center_x = x + w // 2
            frame_center = frame.shape[1] // 2

            # Dá prioridade a contornos próximos ao centro
            if frame_center - 100 < center_x < frame_center + 100:
                color = get_proximity_color(area)
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

                # Exibe uma mensagem visual de proximidade
                label = "Muito Perto!" if color == (0, 0, 255) else "Ande com Cuidado" if color == (0, 255, 255) else "Pode Mover"
                cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    # Exibe o frame processado
    cv2.imshow('Proximity Detection', frame)

    # Sair ao pressionar 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera a câmera e fecha as janelas
cap.release()
cv2.destroyAllWindows()
