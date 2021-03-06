from PIL import ImageTk, Image

supported_img_types = (".png",".jpg",".jpeg", ".bmp", ".gif")
#imageCanvas = lambda imagePath: ImageTk.PhotoImage(Image.open(imagePath))

# imagePath: path to image
# canvasSize: size of the canvas that the image will be sitting on.
def imageCanvas(imagePath, canvasSize):
    im = Image.open(imagePath)

    # Resizing so that the image fills the canvas, but fully contained
    imHeight, imWidth = im.size
    canvasHeight, canvasWidth = canvasSize
    sizeFactor = min(canvasHeight / imHeight, canvasWidth / imWidth)
    imHeight = int(sizeFactor * imHeight)
    imWidth = int(sizeFactor * imWidth)

    im = im.resize((imHeight,imWidth))
    
    img = ImageTk.PhotoImage(im)
    #labelObject.config(image = img)
    return img
    
def simpleTkImage(imagePath):
    return ImageTk.PhotoImage(Image.open(imagePath))