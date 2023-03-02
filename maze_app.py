import io
import os
import base64
import zipfile

from uuid import uuid4

from typing import Dict, Union, Optional, List

from fastapi import FastAPI, Response, UploadFile, Form
from fastapi.responses import StreamingResponse, HTMLResponse

from maze_methods import generate_maze_, draw_maze, filter_maze_passages
from path_finding import (djikstra, a_star, bfs, dfs, bellman_ford,
                          bidirectional_search, beam_search)

app = FastAPI()
FILE_PREF = 'maze_data' if 'maze_algorithms' in os.getcwd() else '/tmp/'


@app.get('/')
async def main() -> Dict:
    """
    A FastAPI endpoint that returns a JSON response with a
    message about the application.

    Returns:
        A dictionary containing a message about the application.
    """
    return {"data": """This is a FastAPI implementation to create \
and solve mazes through various algorithms!""", 'maze_generator':
           '/maze_generator', 'maze_solver': '/uploud_maze'}


@app.get('/maze_generator', response_class=HTMLResponse)
async def maze_generator() -> HTMLResponse:
    """
    Returns the HTML response for the maze generator form.

    Returns:
        HTMLResponse: An HTML response containing the maze generator form.
    """
    headers = {
        "Cache-Control": "no-cache, no-store, must-revalidate",
        "Pragma": "no-cache",
        "Expires": "0",
    }
    with open(os.path.join('html_responses', 'maze_generator_form.html'),
              'r') as f:
        response_ = f.read()
    return HTMLResponse(response_, headers=headers)


@app.get("/download/{type_}/{name_}")
async def stream_image(type_: str, name_: str):
    """
    This endpoint serves for downloading files generated by the maze generator.

    Parameters:
    -----------
    type_: str
        Type of file to download. Possible values: "image", "text" or "zip".
    name_: str
        Name of the file to download.

    Returns:
    --------
    Union[StreamingResponse, Response, FileResponse]
        The file to be downloaded in the appropriate format,
        depending on the `type_` parameter.
    """
    if type_ == 'image':
        with open(os.path.join(FILE_PREF, f'{name_}.png'), 'rb') as f:
            image_data = f.read()
        response = StreamingResponse(io.BytesIO(image_data),
                                     media_type="image/jpeg")
        response.headers["Content-Disposition"
                         ] = f'attachment; filename="{name_}.png"'
        response.headers["Cache-Control"
                         ] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        delete_temp_files()
        return response
    elif type_ == 'text':
        with open(os.path.join(FILE_PREF, f'{name_}.json'), 'rb') as f:
            maze_dict = eval(f.read())
        response = Response(content=str(maze_dict))
        response.headers["Content-Disposition"
                         ] = f"attachment; filename={name_}.json"
        response.headers["Content-Type"] = "text/plain"
        delete_temp_files()
        return response
    elif type_ == 'zip':
        file_list = [os.path.join(FILE_PREF, f'{name_}.png'),
                     os.path.join(FILE_PREF, f'{name_}.json')]
        zip_ = zipfiles(file_list)
        delete_temp_files()
        return zip_


@app.get('/generate_maze')
async def generate_maze(width: int, height: int, strict: float,
                        weight: float, name_: Union[str, None] = None,
                        img_show: bool = False, download: int = 0
                        ) -> HTMLResponse:
    """
    Generates a maze with the given width and height, using the given `strict`
    value and `weight` probability to add weights to the maze edges.
    If `name_` is not provided, a random UUID will be generated to
    name the maze. If `img_show` is True, the maze image will be displayed in
    the HTML response. If `download` is non-zero, the corresponding file(s)
    will be available for download. Returns an HTMLResponse containing the
    generated maze and options for downloading it in various formats.

    :param width: The width of the maze.
    :param height: The height of the maze.
    :param strict: The strictness of the maze.
    :param weight: The probability of adding weights to the maze edges.
    :param name_: The name of the maze.
    :param img_show: A flag indicating whether the maze image should be
        displayed.
    :param download: A flag indicating whether files should be available
        for download.
    :return: An HTMLResponse containing the generated maze and
        download options.
    """
    delete_temp_files()
    name_ = str(uuid4()) if not name_ else name_
    maze_dict: Dict = generate_maze_(width=width, height=height, strict=strict,
                                     add_weights_prob=weight, name_=name_)
    maze_image, _ = draw_maze(maze_dict, name_=name_)

    buffer = io.BytesIO()
    maze_image.save(buffer, format="JPEG")
    image_data = buffer.getvalue()
    image_base64 = base64.b64encode(image_data).decode()

    return HTMLResponse(f"""
    <html>
    <body {'onload="download__()"' if download != 0 else delete_temp_files()}>
        {'' if img_show else '<!--'
        }<img src="data:image/jpeg;base64,{image_base64}" />{
            '' if img_show else '-->'}
        <p></p>
        <p>{maze_dict}</p>

        <a id="download-link" href="/download/{
            'image' if download == 1 else 'text'
            if download == 2 else 'zip'}/{name_}" style="display:none"></a>
        <script>
        function download__() {{
            var downloadLink = document.getElementById('download-link');
            downloadLink.click();
        }}
        </script>
    </body>
    </html>
    """, headers={
        "Cache-Control": "no-cache, no-store, must-revalidate",
        "Pragma": "no-cache",
        "Expires": "0",
    })


