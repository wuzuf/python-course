import shlex


def read_inputs():
    """Read inputs from stdin."""
    while True:
        try:
            yield input(">> ")
        except EOFError:
            return


HANDLERS = {}


def validate_input(validator=lambda args, kwargs: (True, "")):
    """Validate input with a validator."""

    def decorator(func):

        def wrapper(*args, **kwargs):
            success, message = validator(args, kwargs)
            if success:
                try:
                    return func(*args, **kwargs)
                except KeyError as e:
                    return f"{str(e)} does not exist."
            return message

        return wrapper

    return decorator


def command_handler(command,
                    parser=lambda x: (shlex.split(x), ""),
                    handlers=HANDLERS):
    """Register a command handler."""

    def decorator(func):
        handlers[command] = {
            'handler': func,
            'parser': parser,
        }
        return func

    return decorator


def simple_parser(args, message):

    def _parser(x):
        a = shlex.split(x)
        if len(args) != len(a):
            return None, message
        return dict(zip(args, a)), ""

    return _parser


@command_handler("quit")
@command_handler("good bye")
@command_handler("close")
@command_handler("exit")
@validate_input()
def handle_quit(data={}):
    """Handle quit command."""
    raise StopIteration


@command_handler("hello")
@validate_input()
def handle_hello(data={}):
    """Handle hello command."""
    return "How can I help you?"


@command_handler(
    "add",
    simple_parser(
        ['name', 'telephone'],
        "Please specify a name and a valid telephone number.",
    ),
)
@validate_input()
def handle_add(name: str, telephone: str, data={}):
    """Handle add command."""
    data[name] = telephone
    return f"Added {name} with number {telephone}"


@command_handler(
    "change",
    simple_parser(
        ['name', 'telephone'],
        "Please specify a name and a valid telephone number.",
    ),
)
@validate_input()
def handle_change(name: str, telephone: str, data={}):
    """Handle change command."""
    previous = data[name]
    data[name] = telephone
    return f"Changed {name} from {previous} to {telephone}"


@command_handler("show all")
@validate_input()
def handle_show_all(data={}):
    """Handle show all command."""
    return "\n".join(f"{k}: {v}" for k, v in data.items())


@command_handler(
    "phone",
    simple_parser(
        ['name'],
        "Please specify a name.",
    ),
)
@validate_input()
def handle_phone(name, data={}):
    """Handle phone command."""
    return data[name]


def dispatch(handlers, data):
    """Dispatch commands to handlers."""

    def _dispatch(line):
        for k, v in handlers.items():
            if line.startswith(k) and (k == line or line[len(k)] == " "):
                args, message = v['parser'](line[len(k) + 1:])
                if message:
                    return message
                if isinstance(args, dict):
                    return v['handler'](**args, data=data)
                return v['handler'](*args, data=data)
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