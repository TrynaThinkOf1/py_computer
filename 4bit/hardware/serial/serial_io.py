class SerialIO:
    def __init__(self):
        pass

    def output(self, message: str) -> None:
        print(message)

    def read_input(self, prompt: str) -> str:
        return input(prompt)
