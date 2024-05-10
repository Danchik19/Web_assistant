from datetime import datetime as dt
from bs4 import BeautifulSoup as bs
from translate import Translator
import locale
import requests
import spacy
import ipapi


class Skills:
    _translator = Translator(from_lang="en", to_lang="ru")
    _nlp = spacy.load("ru_core_news_lg")
    _result = ""

    def __init__(self, message: str, funcs: str, params: dict[str, str]) -> None:
        self.doc = self._nlp(message)
        self.lst_funcs = funcs.split()
        self.params = params
        
    def MakeRequest(self):
        """
        Метод вызывает нужную функцию обработки запроса пользователя и
        возвращает её результат.
        """

        match self.lst_funcs:
            case FuncMain, FuncAdd:
                exec(f"self.{FuncMain}('{FuncAdd}')")
            case FuncMain:
                exec(f"self.{FuncMain[0]}()")
        
        translation = self._translator.translate(self._result)
        return translation

    def nothing(self) -> None:
        self._result = "Я не знаю такой команды("

    def communicate(self, func: str="") -> None:
        """
        Метод имитирует общение.
        """
        
        def hello():
            self._result = "Привет!"

        def goodbye():
            self._result = "Пока!"

        if func != "":
            exec(func + "()")
        else:
            self._result = ""

    def WhatWeather(self, func: str="") -> None:
        """
        Метод определяет погоду.
        """
        
        def get_location():
            return ipapi.location(ip=self.params.get("ip_client"), output="city")
        
        url = f"http://wttr.in/{get_location()}"
        weather_parameters = {"format": "j1"}

        def get_city():
            nonlocal url
            for ent in self.doc.ents:
                if ent.label_ == "LOC":
                    url = f"http://wttr.in/{ent.lemma_}"
                    break

        if func != "":
            exec(func + "()")
        
        response = requests.get(url, params=weather_parameters).json()
        data = response["current_condition"][0]
        self._result = f"Сейчас {data["weatherDesc"][0]["value"].lower()}, {data["temp_C"]}°C"
    
    def WhatDate(self, func: str="") -> None:
        """
        Метод определяет дату.
        """

        def number():
            self._result += dt.now().strftime("%d")

        def WeekDay():
            self._result += dt.now().strftime("%A")
        
        self._result = "Сегодня "
        locale.setlocale(locale.LC_ALL, ("ru_RU", "UTF-8"))

        if func != "":
            exec(func + "()")
        else:
            DataDate = dt.now()
            month = DataDate.strftime("%B")
            month = month[:-1] + "я" if month[-1] in "ьй" else month + "а" 
            self._result += DataDate.strftime("%A, %d ") + month + DataDate.strftime(" %Y года")

    def WhatTime(self, func: str="") -> None:
        """
        Метод определяет время.
        """

        def get_city():
            pass

        self._result = "Сейчас "

        if func != "":
            exec(func + "()")
        else:
            self._result += dt.now().strftime("%H:%M")

if __name__ == "__main__":
    obj = Skills("какая сейчас погода", "WhatWeather", {"ip_client": "158.46.32.12"})
    obj2 =Skills("какая погода в Париже", "WhatWeather get_city", {"ip_client": "51.158.203.17"})
    print(obj.MakeRequest())
    print(obj2.MakeRequest())
