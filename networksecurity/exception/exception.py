
import sys  #commonly used to access runtime details like the current exception traceback.
from networksecurity.Logging import logger


class NetworkSecurityException(Exception):
    def __init__(self,error_message,error_details:sys):  ## error details coming from system
        self.error_message = error_message
        _,_,exc_tb = error_details.exc_info()  ## skipping first 2 info (not useful) third give error details

        self.lineno = exc_tb.tb_lineno
        file_name = exc_tb.tb_frame.f_code.co_filename   ## file name of error
        ## more given in custom exception handling documentation

        def __str__(self):
            return "Error occured in python script namen [{0}] line number [{1}] error message [{2}]".format(
                self.file_name,self.lineno,str(self.error_message)
            )
        
    ## Checking if it is working
# if __name__ == "__main__":
#     try:
#         logger.logging.info("Entered try")
#         a = 1/0
#     except Exception as ex:
#         err = NetworkSecurityException(ex,sys)
#         logger.logging.info(err)
#         raise err from None
    

    
 