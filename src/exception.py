import sys # provides various funtions and variables that are used to manipulate different parts of the Python runtime environment
from logger import logging
def error_message_details(error, error_detail:sys):
    '''
    Docstring for error_message_details

    :param error: Exception object
    :param error_detail: sys module
    :type error_detail: sys
    '''
    _,_,exc_tb = error_detail.exc_info() # retrieves information about the most recent exception caught by an except clause in the current thread
    file_name = exc_tb.tb_frame.f_code.co_filename # retrieves the filename where the exception occurred
    error_message = "Error occured in python script name [{0}] line number [{1}] error message [{2}]".format(
        file_name,
        exc_tb.tb_lineno,
        str(error))

    return error_message


class CustomException(Exception):
    '''
    Docstring for CustomException class

    Inherits from the built-in Exception class to create a custom exception type.
    '''
    def __init__(self, error_message, error_detail:sys):
        '''
        Docstring for CustomException.__init__

        :param error_message: Error message string
        :param error_detail: sys module
        :type error_detail: sys
        '''
        super().__init__(error_message) # Call the constructor of the base Exception class
        self.error_message = error_message_details(error_message, error_detail=error_detail) # Get detailed error message

    def __str__(self):
        '''
        Docstring for CustomException.__str__

        :return: String representation of the CustomException
        :rtype: str
        '''
        return self.error_message

# if __name__ == "__main__":
#     try:
#         a = 1/0
#     except Exception as e:
#         logging.info("Divide by zero exception occurred")
#         raise CustomException(e, sys)
