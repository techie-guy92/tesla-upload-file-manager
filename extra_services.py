from django.conf import settings
from django.core.mail import EmailMultiAlternatives 
from django.utils.text import slugify
# from slugify import slugify
from random import randint
from uuid import uuid4
import os


#=======================================================================
media_url = settings.MEDIA_URL
media_root = settings.MEDIA_ROOT
img_list = os.listdir(os.path.join(media_root, "images"))


#=======================================================================   
class Uploading_Files:
    def __init__(self, prefix_dir, suffix_dir):
      self.prefix_dir = prefix_dir
      self.suffix_dir = suffix_dir
      
    def file_name(self,instance,filename):
        filename, ext = os.path.split(filename)
        new_filename = f"{uuid4()}{ext}"
        return f"{self.prefix_dir}/{self.suffix_dir}/{new_filename}"

#sample
# folder_path = Uploading_Files("images","group")  


#=======================================================================
def upload_to(instance, filename):
    file_name, ext = os.path.splitext(filename)
    new_filename = f"{uuid4()}{ext}"
    return f"uploaded_files/{instance.user.first_name}_{instance.user.last_name}/{new_filename}"


#=======================================================================
def Sending_Mail(Subject,Message,HTML_Content,To):
    Sending_From = settings.EMAIL_HOST_USER
    Message = EmailMultiAlternatives(Subject,Message,Sending_From,To)
    Message.attach_alternative(HTML_Content,"text/html")
    Message.send()
    
    
#=======================================================================
def generating_random_code(count):
    count -= 1
    generator = randint(10**count, 10**(count + 1)-1)
    return generator


#=======================================================================
# Both modules can be used, but 'slugify' will convert the slug to Finglish, 
# while 'django.utils.text' can save Persian slugs when the 'allow_unicode=True' option is enabled.


def replace_dash_to_space(title):
        new_title = "".join([eliminator.replace(" ","-") for eliminator in title])
        return new_title.lower()
    
# def generate_slug(title):
#     new_title = replace_dash_to_space(title)
#     return slugify(new_title)

def generate_slug(title):
    new_title = replace_dash_to_space(title)
    return slugify(new_title, allow_unicode=True)
   
# print(generate_slug("soheil Daliri TEHRAN"))


#=======================================================================

