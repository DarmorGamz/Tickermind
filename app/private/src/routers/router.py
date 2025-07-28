from fastapi import APIRouter, HTTPException, Request, UploadFile

router = APIRouter()

@router.get("/")
def handle_get(request: Request):
    varsIn = dict(request.query_params)
    try:
        return ApiAccess().RunCmd(varsIn)
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        raise HTTPException(500, f"Error processing request: {str(e)}")

@router.post("/")
async def handle_post(request: Request):
    form = await request.form()
    body = {k: v for k, v in form.items() if not isinstance(v, UploadFile)}
    files = {k: v for k, v in form.items() if isinstance(v, UploadFile)}
    body.update(files)

    varsIn = dict(request.query_params)
    varsIn.update(body)
    try:
        return ApiAccess().RunCmd(varsIn)
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        raise HTTPException(500, f"Error processing request: {str(e)}")

class ApiAccess():
    def __init__(self):
        pass

    def RunCmd(self, varsIn: dict = None):
        try:
            cmd = varsIn.get("Cmd")
            if cmd is None:
                raise HTTPException(400, "Cmd required: {cmd}")
            
            parts = cmd.split(".")
            if len(parts) == 2:
                model, op = parts
        
            match model:
                case "Ping":
                    return {"message": "pong"}
                case _:
                    raise HTTPException(400, "Invalid Cmd")
        except Exception as e:
            raise HTTPException(500, f"Error processing command: {str(e)}")
        