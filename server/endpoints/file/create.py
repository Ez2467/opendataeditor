from __future__ import annotations

from typing import Optional

from fastapi import File, Form, Request, UploadFile

# TODO: replace exception class
from frictionless import FrictionlessException
from pydantic import BaseModel

from ... import helpers
from ...project import Project
from ...router import router


class Props(BaseModel, extra="forbid"):
    path: str
    bytes: bytes
    folder: Optional[str] = None
    deduplicate: Optional[bool] = None


class Result(BaseModel, extra="forbid"):
    path: str
    size: int


# TODO: this operation needs to be atomic (has to include file creation and table validation)
# it will allow proper clean-ups in case of errors and better error messages
# (see "/file/fetch" as an example)


@router.post("/file/create")
async def endpoint(
    request: Request,
    file: UploadFile = File(),
    path: Optional[str] = Form(None),
    folder: Optional[str] = Form(None),
    deduplicate: Optional[bool] = Form(None),
) -> Result:
    bytes = await file.read()
    path = path or file.filename or "name"
    return action(
        request.app.get_project(),
        Props(path=path, bytes=bytes, folder=folder, deduplicate=deduplicate),
    )


def action(project: Project, props: Props) -> Result:
    fs = project.filesystem

    # Folder
    path = props.path
    if props.folder:
        folder = fs.get_fullpath(props.folder)
        if not folder.exists():
            raise FrictionlessException("folder does not exist")
        path = str(folder / path)

    # Create
    path = helpers.write_file(
        project, path=path, bytes=props.bytes, deduplicate=props.deduplicate
    )

    return Result(path=path, size=len(props.bytes))
