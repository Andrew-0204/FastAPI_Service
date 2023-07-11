from fastapi import HTTPException, APIRouter, Body
from fastapi.encoders import jsonable_encoder
from ..database import MongoAPI
from ..models.arg_model import (
    Model,
    MongoBase
)
import requests
from dotenv import dotenv_values
from ..my_number import numbers
config = dotenv_values(".env")
router = APIRouter()

@router.get('/mongodb')
async def get_all(request: MongoBase = Body(...)):
    data = jsonable_encoder(request)
    if data is None or data == {}:
        raise HTTPException(status_code=400, detail="Please provide connection information")

    obj1 = MongoAPI(data)
    response = await obj1.all()
    print(response)
    return response

@router.get('/mongodb/last')
async def get_last_document(request: MongoBase = Body(...)):
    data = jsonable_encoder(request)
    if data is None or data == {}:
        raise HTTPException(status_code=400, detail="Please provide connection information")

    obj1 = MongoAPI(data)
    response = await obj1.get_last_document()
    return response


@router.get('/mongodb/{id}')
async def get_last_document(id, request: MongoBase = Body(...)):
    data = jsonable_encoder(request)
    if data is None or data == {}:
        raise HTTPException(status_code=400, detail="Please provide connection information")

    obj1 = MongoAPI(data)
    response = await obj1.retrieve_one_value(id)
    return response

@router.post('/mongodb/cal')
async def mongo_cal(request: Model = Body(...)):
    data = jsonable_encoder(request)
    if not data:
        raise HTTPException(status_code=400, detail="Please provide connection information")

    obj1 = MongoAPI(data)
    await obj1.create(data)  # Await the coroutine function call
    last_document = await obj1.get_last_document()  # Await the coroutine function call
    print(last_document)
    if last_document is None:
        raise HTTPException(status_code=404, detail="No last document found")

    number = last_document['number']
    args = last_document['args']
    object_1 = args['Object_1']
    x_1, y_1, z_1 = args['X_1'], args['Y_1'], args['Z_1']
    object_2 = args['Object_2']
    x_2, y_2, z_2 = args['X_2'], args['Y_2'], args['Z_2']

    payload = {
        'nargout': 2,
        'rhs': [
            [number],
            [object_1],
            x_1,
            y_1,
            z_1,
            [object_2],
            x_2,
            y_2,
            z_2
        ]
    }

    try:
        response = requests.post("http://mymatlab:9910/mi_service/FunctionCMM", json=payload)
        response.raise_for_status()
        result = response.json()
    except requests.exceptions.RequestException as err:
        result = {'err': str(err), 'arr': None}

    if number in numbers.Number:
        data['collection'] = numbers.Number[number]
        obj1 = MongoAPI(data)

    await obj1.write_result(data, result)

    return result['lhs'][1]['mwdata']


@router.post('/mongodb')
async def mongo_write(request: Model = Body(...)):
    data = request.json()
    if data is None or data == {} or 'Document' not in data:
        raise HTTPException(status_code=400, detail="Please provide connection information")

    obj1 = MongoAPI(data)
    response = await obj1.create(data)
    return response

