import pathlib
fileDir = r"C:\Users\ad94\PycharmProjects\english_books_bot\Eng\ะบััั Own it"
fileExt = r"*.pdf"
print(list(pathlib.Path(fileDir).glob(fileExt))[0])