@app.get("/upload_maze", response_class=HTMLResponse)
async def upload_maze() -> HTMLResponse:
    """
    A route for uploading a maze.

    Returns:
        HTMLResponse: An HTML response with a maze uploader form.
    """
    with open(os.path.join('html_responses', 'maze_uploader.html'), 'r') as f:
        response_ = f.read()
    return HTMLResponse(response_)


@app.post("/maze_solver")
async def maze_solver(file: UploadFile = Form(...),
                      solve_algorithm: int = Form(...),
                      start_coords: str = Form(...),
                      end_coords: str = Form(...),
                      img_show: Optional[bool] = Form(False),
                      download: int = Form(...)
                      ) -> HTMLResponse:
    """
    A route for solving a maze.

    Args:
        file (UploadFile): The uploaded maze file.
        solve_algorithm (int): The algorithm used to solve the maze.
        start_coords (str): The starting coordinates of the maze in
            the form "x,y".
        end_coords (str): The ending coordinates of the maze in the form "x,y".
        img_show (Optional[bool], optional): Whether or not to display the
            maze image. Defaults to False.
        download (int): The type of download to offer after solving the maze.
            0 for no download, 1 for image only, 2 for text only, 3 for both.

    Returns:
        HTMLResponse: An HTML response with the solved maze image, path,
        and download link.
    """
    file_contents = await file.read()

    start_coords = [int(i) for i in start_coords.split(',')]
    start_coords = (start_coords[0], start_coords[1])
    end_coords = [int(i) for i in end_coords.split(',')]
    end_coords = (end_coords[0], end_coords[1])

    methods_ = [djikstra, a_star, bfs, dfs, bellman_ford,
                bidirectional_search, beam_search]
    path = methods_[solve_algorithm](filter_maze_passages(eval(file_contents)),
                                     start_coords, end_coords)
    maze_image, image_name = draw_maze(eval(file_contents), path)
    image_name = image_name.replace(FILE_PREF, '').replace(
        '/', '').split('.')[0].replace('\\', '')
    with open(os.path.join(FILE_PREF, image_name + '.json'), 'w') as f:
        f.write(str(path))

    buffer = io.BytesIO()
    maze_image.save(buffer, format="JPEG")
    image_data = buffer.getvalue()
    image_base64 = base64.b64encode(image_data).decode()

    return HTMLResponse(f"""
    <html>
    <body {'onload="download__()"' if download != 0 else delete_temp_files()}>
        {'' if img_show else '<!--'
        }<img src="data:image/jpeg;base64,{image_base64}" />{
            '' if img_show else '-->'}
        <p></p>
        <p>{path}</p>

        <a id="download-link" href="/download/{
            'image' if download == 1 else 'text'
            if download == 2 else 'zip'}/{
                image_name.replace(FILE_PREF, '').replace(
                    '/', '').split('.')[0]}" style="display:none"></a>
        <script>
        function download__() {{
            var downloadLink = document.getElementById('download-link');
            downloadLink.click();
        }}
        </script>
    </body>
    </html>
    """, headers={
        "Cache-Control": "no-cache, no-store, must-revalidate",
        "Pragma": "no-cache",
        "Expires": "0",
    })


def delete_temp_files() -> None:
    """
    Deletes all temporary files in the specified file prefix directory.
    """
    for filename in os.listdir(FILE_PREF):
        file_path = os.path.join(FILE_PREF, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Error deleting file {file_path}: {e}")


def zipfiles(file_list: List[str]) -> StreamingResponse:
    """
    Creates a zip file containing the files in the specified
    list of file paths.

    Args:
    file_list (List[str]): A list of file paths to be zipped.

    Returns:
    StreamingResponse: A streaming response that is a zip file
    containing the specified files.
    """
    io_ = io.BytesIO()
    zip_sub_dir = FILE_PREF
    zip_filename = zip_sub_dir.replace('/', '') + '.zip'
    with zipfile.ZipFile(io_, mode='w',
                         compression=zipfile.ZIP_DEFLATED) as zip:
        for fpath in file_list:
            zip.write(fpath)
        zip.close()
    return StreamingResponse(
        iter([io_.getvalue()]),
        media_type="application/x-zip-compressed",
        headers={"Content-Disposition": f"attachment;filename={zip_filename}"}
    )
