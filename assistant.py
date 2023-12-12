import queue
import vosk
import json
import words
import voice
import sounddevice as sd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from skills import *


q = queue.Queue()

model = vosk.Model('vosk_model')

device = sd.default.device
samplerate = int(sd.query_devices(device[0], 'input')['default_samplerate'])

def callback(indata, frames, time, status):
    q.put(bytes(indata))

def recognize(data, vectorizer, clf):
    trg = words.TRIGGERS_MAN.intersection(data.split())
    if not trg:
        return
    
    # Удаляем имя ассистента, если мы к нему обратились
    data = data.split()
    filtered_data = [word for word in data if word not in words.TRIGGERS_MAN]
    data = ' '.join(filtered_data)

    # Преобразуем команду пользователя в числовой вектор
    user_vector = vectorizer.transform([data])

    # Предсказание вероятностей принадлежности к каждому классу
    predicted_probabilities = clf.predict_proba(user_vector)

    # Задание порога совпадения
    threshold = 0.2

    # Поиск наибольшей вероятности и выбор ответа, если превышает порог
    max_probability = max(predicted_probabilities[0])
    if max_probability >= threshold:
        answer = clf.classes_[predicted_probabilities[0].argmax()]
    else:
        voice.speaker_silero('Я пока не знаю такой команды, но ты можешь меня научить ей')
        return
    
    # Получаем имя функции из ответа data_set
    func_name = answer.split()[0]

    # Озвучиваем ответ из data_set
    voice.speaker_silero(answer.replace(func_name, ''))

    # Вызываем функцию по запросу
    exec(func_name + '()')

def main():
    vectorizer = CountVectorizer()
    vectors = vectorizer.fit_transform(list(words.data_set.keys()))

    clf = LogisticRegression()
    clf.fit(vectors, list(words.data_set.values()))

    del words.data_set

    with sd.RawInputStream(samplerate=samplerate, blocksize = 16000, device=device,
                dtype="int16", channels=1, callback=callback):

        rec = vosk.KaldiRecognizer(model, samplerate)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                data = json.loads(rec.Result())['text']
                recognize(data, vectorizer, clf)
            #else:
            #    print(rec.PartialResult())

if __name__ == '__main__':
    main()