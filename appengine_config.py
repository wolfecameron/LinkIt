from google.appengine.ext import vendor
import os

#specifies where to look for third party libraries (in the lib folder)
vendor.add(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib'))
