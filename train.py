# From https://github.com/jsvine/markovify
import markovify
from random import shuffle
import language_tool_python

import json
from dataset import DATASETS


def make_data():
    data = DATASETS["vn"].sample(15000)
    shuffle(data)
    return data


if __name__ == "__main__":
    lines = make_data()

    # Build the model
    text_model = markovify.NewlineText("\n".join(lines), state_size=4)
    with open("model.json", "w+") as f:
        json.dump(text_model.to_json(), f)

    count = 0
    tool = language_tool_python.LanguageTool('en-US')
    while count < 10:
        sentence = None
        while sentence is None:
            sentence = text_model.make_short_sentence(280, 80)
        if len(tool.check(sentence)) < 5:
            print(tool.correct(sentence))
            count += 1
