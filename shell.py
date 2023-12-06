import gurt

while True:
    text = input('gurt > ')
    if text.strip() == "":
        continue
    if text.lower() == 'exit' or text.lower() == 'quit':
        exit(0)
    if text.lower() == 'run':
        exit(0)
    result, error = gurt.run('<stdin>', text)

    if error:
        print(error.as_string())
    elif result:
        if len(result.elements) == 1:
            print(repr(result.elements[0]))
        else:
            print(repr(result))
