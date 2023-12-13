from transformers import BertTokenizer, BertForSequenceClassification
from torch.nn.functional import softmax
import torch


# Cargar el modelo y el tokenizador para el español
model_name = 'nlptown/bert-base-multilingual-uncased-sentiment'
model = BertForSequenceClassification.from_pretrained(model_name)
tokenizer = BertTokenizer.from_pretrained(model_name)

# Función para analizar el sentimiento de un texto
def analizar_sentimiento(texto):
    tokens = tokenizer(texto, return_tensors='pt')
    with torch.no_grad():
        outputs = model(**tokens)
    probs = softmax(outputs.logits, dim=1)
    return probs

# Ejemplo de texto en español
texto_ejemplo = "Hoy es el mejor dia de mi vida, tengo amigos, dinero y la despensa llena."

# Analizar el sentimiento
probabilidades = analizar_sentimiento(texto_ejemplo)

# Imprimir las probabilidades asociadas a cada clase
etiquetas_clases = ['Muy negativo', 'Negativo', 'Neutral', 'Positivo', 'Muy positivo']
for etiqueta, prob in zip(etiquetas_clases, probabilidades[0]):
    print(f'{etiqueta}: {prob.item():.4f}')
