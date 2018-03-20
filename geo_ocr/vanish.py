from multiprocessing import Process
from multiprocessing import Manager
from skimage import color
from skimage import filters
from skimage import img_as_ubyte
from skimage import util
import cv2
from . import file_operations as file_ops

DEBUG_DIR = "results/debug"

def vanish_image(img,local_area,offset,ret,size,invert=False):
    gray_scale_image = color.rgb2gray(img)
    if invert:
        gray_scale_image = util.invert(gray_scale_image)
    val = filters.threshold_local(gray_scale_image,local_area,mode="wrap",offset=offset)
    ret[size] = (gray_scale_image>val)
    #return (gray_scale_image > val)



def vanish_img(src_img):
    # src_img = deskew_image(src_img)
    file_ops.create_clean_dir(DEBUG_DIR)
    
    manager=Manager()
    imgs=manager.dict()
    p1=Process(target=vanish_image,args=(src_img,51,0.2,imgs,"clean"))
    p2=Process(target=vanish_image,args=(src_img,27,0.04,imgs,"noisy"))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    clean_img=img_as_ubyte(imgs["clean"])
    clean_small_img=img_as_ubyte(imgs["clean"])
    #src_img=img_as_ubyte(imgs["noisy"])
    src_img=img_as_ubyte(imgs["noisy"])
    #clean_img = img_as_ubyte(vanish_image(src_img,201,0.2))
    #src_img = img_as_ubyte(vanish_image(src_img,101,0.04))




    src_img = cv2.resize(src_img, (0, 0), fx = 4, fy = 4)
    clean_img = cv2.resize(clean_img, (0, 0), fx = 4, fy = 4)

#    src_img = cv2.erode(src_img, None, iterations=1)
#    cv2.imwrite(("%s/a1 eroded.png" % DEBUG_DIR), src_img)


    src_img=img_as_ubyte(src_img>200)
    clean_img=img_as_ubyte(clean_img>200)

    #thresh = filters.threshold_otsu(src_img)
    #src_img = img_as_ubyte(src_img >= thresh)

    cv2.imwrite(("%s/a1 vainshed.png" % DEBUG_DIR), src_img)
    cv2.imwrite(("%s/a1 clean.png" % DEBUG_DIR), clean_img)
    
    return src_img,clean_img, clean_small_img
    
