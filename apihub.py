# coding=utf8
import time
import responder

api = responder.API()


# @api.route("/")
# def hello_world(req, resp):
#     resp.text = "hello, world!"


@api.route("/upload_file")
async def upload_file(req, resp):
    @api.background.task
    def process_data(data):
        f = open('./{}'.format(data['file']['filename']), 'w')
        f.write(data['file']['content'].decode('utf-8'))
        f.close()

    data = await req.media(format='files')
    print(data)
    process_data(data)

    resp.media = {'success': 'ok'}


@api.route("/incoming")
async def receive_incoming(req, resp):
    @api.background.task
    def process_data(data):
        """Just sleeps for three seconds, as a demo."""
        time.sleep(3)

    # Parse the incoming data as form-encoded.
    # Note: 'json' and 'yaml' formats are also automatically supported.
    data = await req.media()

    # Process the data (in the background).
    process_data(data)

    # Immediately respond that upload was successful.
    resp.media = {'success': True}


if __name__ == '__main__':
    api.run(address='0.0.0.0', port=8279)
    pass
