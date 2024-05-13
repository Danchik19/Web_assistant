import random
import json
import torch
from ChatBot.model import NeuralNet
from ChatBot.nltk_utils import bag_of_words, tokenize
from ChatBot.skills import Skills


class Hedgehog:
    _device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    with open("ChatBot/intents.json", "r", encoding="utf-8") as f:
        _intents = json.load(f)

    _FILE = "ChatBot/data.pth"
    _data = torch.load(_FILE)

    _input_size = _data["input_size"]
    _hidden_size = _data["hidden_size"]
    _output_size = _data["output_size"]
    _all_words = _data["all_words"]
    _tags = _data["tags"]
    _model_state = _data["model_state"]

    _model = NeuralNet(_input_size, _hidden_size, _output_size).to(_device)
    _model.load_state_dict(_model_state)
    _model.eval()

    def __init__(self, message: str, params: dict[str, str]) -> None:
        self.message = message
        self.params = params

    def get_answer(self) -> str:
        """
        Метод возвращает ответ на запрос пользователя.
        """

        message = tokenize(self.message)
        X = bag_of_words(message, self._all_words)
        X = X.reshape(1, X.shape[0])
        X = torch.from_numpy(X).to(self._device)

        output = self._model(X)
        _, predicted = torch.max(output, dim=1)
        
        tag = self._tags[predicted.item()]

        probs = torch.softmax(output, dim=1)
        prob = probs[0][predicted.item()]

        if prob.item() > 0.75:
            for intent in self._intents["intents"]:
                if tag == intent["tag"]:
                    temp_result = random.choice(intent["responses"])
                    skill = Skills(tag, self.message, temp_result, self.params)
                    return skill.make_request()
        else:
            return "Я не знаю такой команды("

if __name__ == "__main__":
    hedgehog = Hedgehog()
    print(hedgehog.get_answer("Привет"))