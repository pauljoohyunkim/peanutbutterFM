from PIL import ImageTk, Image

imageCanvas = lambda imagePath: ImageTk.PhotoImage(Image.open(imagePath))
#def imageCanvas(imagepath, canvasObject=None):
#    img = ImageTk.PhotoImage(Image.open(imagepath))
#    #labelObject.config(image = img)
#    return img
    