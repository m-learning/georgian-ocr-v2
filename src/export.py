import sys

def create_char_element(meta):
    return '<span '

def export_svg(original_image, meta_dir, output_html):
    # Read template
    # Replace values
    # 
    


if __name__ == "__main__":
    if len(sys.argv) > 3:
        original_image = sys.argv[1]
        meta_dir = sys.argv[2]
        output_html = sys.argv[3]

        export_svg(original_image, meta_dir, output_html)
    else:
        print ("Invalid argument: <original image>, <meta dir>, <output html>")

