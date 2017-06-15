from learning import *
from predict import *
import os

print "cat"

def learning(path=os.getcwd()):
    train(path)

def predict():
    args = init_arguments()
    char = recognize_image(args.image)
    print(char)

