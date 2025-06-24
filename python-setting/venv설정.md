## ✅ 1. 가상환경 생성 (터미널에서)

```bash
python -m venv venv
```

* 현재 프로젝트 폴더 안에 `venv/`라는 폴더가 생깁니다.
* 해당 폴더 안에는 독립적인 Python 실행 환경이 구성됩니다.

---

## ✅ 2. 가상환경 활성화

### Windows:

```bash
venv\Scripts\activate
```

### macOS/Linux:

```bash
source venv/bin/activate
```

> 활성화되면 터미널 앞에 `(venv)`가 표시됩니다.

---

## ✅ 3. VS Code에서 venv 인식시키기

### 방법 A: VS Code가 자동으로 venv를 인식하지 않는 경우

1. `Ctrl + Shift + P` (Command Palette 열기)
2. `Python: Select Interpreter` 입력 후 선택
3. 목록 중 `./venv/bin/python` (또는 `.\venv\Scripts\python.exe`) 선택

### 방법 B: `.vscode/settings.json` 파일에 명시

```json
{
  "python.pythonPath": "venv/bin/python"  // Windows는 "venv\\Scripts\\python.exe"
}
```

> 이렇게 하면 VS Code가 항상 지정된 venv 환경을 사용합니다.

---

## ✅ 4. 필요한 패키지 설치

```bash
pip install -r requirements.txt
```

> 설치된 패키지는 `venv` 안에만 적용됩니다.

---

## ✅ 5. `requirements.txt`로 패키지 목록 저장 (협업/배포용)

```bash
pip freeze > requirements.txt
```

> 나중에 서버나 다른 컴퓨터에서도 `pip install -r requirements.txt`로 동일한 환경 구축 가능.

---

## ✅ 6. (선택) `.venv/` 폴더는 Git 등에서 제외

`.gitignore`에 추가:

```
venv/
```


