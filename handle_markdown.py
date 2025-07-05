
def remove_symbol(text: str):
    for s in ["$\n", "$", "# ", "#"]:
        text = text.replace(s, "")
    return text

def replace_space(text: str):
    for s in ["\\", "{" ,"}"]:
        text = text.replace(s, " ")
    return text

def replace_symbol(text: str):
    d = {
        "\%": " percent",
        "_": " sub ",
        "=": " equals ",
        "+": " plus ",
        "-": " minus ",
        "^": " to the "
    }
    for k, v in d.items():
        # Percent symbols
        text = text.replace(k, v)
    return text

def run():
    with open('input.txt','r',encoding = 'utf-8') as f:
        text = f.read()

    text = remove_symbol(text)
    text = replace_space(text)
    text = replace_symbol(text)

    with open('output.txt', 'w', encoding = 'utf-8') as f:
        f.write(text)


if __name__ == '__main__':
    run()
