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
- 의존성은 알아서 주기적으로 정리해준다. 특별한 사유가 없으면 소스 기반으로 최소한의 의존성만 넣도록 한다. 버전이 중요하지 않다면 아래의 예시로 일괄 적용하는 것도 생각해보자.
    ```sh
    pip install --upgrade pipreqs
    pipreqs --force .
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
pip install --upgrade pip black ruff mypy pylint pytest 'watchdog[watchmedo]'
pip install --requirement requirements.txt
```

설치 편의를 위해 파이썬 환경 설정 및 패키지 설치 과정을 스크립트로 만들어 사용할 수 있다.

_./scripts/setup.sh_
```sh
#!/bin/bash

set -ex

virtualenv venv --python=python3.13
source venv/bin/activate

pip install --upgrade pip black ruff mypy pylint pytest 'watchdog[watchmedo]'
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

#### 2. Ruff

- 목적 : 빠른 린팅 및 자동 수정
- 참고 : https://pypi.org/project/ruff/

```sh
pip install --upgrade ruff
ruff check --fix main.py src tests
```

#### 3. Mypy

- 목적 : 정적 타입 검사
- 참고 : https://pypi.org/project/mypy/

```sh
pip install --upgrade mypy
mypy --strict main.py src tests
```

#### 검증 스크립트로 통합

검증 편의를 위해서 위의 3개 검증 패키지를 순서대로 호출하는 스크립트를 작성해서 사용할 수 있다.

_./scripts/check.sh_
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
    .
```

이를 실행시키면 아무 일도 일어나지 않는데, `*.py` 형식의 코드를 수정하고 저장하게 되면 이를 자동으로 감지해서 `check.sh` 스크립트와 `main.py` 가 실행된다.
이 또한 스크립트로 만들어서 편하고 직관적으로 관리할 수 있다.

_./scripts/start.sh_
```sh
#!/bin/bash

set -ex

./scripts/check.sh
watchmedo shell-command \
    --patterns="*.py" \
    --recursive \
    --command="./scripts/check.sh && python main.py" \
    .
```

사용할 때에는 실행이 가능하도록 파일 권한을 바꾸어주어야 한다.

```sh
chmod +x ./scripts/start.sh
./scripts/start.sh
```