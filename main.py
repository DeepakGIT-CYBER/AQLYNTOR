from fastapi import FastAPI
from singularity_core import app as v14_app

app = FastAPI(title='AQLYNTOR Supreme Core')
app.mount('/v14', v14_app)

@app.get('/')
def root():
    return {'status': 'AQLYNTOR v14.0 OZSC System Online'}
