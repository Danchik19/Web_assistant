from datetime import datetime as dt
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import locale
import requests
import spacy
import ipapi
import pytz


class Skills:
    _geolocator = Nominatim(user_agent="my_request")
    _nlp = spacy.load("ru_core_news_lg")
    _answer = ""

    def __init__(self, tag: str, message: str, result: str, params: dict[str, str]) -> None:
        self.tag = tag
        self.message = message
        self.doc = self._nlp(message)
        self.result = result
        self.params = params
        
    def make_request(self):
        """
        Метод обрабатывает запрос пользователя для определённого тега и выводит результат.
        """

        match self.tag:
            case "погода":
                self.what_weather()
            case "дата":
                self.what_date()
            case "время":
                self.what_time()
            case _:
                self._answer = self.result
        
        return self._answer

    def what_weather(self) -> None:
        """
        Метод определяет погоду.
        """
        
        get_location = lambda: ipapi.location(ip=self.params.get("ip_client"), output="city")
        location = self._geolocator.geocode(get_location())
        city = location.address.split(", ")[0]

        url = f"http://wttr.in/{city}"
        weather_parameters = {"format": "j1", "lang": "ru"}

        for ent in self.doc.ents:
            if ent.label_ == "LOC":
                city = ent.lemma_[0].upper() + ent.lemma_[1:]
                url = f"http://wttr.in/{city}"
                break
        
        response = requests.get(url, params=weather_parameters).json()
        data = response["current_condition"][0]
        self._answer = f"{city}: {data['lang_ru'][0]['value'].lower()}, {data['temp_C']}°C"
    
    def what_date(self) -> None:
        """
        Метод определяет дату.
        """
        
        self._answer = "Сегодня "
        locale.setlocale(locale.LC_ALL, ("ru_RU", "UTF-8"))

        if "число" in self.message:
            DataDate = dt.now()
            month = DataDate.strftime("%B")
            month = month[:-1] + "я" if month[-1] in "ьй" else month + "а" 
            self._answer += DataDate.strftime("%d ") + month + DataDate.strftime(" %Y года")
        else:
            self._answer += dt.now().strftime("%A")

    def what_time(self) -> None:
        """
        Метод определяет время.
        """

        self._answer = dt.now().strftime("Сейчас %H:%M")

        for ent in self.doc.ents:
            if ent.label_ == "LOC":
                city = ent.lemma_[0].upper() + ent.lemma_[1:]
                location = self._geolocator.geocode(city)
                timezone = pytz.timezone(TimezoneFinder().timezone_at(lng=location.longitude, lat=location.latitude))
                city_time = dt.now().astimezone(timezone)
                self._answer = city_time.strftime(f"В {city[:-1]}е сейчас %H:%M")
                break

if __name__ == "__main__":
    skill = Skills("погода", "Какая сейчас погода на улице?", "what_weather", {"ip_client": "158.46.32.12"})
    print(skill.make_request())
