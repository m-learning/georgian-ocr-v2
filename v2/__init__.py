from learning import *
from predict_all import *
import os

def learning(path=os.getcwd()):
    train(path)

def predict(path=os.getcwd()):
	
    f.do_fragmentation(path)
    result = ''
    full_score = 0
    full_count = 0

    for (dir_path, dir_names, file_names) in os.walk(f.FRAGMENTS_DIR):
        file_names = sorted(file_names)
        for file_name in file_names:
            [char, score] = recognize_image(os.path.join(dir_path, file_name))
            full_score += score
            full_count += 1

            print file_name, char.encode('utf8'), score
            write_meta_char(file_name[:-4]+'.json', char, score)
    print 'Avg score: %d' % (full_score * 100 /full_count)

    
    

