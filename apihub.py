# coding=utf8
import time, os
import responder
from tools.uuid_generator import uuid_hash
from auto_ml.core.parameter_parser import ModelStore
from auto_ml.core.aml import AML

api = responder.API()

data_store_path = './static/data/'
# model_store_path = './static/model'


# @api.route("/")
# def hello_world(req, resp):
#     resp.text = "hello, world!"


FileExistsError_msg = 'data {} existed! please do not upload same data! '


class FileExistsError(Exception):
    def __init__(self, msg):
        self.msg = msg


@api.route("/upload_file")
async def upload_file(req, resp):
    @api.background.task
    def store_data(content, path, filename):

        if not os.path.exists(path):
            f = open(path, 'wb')

            f.write(content)
            f.close()
        else:
            raise FileExistsError(FileExistsError_msg.format(filename))

    data = await req.media(format='files')
    # data = req.media(format='files')

    data_uuid = uuid_hash(str(data))

    filename = data_uuid  # data['file']['filename']
    content = data['file']['content']
    path = data_store_path + '{}'.format(filename)

    msg = FileExistsError_msg.format(filename)
    if not os.path.exists(path):
        print(filename)
        store_data(content, path, filename)
        resp.media = {'dataid': filename, 'status': 'good', 'store_status': 'ok'}
        resp.status_code = api.status_codes.HTTP_200
    else:
        resp.media = {'dataid': 'error', 'status': 'duplicates', 'store_status': msg}
        resp.status_code = api.status_codes.HTTP_409


@api.route("/check_file/{dataid}")
async def check_file(req, resp, *, dataid):
    if os.path.exists(data_store_path + dataid):
        resp.text = f'{dataid} found!'
        resp.status_code = api.status_codes.HTTP_200

    else:
        resp.text = f"{dataid} not found!"
        resp.status_code = api.status_codes.HTTP_404


@api.route("/AutoML/{dataid}")
class AutoML(object):
    # def on_get(self, req, resp, *, dataid):
    #     if dataid == 'get_supported_model':
    #         parameters = self.parse_parameters(req.params)

    def on_request(self, req, resp, *, dataid):  # or on_get...
        parameters = self.parse_parameters(req.params)
        if dataid == 'getParams':
            if 'type' in parameters:
                result = AML.get_supported_model(parameters['type'], raiseError=False)

                resp.text = f"{result}"
                resp.status_code = api.status_codes.HTTP_200
            else:
                resp.text = f"{dataid}, wrong parameters! Please retry! "
                resp.status_code = api.status_codes.HTTP_416

        else:
            print(parameters)
            if os.path.exists(data_store_path + dataid):
                result = self.run_program(parameters, data_store_path + dataid)

                resp.text = f"{result}"
                # resp.headers.update({'X-Life': '42'})
                resp.status_code = api.status_codes.HTTP_200
            else:
                resp.text = f"{dataid}, No dataset found! Please upload data first!"
                resp.status_code = api.status_codes.HTTP_416

    @staticmethod
    def _load_dataset(dataset):

        strings = ModelStore._force_read(dataset)
        return ModelStore._force_read_from_string(strings)

        pass

    @classmethod
    def run_program(cls, parameters, dataset):

        m = AML.run(parameters, dataset)
        # dataset_dict = cls._load_dataset(dataset)

        return m

    @staticmethod
    def parse_parameters(params):
        pa = {}
        for key, values in params.items():
            if values == 'Null':
                values = None
            elif values == '[]':
                values = []
            elif values.isnumeric():
                values = float(values)
            else:
                pass
            pa[key] = values

        return pa


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
