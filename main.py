from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from datetime import datetime
from passlib.context import CryptContext

from starlette.responses import RedirectResponse

import db

passw = CryptContext(schemes=['bcrypt'], deprecated='auto')
app = FastAPI()
app.mount('/static', StaticFiles(directory='static'))
app.add_middleware(SessionMiddleware, secret_key='asfklqjwefijasfkljm12384712klzf')

template = Jinja2Templates(directory='templates')


@app.get('/', response_class=HTMLResponse)
def index(request: Request):
    current_year = datetime.now().year
    return template.TemplateResponse('index.html', {'request': request, 'current_year': current_year})


@app.post('/action_reg', response_class=HTMLResponse)
def action_reg(request: Request, email: str = Form(...), password: str = Form(...)):
    new_pass = passw.hash(password)
    db.reg(email, new_pass)
    return RedirectResponse(url='/', status_code=303)


@app.post('/action_auth', response_class=HTMLResponse)
def action_auth(request: Request, email: str = Form(...), password: str = Form(...)):
    password_hash = db.get_hash(email)
    if passw.verify(password, password_hash):
        request.session['login'] = email
    return RedirectResponse(url='/', status_code=303)


@app.get('/lk', response_class=HTMLResponse)
def lk(request: Request):
    if 'login' in request.session:
        vebinars = db.get_vebinars()
        vebinars_new = []
        for v in vebinars:
            video = v[3].split('/')[-2]
            vebinars_new.append((v[0], v[1], v[2], video, v[4], v[5], v[6]))

        return template.TemplateResponse('lk/index.html', {'request': request,'vebinars': vebinars_new})
    return RedirectResponse(url='/', status_code=303)


@app.get('/logout', response_class=HTMLResponse)
def logout(request: Request):
    if 'login' in request.session:
        del request.session['login']
    return RedirectResponse(url='/')


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, port=8007)
