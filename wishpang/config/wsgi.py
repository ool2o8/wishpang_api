# import os,sys
# path = os.path.abspath(__file__+'/../..')
# if path not in sys.path:
#     sys.path.append(path)

# from django.core.wsgi import get_wsgi_application

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# application = get_wsgi_application()

# activate_this = "C:\side_project\Wishpang\myvenv\Scripts\activate_this.py"
# # execfile(activate_this, dict(__file__=activate_this))
# exec(open(activate_this).read(),dict(__file__=activate_this))

# import os
# import sys
# import site

# # Add the site-packages of the chosen virtualenv to work with
# site.addsitedir('C:\side_project\Wishpang\myvenv\Lib\site-packages')




# # Add the app's directory to the PYTHONPATH
# sys.path.append('C:\side_project\Wishpang\Wishpang')
# sys.path.append('C:\side_project\Wishpang\Wishpang\config')

# os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# from django.core.wsgi import get_wsgi_application
# application = get_wsgi_application()
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()