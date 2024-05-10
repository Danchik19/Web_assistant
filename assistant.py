import words
from skills import Skills
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression


class Assistant:
    _vectorizer = CountVectorizer()
    _vectors = _vectorizer.fit_transform(list(words.data_set.keys()))
    _clf = LogisticRegression()
    _clf.fit(_vectors, list(words.data_set.values()))

    def __init__(self, message: str, params: dict[str, str]) -> None:
        self.message = message
        self.params = params
    
    def GetAnswer(self) -> str:
        """
        Метод возвращает ответ на запрос пользователя.
        """

        answer = self.ProcessingMessage(self.message, self._vectorizer, self._clf)
        skill = Skills(self.message, answer, self.params)

        return skill.MakeRequest()

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
        answer = "nothing"
        if max_probability >= threshold:
            answer = clf.classes_[predicted_probabilities[0].argmax()]

        return answer

if __name__ == "__main__":
    obj = Assistant("Какая в Москве погода")
    print(obj.GetAnswer())
