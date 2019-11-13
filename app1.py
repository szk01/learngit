from . import create_app

if __name__ == '__main__':
    app = create_app()
    print('application', app)
    config = dict(
        debug=True,
        # host='127.0.0.1',
        # local_host='106.15.44.224',
        host='0.0.0.0',
        # host='192.168.101.39',
        port=80,
        app=app,
    )
    app.run(**config)
