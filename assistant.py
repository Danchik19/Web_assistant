import words
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression


class Assistant:
    def __init__(self, message: str="") -> None:
        self.message = message
        self.vectorizer = CountVectorizer()
        self.vectors = self.vectorizer.fit_transform(list(words.data_set.keys()))
        self.clf = LogisticRegression()
        self.clf.fit(self.vectors, list(words.data_set.values()))
    
    def GetAnswer(self) -> str:
        """
        Метод возвращает ответ на запрос пользователя.
        """

        good = self.ProcessingMessage(self.message, self.vectorizer, self.clf)
        answer = good if good else "error Я не знаю такой команды("
            
        return answer

    def ProcessingMessage(self, data: str, vectorizer: CountVectorizer, clf: LogisticRegression) -> str:
        """
        Метод преобразует команду пользователя в числовой вектор.
        Предсказывает вероятности принадлежности к каждому классу.
        Выбирает ответ из data_set (words.py),
        если наибольшая вероятность превышает заданный порог.
        """

        user_vector = vectorizer.transform([data])
        predicted_probabilities = clf.predict_proba(user_vector)

        threshold = 0.2

        max_probability = max(predicted_probabilities[0])
        answer = ""
        if max_probability >= threshold:
            answer = clf.classes_[predicted_probabilities[0].argmax()]
        
        return answer

if __name__ == "__main__":
    obj = Assistant("привет")
    print(obj.GetAnswer())
