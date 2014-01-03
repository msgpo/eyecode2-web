import sys, os, logging
INTERP = os.path.join(os.environ['HOME'], 'experiment.synesthesiam.com', 'bin', 'python')
if sys.executable != INTERP:
	os.execl(INTERP, INTERP, *sys.argv)

cwd = os.getcwd()
sys.path.append(cwd)

sys.path.append('eyecode2')
from eyecode2.app import app as e2app

logging.basicConfig(filename=os.path.join(cwd, "error.log"),
        level=logging.DEBUG,
        format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
        datefmt="%H:%M:%S")
logging.info("Started server")

def application(environ, start_response):
    results = []
    try:
        results = e2app(environ, start_response)
    except ex:
        logging.exception(ex)
    return results
