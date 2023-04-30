def read_inputs():
    """Read inputs from stdin."""
    while True:
        try:
            yield input(">> ")
        except EOFError:
            return


HANDLERS = {}


def validate_input(validator, message):
    """Validate input with a validator."""

    def decorator(func):

        def wrapper(*args, **kwargs):
            if validator(args):
                try:
                    return func(*args, **kwargs)
                except KeyError:
                    return message
            return message

        return wrapper

    return decorator


def command_handler(command, parser=str.split, handlers=HANDLERS):
    """Register a command handler."""

    def decorator(func):
        handlers[command] = {
            'handler': func,
            'parser': parser,
        }
        return func

    return decorator


@command_handler("quit")
@command_handler("good bye")
@command_handler("close")
@command_handler("exit")
def handle_quit(data={}):
    """Handle quit command."""
    raise StopIteration


@command_handler("hello")
def handle_hello(data={}):
    """Handle hello command."""
    return "How can I help you?"


@command_handler("add")
@validate_input(
    lambda x: len(x) == 2,
    "Please specify a name and a valid telephone number.",
)
def handle_add(name: str, telephone: str, data={}):
    """Handle add command."""
    data[name] = telephone
    return f"Added {name}"


@command_handler("change")
@validate_input(
    lambda x: len(x) == 2,
    "Please specify an existing name and a valid telephone number.",
)
def handle_change(name: str, telephone: str, data={}):
    """Handle change command."""
    previous = data[name]
    data[name] = telephone
    return f"Changed {name} from {previous} to {telephone}"


@command_handler("show all")
def handle_show_all(data={}):
    """Handle show all command."""
    return "\n".join(f"{k}: {v}" for k, v in data.items())


@command_handler("phone")
@validate_input(lambda x: len(x) == 1, "Please specify a name.")
def handle_phone(name, data={}):
    """Handle phone command."""
    return data[name]


def dispatch(handlers, data):
    """Dispatch commands to handlers."""

    def _dispatch(line):
        for k, v in handlers.items():
            if line.startswith(k):
                return v['handler'](*v['parser'](line[len(k):]), data=data)
        return "I don't understand, please rephrase."

    return _dispatch


def run(
    input=read_inputs,
    output=print,
    handlers=HANDLERS,
):
    data = {}
    list(map(output, map(dispatch(handlers, data), input())))
    output("Good bye!")


if __name__ == "__main__":
    run()