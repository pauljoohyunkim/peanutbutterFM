from PIL import ImageTk, Image

supported_img_types = (".png",".jpg",".jpeg")
imageCanvas = lambda imagePath: ImageTk.PhotoImage(Image.open(imagePath))
#def imageCanvas(imagepath, canvasObject=None):
#    img = ImageTk.PhotoImage(Image.open(imagepath))
#    #labelObject.config(image = img)
#    return img
    