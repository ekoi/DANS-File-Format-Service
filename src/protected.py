import json
import random
import shutil
import uuid
import logging
import os
from typing import Union, Optional

import magic
import requests
import xml.etree.ElementTree as ET

# import codecs
from fastapi import APIRouter, Request, HTTPException, Query

from commons import data

router = APIRouter()
verify_type_response_example = {
    200: {
        "description": "File successfully verified",
        "content": {
            "application/json": {
                "example":
                    {
                        "MIME-type": "text/plain",
                        "info": "Some details",
                        "purpose": "audio/video",
                        "schema": "https://ddialliance.org/Specification/DDI-Lifecycle/3.2/XMLSchema/dc.xsd"
                    }
            }
        }
    },
    422: {
        "description": "Validation error",
        "content": {
            "application/json": {
                "example":
                    {
                        "message": "Some details"
                    }
            }
        }
    }
}

verify_format_response_example = {
    200: {
        "description": "Verify formats for preservation and dissemination",
        "content": {
            "application/json": {
                "example":
                    {
                        "accepted": "yes",
                        "info": "Some details",
                        "dissemination-format": "AAC",
                        "preservation-format": "MKA"
                    }
            }
        }
    },
    422: {
        "description": "Validation error",
        "content": {
            "application/json": {
                "example":
                    {
                        "message": "Some details"
                    }
            }
        }
    }
}


@router.post('/verify-type', status_code=200, tags=['Verification'], responses=verify_type_response_example)
async def verify_type(submitted_file: Request,
                      purpose: Union[str | None] = Query(default=None, enum=["audio", "video"]),
                      schema_validation: Optional[bool] = Query(None,
                                                                description="Validate XML/JSON to a metadata schema")):
    bytes_input = await submitted_file.body()
    # Posting Content type header is optional
    # content_type = submitted_file.headers['Content-Type']

    return {"MIME-type": magic.from_buffer(bytes_input, mime=True), "info": magic.from_buffer(bytes_input)
        , "purpose": "Not Specified", "schema": "Not applicable"}


@router.post('/verify-format/{file_extension}', status_code=200, tags=['Verification'], responses=verify_format_response_example)
async def verify_format(file_extension: str, purpose: Union[str | None] = Query(default=None, enum=["audio", "video"])):
    #Check file extension in dans_file_formats
    if file_extension in data.get('preferred-formats'):
        return {"accepted": "yes"}
    elif file_extension in data.get('non-preferred-formats'):
        return {"accepted": "no"}
    else:
        return {"accepted": "tbd"}


@router.post("/transform", tags=['Transform'])
async def transform(submitted_file: Request):
    return {"message": "msg"}
