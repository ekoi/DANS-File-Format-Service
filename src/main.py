import json
import logging
import os

import requests
import uvicorn
from fastapi import FastAPI, HTTPException, Depends, status, Query
from fastapi.security import OAuth2PasswordBearer

import commons
import protected
import public
from commons import settings, __version__, data

api_keys = [
    settings.DANS_FILE_FORMAT_SERVICE_API_KEY
]  # Todo: This is encrypted in the .secrets.toml

# Authorization Form: It doesn't matter what you type in the form, it won't work yet. But we'll get there.
# See: https://fastapi.tiangolo.com/tutorial/security/first-steps/
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  # use token authentication


def api_key_auth(api_key: str = Depends(oauth2_scheme)):
    if api_key not in api_keys:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Forbidden"
        )


app = FastAPI(title=settings.FASTAPI_TITLE, description=settings.FASTAPI_DESCRIPTION,
              version=__version__)

app.include_router(
    public.router,
    tags=["Public"],
    prefix=""
)

app.include_router(
    protected.router,
    # tags=["Protected"],
    prefix="",
    dependencies=[Depends(api_key_auth)]
)


@app.on_event('startup')
def set_dans_file_formats():
    logging.debug("startup")
    #TODO: Exception eg. 200, 404
    resp = requests.get(settings.DANS_FILE_FORMATS_URL)
    dans_formats_json = resp.json()
    # split here preferred-formats and non-preferred formats
    print(dans_formats_json)
    commons.data.update({"dans-file-formats":json.dumps(dans_formats_json)})
    preferred_formats = {"type": "audio", "formats": []} #todo: dans_formats_json
    non_preferred_formats = {"type": "audio", "formats": []} #todo: dans_formats_json
    commons.data.update({"preferred-formats": preferred_formats})
    commons.data.update({"non-preferred-formats": non_preferred_formats})
    return commons.data


if __name__ == "__main__":
    logging.info("Start")
    uvicorn.run("src.main:app", host="0.0.0.0", port=2004, reload=False)
