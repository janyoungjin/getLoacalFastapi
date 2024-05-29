from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse,JSONResponse
import uvicorn

app = FastAPI()

# 데이터 로드 및 KNN 모델 학습
df = pd.read_csv("https://raw.githubusercontent.com/janyoungjin/localData/main/data.csv")
knn = KNeighborsClassifier()
knn.fit(df[['경도','위도']], df['지역명'])

@app.get("/")
def  index():
    return HTMLResponse(f"<center><h1>각 지역별 경도와 위도</h1>{df.to_html(index=False,escape=False)}</center>")
# 경도가 x, 위도가 y
@app.post("/getlocal")
def get_result(x: str = Form(...), y: str = Form(...)):
    x = float(x)
    y = float(y)
    
    if 33.2533 < y < 38.37881 and 126.10863 < x < 129.365:#한국 안에 있다면?(경도 위도 출처 : chatgpt)
        prediction = knn.predict([[x, y]])
        local = prediction[0]
    else:
        local = '외국'
    return JSONResponse({'local': local})


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)