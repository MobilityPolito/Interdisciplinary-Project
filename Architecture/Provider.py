""" 

Provider:
This metaclass represents a service provider.
Besides some common utility method, the classes implementing this 
interface should come with specific methods which exploit any 
particular data/function supplied by providers.

"""

from abc import ABCMeta

class Provider ():
    
    __metaclass__ = ABCMeta

    def __init__ ():
        pass
    
    def get_data():
        """
        Query provider's data from db with some criterion
        """
        pass
    
    def get_fields():
        """
        Figure out how provider's data are organised
        """
        pass
    