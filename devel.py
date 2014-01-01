import sys, os
sys.path.append(os.getcwd())
sys.path.append('eyecode2')

os.environ["EYECODE2_CONFIG"] = "devel.cfg"
from eyecode2.app import app as application

if __name__ == "__main__":
    application.run()
