from application import create_app
import sys

def create_with_port(port_no):
    app = create_app()
    app.run(host="0.0.0.0",port=port_no)

if __name__== "__main__":
    create_with_port(sys.argv[1])
