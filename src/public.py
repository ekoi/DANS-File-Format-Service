import json
import logging
import os
from os.path import exists
import puremagic

from fastapi import HTTPException, Query, APIRouter, File

import commons
import src

from src.commons import settings, __version__

router = APIRouter()


@router.get('/')
def info():
    logging.info("DANS File Format Service")
    logging.debug("info")
    return {"name": "DANS File Format Service", "version": __version__}


@router.get("/formats")
def get_formats():
    # with open(settings.DANS_FILE_FORMATS) as json_file:
    #     data = json.load(json_file)
    return json.loads(commons.data['dans-file-formats'])


@router.get("/type/{filetype}")
def check_filetype(filetype: str):
    # todo: check in IANA.org
    if filetype.upper() in commons.all_formats:
        return {filetype: True}

    return {filetype: False}


@router.post("/type/verification/{filetype}")
def verify_filetype(filetype: str, file_header: bytes = File()):
    # Todo: retrieve header
    given_file_type = puremagic.from_string(file_header)
    if given_file_type != f".{filetype}":
        raise HTTPException(status_code=400, detail="Doesn't match")

    return {filetype: "ok"}


@router.get("/type/formats/{filetype}")
def check_formats():
    # with open(settings.DANS_FILE_FORMATS) as json_file:
    #     data = json.load(json_file)
    return json.loads(commons.data['dans-file-formats'])


@router.post("/type/convert/{to_format}")
def convert(to_format: str):
    raise HTTPException(status_code=501, detail=f'This endpoint is not implemented yet.')

