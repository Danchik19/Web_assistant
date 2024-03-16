import words
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

def there_is_trigger(data):
    """
    Функция проверяет наличие имени помощника в запросе.
    """

    trg = words.TRIGGERS.intersection(data.split())
    return trg


def get_answer(data, vectorizer, clf):
    """
    Функция преобразует команду пользователя в числовой вектор.
    Предсказывает вероятности принадлежности к каждому классу.
    Выбирает ответ из data_set (words.py),
    если наибольшая вероятность превышает заданный порог.
    """

    data = data.split()
    filtered_data = [word for word in data if word not in words.TRIGGERS]
    data = " ".join(filtered_data)

    user_vector = vectorizer.transform([data])
    predicted_probabilities = clf.predict_proba(user_vector)

    threshold = 0.2

    max_probability = max(predicted_probabilities[0])
    if max_probability >= threshold:
        answer = clf.classes_[predicted_probabilities[0].argmax()]
    else:
        answer = False
    
    return answer


def punct_marks(data):
    """
    Функция расставляет знаки препинания в запросе.
    """
    
    edit_data = data

    return edit_data


def main(message):
    """
    Функция принимает запрос и возвращает ответ
    """

    vectorizer = CountVectorizer()
    vectors = vectorizer.fit_transform(list(words.data_set.keys()))

    clf = LogisticRegression()
    clf.fit(vectors, list(words.data_set.values()))

    answer = "error Пожалуйста, обратись ко мне по имени)"
    if there_is_trigger(message):
        good = get_answer(message, vectorizer, clf)
        answer = good if good else "error Я не знаю такой команды("
        
    return answer


if __name__ == "__main__":
    main()
