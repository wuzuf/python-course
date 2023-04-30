import chatbot
import pytest


def read_inputs(scenario):

    def read():
        for i in scenario:
            if i.startswith(">> "):
                yield i[3:]

    return read


def outputs(scenario):
    for i in scenario:
        if not i.startswith(">>"):
            yield i


scenarios = [
    [
        ">> hello",
        "How can I help you?",
        ">> invalid command",
        "I don't understand, please rephrase.",
        ">> add John 123456",
        "Added John",
        ">> add Mary 234567",
        "Added Mary",
        ">> phone Mary",
        "234567",
        ">> change Mary 999999",
        "Changed Mary from 234567 to 999999",
        ">> phone Mary",
        "999999",
        ">> show all",
        "John: 123456\nMary: 999999",
        ">> good bye",
        "Good bye!",
    ],
    [
        ">> add John",
        "Please specify a name and a valid telephone number.",
        "Good bye!",
    ],
    [
        ">> change John 1234567",
        "Please specify an existing name and a valid telephone number.",
        "Good bye!",
    ],
    [
        ">> phone",
        "Please specify a name.",
        "Good bye!",
    ],
]


@pytest.mark.parametrize("scenario", scenarios)
def test_chatbot_run(scenario):
    out = []
    chatbot.run(read_inputs(scenario), lambda x: out.append(x),
                chatbot.HANDLERS)
    assert list(outputs(scenario)) == out
