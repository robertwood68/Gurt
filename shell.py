import gurt

while True:
    text = input('gurt > ')
    if text == 'exit':
        exit(0)
    result, error = gurt.run('<stdin>', text)

    if error:
        print(error.as_string())
    else:
        print(result)
