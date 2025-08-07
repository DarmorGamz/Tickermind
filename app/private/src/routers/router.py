from fastapi import APIRouter, HTTPException, Request, UploadFile

router = APIRouter()

@router.get("/")
async def handle_get(request: Request):
    varsIn = dict(request.query_params)
    try:
        return await ApiAccess().RunCmd(varsIn)
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
        return await ApiAccess().RunCmd(varsIn)
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        raise HTTPException(500, f"Error processing request: {str(e)}")

class ApiAccess():
    def __init__(self):
        pass

    async def RunCmd(self, varsIn: dict = None):
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
                case "Tickers":
                    import components.stocks.tickers as tickers
                    tickers_instance = tickers.tickers()

                    varsIn1 = {}
                    return await tickers_instance.Gsad(op, varsIn1)
                case _:
                    raise HTTPException(400, "Invalid Cmd")
        except Exception as e:
            raise HTTPException(500, f"Error processing command: {str(e)}")
        