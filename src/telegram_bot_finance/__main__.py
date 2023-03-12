from controller.controller import Controller
import asyncio

if __name__ == "__main__":
    s = Controller()
    asyncio.run(s.main())

# import time
# import logging
# import logging.handlers
#
# log_file_name = 'LOG_FILE'
# logging_level = logging.DEBUG
# try:
#     # set TimedRotatingFileHandler for root
#     formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
#     # use very short interval for this example, typical 'when' would be 'midnight' and no explicit interval
#     handler = logging.handlers.TimedRotatingFileHandler(log_file_name, when="S", interval=10, backupCount=3)
#     handler.setFormatter(formatter)
#     logger = logging.getLogger() # or pass string to give it a name
#     logger.addHandler(handler)
#     logger.setLevel(logging_level)
#     # generate lots of example messages
#     for i in range(20):
#         time.sleep(1)
#         logger.debug('i=%d' % i)
#         logger.info('i=%d' % i)
#         logger.warning('i=%d' % i)
#         logger.error('i=%d' % i)
#         logger.critical('i=%d' % i)
# except KeyboardInterrupt:
#     # handle Ctrl-C
#     logging.warning("Cancelled by user")
# except Exception as ex:
#     # handle unexpected script errors
#     logging.exception("Unhandled error\n{}".format(ex))
#     raise
# finally:
#     # perform an orderly shutdown by flushing and closing all handlers; called at application exit and no further use of the logging system should be made after this call.
#     logging.shutdown()


