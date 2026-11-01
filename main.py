from fastapi import FastAPI
from singularity_core import app as v14_app

app = FastAPI(
    title='AQLYNTOR v14.0 Omniversal Zero-Point Singularity Core',
    description='Beyond AI & Standard Computing',
    version='14.0.0'
)

app.mount('/v14', v14_app)

@app.get('/')
def root():
    return {
        'status': 'ONLINE',
        'version': 'v14.0-OZSC',
        'sole_architect': 'Deepak Reddy (M.Tech CSE)',
        'paradigm': 'Omniversal Zero-Point Singularity Core',
        'patent_watermark': 'Exclusive Intellectual Property of Deepak Reddy. Protected Worldwide.'
}

