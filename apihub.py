# coding=utf8
import time, os
import responder

api = responder.API()

data_store_path = './static/'


# @api.route("/")
# def hello_world(req, resp):
#     resp.text = "hello, world!"
class FileExistsError(Exception):
    def __init__(self, msg):
        self.msg = msg


@api.route("/check_file")
def check_file(req, resp):
    pass


@api.route("/upload_file")
async def upload_file(req, resp):
    @api.background.task
    def store_data(content, path, filename):

        if not os.path.exists(path):
            f = open(path, 'wb')

            f.write(content)
            f.close()
        else:
            raise FileExistsError('{} existed! please rename it! '.format(filename))

    data = await req.media(format='files')
    # data = req.media(format='files')
    # print(data)
    filename = data['file']['filename']
    content = data['file']['content']
    path = data_store_path + '{}'.format(filename)

    msg = '{} existed! please rename it! '.format(filename)
    if not os.path.exists(path):
        store_data(content, path, filename)
        resp.media = {'filename': filename, 'status': 'good', 'store_status': 'ok'}
    else:
        resp.media = {'filename': filename, 'status': 'bad', 'store_status': msg}


@api.route("/{auto_ml}")
class auto_ml:
    def on_request(self, req, resp, *, auto_ml):  # or on_get...

        parameters = self.parse_parameters(req.params)
        print(parameters)
        resp.text = f"{auto_ml}, world!"
        resp.headers.update({'X-Life': '42'})
        resp.status_code = api.status_codes.HTTP_416

    @staticmethod
    def parse_pareters(params):
        pa ={}
        for key, values in params.items():
            if values == 'Null':
                values =None
            elif values == '[]':
                values =[]
            else:
                print(values)


        return {key: values  }


# @api.route("/auto_ml")
# def auto_ml(req, resp):
#     paras = req.media()
#
#     print(paras, paras['parameters'])
#     resp.media = {'filename': 's', 'status': 'good', 'store_status': 'ok'}
#     pass


# @api.route("/incoming")
# async def receive_incoming(req, resp):
#     @api.background.task
#     def process_data(data):
#         """Just sleeps for three seconds, as a demo."""
#         time.sleep(3)
#
#     # Parse the incoming data as form-encoded.
#     # Note: 'json' and 'yaml' formats are also automatically supported.
#     data = await req.media()
#
#     # Process the data (in the background).
#     process_data(data)
#
#     # Immediately respond that upload was successful.
#     resp.media = {'success': True}
#

if __name__ == '__main__':
    api.run(address='0.0.0.0', port=8279)
    pass
