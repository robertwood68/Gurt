import gurt

while True:
    text = input('gurt > ')
    result, error = gurt.run('<stdin>', text)

    if error:
        print(error.as_string())
    else:
        print(result)
