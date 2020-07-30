from waitress import serve
import pandaserver

if __name__ == '__main__':
    serve(pandaserver.app, port=80)
