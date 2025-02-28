# Python Project Template by LonelyWolf
본 `repository`는 `Python Project`를 구축하rl 위한 초기 설정에 대해 `setup/develop/test/deploy/observabillity` 관점에서 `template`을 가이드의 형태로 기록하기 위해 생성하였다.

## 목차
- [Python Project Template by LonelyWolf](#python-project-template-by-lonelywolf)
  - [목차](#목차)
  - [시작하기 전, 작성목표](#시작하기-전-작성목표)
  - [계속하기 전, 참고사항](#계속하기-전-참고사항)
  - [개발하기 위한 사전준비](#개발하기-위한-사전준비)
    - [프로젝트 기본 구조 잡기](#프로젝트-기본-구조-잡기)
    - [프로젝트 환경 설정](#프로젝트-환경-설정)
    - [품질 관리를 위한 패키지 적용](#품질-관리를-위한-패키지-적용)
      - [1. Black](#1-black)
      - [2. Ruff](#2-ruff)
      - [3. Mypy](#3-mypy)
      - [검증 스크립트로 통합](#검증-스크립트로-통합)
  - [개발시 지속적으로 품질을 관리하자](#개발시-지속적으로-품질을-관리하자)
    - [1. Watchdog(Watchmedo)](#1-watchdogwatchmedo)
    - [2. Logging](#2-logging)
    - [3. Dynamic environment by profile](#3-dynamic-environment-by-profile)
  - [코드 커밋시 테스트를 수행하자](#코드-커밋시-테스트를-수행하자)
    - [1. Pylint](#1-pylint)
    - [2. Pytest](#2-pytest)
    - [Pre-Commit 로 자동화](#pre-commit-로-자동화)

## 시작하기 전, 작성목표

개인적인 경험에 의해, 개발 전에 결정하고 세팅 해야 이후 비즈니스 로직에 집중하기 좋다고 생각 되는 부분에 대한 `Python Template` 을 작성하는 것을 목적으로 하고 있다. 또한 Template 의 각 구성요소마다 작성 내용 및 설명을 같이 작성하도록 한다.

개발을 하는 매 순간마다, 아래의 고민을 반복해서 하게 된다.

- 나는 언어의 `language conventions`에 맞춰서 잘 개발하고 있는가?
- 개발시 필요한 `environment`는 개발 단계에 따라 유동적으로 설정할 수 있는가?
- 내가 작성하고 있는 코드에는 잠재적 `bug` 또는 `version`에 맞지 않는 코드가 있지는 않은가?
- 현재 작성하고 있는 코드는 이전에 작성한 코드의 기능들을 망가뜨리지 않도록 `test` 되었는가?
- `deploy`는 배포 환경에 독립적이고 확장성 있는 사용을 위해 잘 구성 되었는가?
- 프로그램의 `logging`, `metric`과 같은 `observabillity`는 어떻게 확보할 수 있는가?

이런 고민들은 개발의 템포를 떨어뜨리고, 비즈니스 로직에 집중할 수 없게 하는 주된 원인이 되기 때문에 대안이 필요하다. 그래서 기술이 선택되면 확정되는 것들(deploy, observabillity)을 미리 정형화여 작성하고, 개발 하는 동안에 계속 고민을 해야하는 부분(conventions, environment, test)은 개발하는 동안 지속적으로 확인할 수 있는 구성을 설정하여 자동으로 확인할 수 있도록 한다.

## 계속하기 전, 참고사항

- 현재 가이드는 `Python 3.13` 버전을 기반으로 `macOS` 에서 작성 되었다. 본 가이드 내용을 토대로 각자 환경에 맞게 구성해야 한다.
- 프로젝트 설정을 위해 [`virtualenv`](https://virtualenv.pypa.io/en/latest/) 등을 사용하여 독립적인 환경을 갖추고 적용한다. `macOS`의 예시는 다음과 같다.
    ```sh
    virtualenv venv --python=python3.13
    source venv/bin/activate
    ```
- `pip`의 업그레이드는 말하지 않아도 알아서 수행 하도록 한다. 아래 예시를 참고하자.
    ```sh
    pip install --upgrade pip
    ```
- `.gitignore`는 알아서 잘 작성 하도록 한다. 특히 `IDE 설정`과도 같은 개인화된 파일은 꼭 빼주도록 한다.
- 의존성은 알아서 주기적으로 정리해준다. 불필요한 패키지는 삭제하고 아래 명령을 수행해주면 된다.
    ```sh
    pip list --format=freeze > requirements.txt
    ```

## 개발하기 위한 사전준비

### 프로젝트 기본 구조 잡기

- `root`            - 프로젝트 기본 폴더
  - `scripts/`          - 프로젝트 편의를 위한 스크립트 모음 폴더
    - `setup.sh`            - 프로젝트 초기 셋업을 위한 설정 및 패키지 다운로드 스크립트
    - `check.sh`            - 지속적 품질 검사를 수행하기 위한 스크립트
    - `start.sh`            - 프로그램 실행을 위한 스크립트
    - `test.sh`             - analyze & test 관련 스크립트
    - `deploy.sh`           - build & deploy 관련 스크립트
  - `src/`              - main.py 를 제외한 실제 프로그램 코드가 존재하는 폴더
    - `app.py`              - 실제 프로그램의 초기화 및 EntryPoint로 사용되는 파일
  - `tests/`            - test suit 를 모아놓는 폴더
    - `test_main.py`        - 기본 테스트를 위한 임시 파일. 빈 프로젝트에서 1개 이상의 테스트가 없으면 추후 check 과정에서 오류가 발생
  - `.gitignore`        - git에서 제외할 목록을 작성하는 파일. 개인화 파일은 전부 추가하여 git에서 제외될 수 있도록 함
  - `main.py`           - 프로그램의 코드상 EntryPoint
  - `pyproject.toml`    - 프로젝트 및 패키지 설정을 위한 파일
  - `README.md`         - 프로젝트 문서화를 위한 기본 파일
  - `requirements.txt`  - 프로젝트 패키지 의존성 관리를 위한 파일

### 프로젝트 환경 설정

> 파이썬의 버전 호환성을 위한 가상환경을 설치하고, 필요한 패키지를 설치하는 과정.

```sh
virtualenv venv --python=python3.13
source venv/bin/activate
pip install --requirement requirements.txt
```

설치 편의를 위해 파이썬 환경 설정 및 패키지 설치 과정을 스크립트로 만들어 사용할 수 있다.

_[./scripts/setup.sh](./scripts/setup.sh)_
```sh
#!/bin/bash

set -ex

virtualenv venv --python=python3.13
source venv/bin/activate

pip install --requirement requirements.txt
```

사용할 때에는 실행이 가능하도록 파일 권한을 바꾸어주어야 한다. 또한, `source venv/bin/activate` 가 격리된 프로세스에서 실행 되었기 때문에 스크립트로 설치혀면 `activate`는 따로 한번 더 실행 해주어야 한다. (새로운 세션을 열면 잊지 말고 수행할 것)

```sh
chmod +x ./scripts/setup.sh
./scripts/setup.sh
source venv/bin/activate
```

### 품질 관리를 위한 패키지 적용

> 코드 스타일, 표준 준수, 정작 타이핑을 위한 패키기 적용 방법. `프로젝트 환경 설정하기`를 진행했다면 설치 과정은 생략해도 된다.

#### 1. Black

- 목적 : 코드 스타일 정리 (자동 포맷팅)
- 참고 : https://pypi.org/project/black/

```sh
pip install --upgrade black
black main.py src tests
```

[pyproject.toml](pyproject.toml) 에 관련 설정을 넣는다.

```toml
[tool.black]
line-length = 88
target-version = ['py313']
skip-string-normalization = false
skip-magic-trailing-comma = false
```

#### 2. Ruff

- 목적 : 빠른 린팅 및 자동 수정
- 참고 : https://pypi.org/project/ruff/

```sh
pip install --upgrade ruff
ruff check --fix main.py src tests
```

[pyproject.toml](pyproject.toml) 에 관련 설정을 넣는다.

```toml
[tool.ruff]
line-length = 88
target-version = "py313"
show-fixes = true
unsafe-fixes = false
lint.select = [
    "B",    # bugbear
    "D",    # pydocstyle
    "E",    # pycodestyle
    "F",    # Pyflakes
    "W",    # pycodestyle
    "I",    # isort
    "RUF",  # ruff
    "UP",   # pyupgrade
    "C90",  # mccabe
]
lint.ignore = [
    "B905",     # `zip()` without an explicit `strict=` parameter
    "D100",     # Missing docstring in public module
    "D101",     # Missing docstring in public class
    "D102",     # Missing docstring in public method
    "D103",     # Missing docstring in public function
    "D104",     # Missing docstring in public package
    "D105",     # Missing docstring in magic method
    "D106",     # Missing docstring in public nested class
    "D107",     # Missing docstring in __init__
    "D203",     # 1 blank line required before class docstring
    "D205",     # 1 blank line required between summary line and description
    "D212",     # Multi-line docstring summary should start at the second line
    "D400",     # First line should end with a period
    "D401",     # First line of docstring should be in imperative mood
    "E501",     # Line too long ({width} > {limit})
    "RUF012",   # mutable default values in class attributes
]
```

#### 3. Mypy

- 목적 : 정적 타입 검사
- 참고 : https://pypi.org/project/mypy/

```sh
pip install --upgrade mypy
mypy --strict main.py src tests
```

[pyproject.toml](pyproject.toml) 에 관련 설정을 넣는다.

```toml
[tool.mypy]
python_version = "3.13"
ignore_missing_imports = true
warn_return_any = true
warn_unused_configs = true
```

#### 검증 스크립트로 통합

검증 편의를 위해서 위의 3개 검증 패키지를 순서대로 호출하는 스크립트를 작성해서 사용할 수 있다.

_[./scripts/check.sh](./scripts/check.sh)_
```sh
#!/bin/bash

set -ex

black main.py src tests
ruff check --fix main.py src tests
mypy --strict main.py src tests
```

사용할 때에는 실행이 가능하도록 파일 권한을 바꾸어주어야 한다.

```sh
chmod +x ./scripts/check.sh
./scripts/check.sh
```

## 개발시 지속적으로 품질을 관리하자

`지속적인 품질 관리`는 서비스 전체의 품질에 큰 영향을 미친다. 또한 동일 조직간의 품질 관리 방향성을 동일하게 하는 것 또한 향후 `유지보수`를 용이하게 만든다. 

보통 `IDE`에 통합된 `lint` 등을 사용하여 확인할 수가 있는데, `error`가 아닌 `warning` 정도는 무시하고 개발을 하거나(필자는 왜 노란줄과 경거 메세지가 뜨는데 그걸 굳이 무시하는지 이해가 가지 않는다..), 관련 표시 설정을 `disable` 하는 사람들이 많다.

또 하나의 방법으로 이를 위해서 `품질 관리 패키지`를 사용하고 이를 위한 `설정을 공유`하는 방법을 많이 사용하는데, 그럼에도 불구하고 잘 지켜지지 않는 경우들이 많다. 그러다보면 `CI/CD` 과정에 품질관리 및 테스트 과정에서 테스트를 통과하지 못하여, 한번에 몰아서 고치거나 테스트는 빼고 품질 검증은 skip 하는 식으로 처리되어 결국 점점 `기술부채`가 쌓여간다.

그래서 제안하는 방법은, 매번 파일의 변경이 일어날 때마다 품질검증을 다시하고 성공시 프로그램을 재기동 하고 실패시 종료시키도록 하는 것이다. 이를 위해 `watchdog` 패키지 내의 `watchmedo`를 사용하려 한다.

### 1. Watchdog(Watchmedo)

- 목적 : 파일 변경 감지를 통한 자동화 가능
- 참고 : https://pypi.org/project/watchdog/

```sh
pip install --upgrade 'watchdog[watchmedo]'
watchmedo shell-command \
    --patterns="*.py" \
    --recursive \
    --command="./scripts/check.sh && python main.py" \
    --drop \
    .
```

이를 실행시키면 아무 일도 일어나지 않는데, `*.py` 형식의 코드를 수정하고 저장하게 되면 이를 자동으로 감지해서 `check.sh` 스크립트와 `main.py` 가 실행된다.
이 또한 스크립트로 만들어서 편하고 직관적으로 관리할 수 있다.

_[./scripts/start.sh](./scripts/start.sh)_
```sh
#!/bin/bash

set -ex

./scripts/check.sh
watchmedo shell-command \
    --patterns="*.py" \
    --recursive \
    --command="./scripts/check.sh && python main.py" \
    --drop \
    .
```

사용할 때에는 실행이 가능하도록 파일 권한을 바꾸어주어야 한다.

```sh
chmod +x ./scripts/start.sh
./scripts/start.sh
```

### 2. Logging

로깅시 적절한 로거를 사용하는 것 또한 매우 중요한 부분이다. 내장함수인 `print()` 를 사용하는 것 보다는 `logging.Logger` 를 사용하게 되면 다양한 hander 로 로깅을 할 수 있고, 환경에 따른 로그 레벨도 분리 할 수 있다. 본 template 에서는 console logger 설정만 했으며, 아래의 사항들을 고려하였다.

1. 필요한 정보(시간, 레벨, 위치, 메세지)가 한번에 정해진 규칙으로 보일것
2. 정보들을 한눈에 볼수 있게, 종류별로 잘 정렬이 되어있을 것
3. 주요 포인트에 색깔로 강조를 할 것

> colorlog
> - 목적 : 로그 포멧에 색을 입히기 위함
> - 참고 : https://pypi.org/project/colorlog/
> - 예제 : [src/utils/loggin.py](src/utils/logging.py)

### 3. Dynamic environment by profile

개발을 진행하다 보면 상황에 따라서 다양한 설정값을 사용해야하고, 이를 위해서 여러 세트의 설정 파일을 가지게 된다. 보통 `profile` 또는 `phase` 라는 이름으로 환경을 구분 하는데(여기서는 `profile`을 사용한다), 이에 따라 동적으로 설정값을 변경 하는 것을 제안한다. 보통 이를 위해 `python-dotenv`를 많이 사용하는데, 내부적으로 이를 사용하는 `pydantic` 중의 `pydantic-settings`을 사용하는 방법을 제안한다. 제안하는 방법은 아래의 사항들을 고려하였다.

1. 실행에 필요한 설정들을 `profile`에 따라 다른 파일로 나눈다. 구분하는 형식은, 기본 환경변수인 `.env`를 두고 `profile`에 따라 접미사를 붙인다(예시: `test profile` 인 경우 `.env.test`). Profile 은 환경변수로 전달하되(`PROFILE`를 `key`로 사용), 설정을 찾지 못하거나 환경변수를 찾지 못하는 경우 기본값(`.env`)을 사용한다.

```sh
export PROFILE=test 
```

2. 편의성을 위하여 `start` 스크립트에 인자로 `profile`을 넣을 수 있도록 수정하였다.

```sh
./scripts/start.sh test
```

3. 로그 레벨을 환경변수로 설정 할 수 있도록 수정하였다.

_.env.test_
```sh
app.log.level=DEBUG
```

> pydantic-settings
> - 목적 : 설
> - 참고 : https://pypi.org/project/pydantic-settings/
> - 예제 : [src/settings.py](src/settings.py)

## 코드 커밋시 테스트를 수행하자

`git` 에서는 코드를 `commit` 한다는 것은 곧 push 를 한다는 것이고, `push`를 한다는 것은 다른 사람과 코드를 공유 하겠다는 것이다. 물론 `CI/CD`와 `PR` 및 `Code Review` 과정에서 어느 정도는 검사가 되겠지만, 최대한 로컬에서 테스트를 수행하고 올리는 것이 낫다. 그런데 개발자가 일일이 `분석 및 테스트`를 수행하게 되면 사람에 따라 빈도와 수준이 편차가 생기게 된다. 그렇기 때문에 이를 특정 `프로세스로 만들어 자동화` 해야 한다고 생각한다.

그럼 `commit` 과 `push` 중 언제 자동화 테스트를 수행해야 할까? 여기서는 개인적인 성향을 반영하여 `commit 시 적용하는 것을 기본으로` 하겠다. 최대한 조금씩 자주 하는게 일관된 `개발 템포`를 가져가고 `코드 작성시 안정감`을 줄 수 있다고 생각하기 때문이다. 단, 테스트 커버리지는 설정하지 않겠다. TDD로 하는게 아니라면, 테스트를 작성하는것이 너무 괴롭기 때문이다...

### 1. Pylint

- 목적 : 좀 더 자세한 린팅 (코드 품질 분석)
- 참고 : https://pypi.org/project/pylint/

```sh
pip install --upgrade pylint
pylint main.py src tests
```

[pyproject.toml](pyproject.toml) 에 관련 설정을 넣는다.

```toml
[tool.pylint.messages_control]
disable = [
    "C0114",  # 모듈 docstring 없음 경고 무시
    "C0115",  # 클래스 docstring 없음 경고 무시
    "C0116",  # 함수 docstring 없음 경고 무시
    "C0301",  # line 이 너무 김
    "R0903",  # 너무 적은 public 메서드 경고 무시
]
enable = [
    "E",  # Error
    "W",  # Warning
    "R",  # Refactoring
]

[tool.pylint.format]
max-line-length = 88  # 최대 줄 길이
indent-string = "    "  # 4칸 공백 사용

[tool.pylint.design]
max-args = 5  # 함수의 최대 인자 개수
max-attributes = 10  # 클래스의 최대 속성 개수
max-locals = 15  # 지역 변수 개수 제한
max-returns = 6  # 함수에서 `return` 개수 제한
max-statements = 50  # 함수 내 최대 코드 줄 수 제한
min-public-methods = 0 # class 내의 public method 숫자가 무시. R0903 제외가 안먹어서 1로 줄임

[tool.pylint.similarities]
min-similarity-lines = 10  # 중복 코드 감지 기준 (10줄 이상)
ignore-comments = true  # 주석 제외

[tool.pylint.reports]
output-format = "colorized"  # 색상이 있는 출력 사용
```

### 2. Pytest

- 목적 : 테스트코드 실행 (unittest 대체)
- 참고 : https://pypi.org/project/pytest/

```sh
pip install --upgrade pytest
pytest tests
```

### Pre-Commit 로 자동화

- 목적 : git commit 이전에 `검증/분석/테스트`를 수행하려고
- 참고 : https://pypi.org/project/pre-commit/

```sh
pip install --upgrade pre-commit
pre-commit install

# (Optional) 수동 테스트 용도
pre-commit run --all-files
```

위에서 만든 check.sh 와 pylint, pytest 가 정상 동작 하게 하기 위해서, pylint+pytest 를 스크립트로 만들었다.

_[./scripts/test.sh](./scripts/test.sh)_
```sh
#!/bin/bash

set -ex

pylint main.py src tests
pytest tests
```

사용할 때에는 실행이 가능하도록 파일 권한을 바꾸어주어야 한다.

```sh
chmod +x ./scripts/test.sh
./scripts/test.sh
```

pre-commit이 원하는 대로 동작하기 위해서는 설정 파일을 프로젝트에 추가해주어야 한다.

_[.pre-commit-config.yaml](.pre-commit-config.yaml)_
```yaml
repos:
  - repo: local
    hooks:
      - id: check
        name: Check code quality
        entry: ./scripts/check.sh
        language: script
      - id: test
        name: Analyze and test code
        entry: ./scripts/test.sh
        language: script
```