# Python Project Template by LonelyWolf
본 `repository`는 `Python Project`를 구축하rl 위한 초기 설정에 대해 `setup/develop/test/deploy/observabillity` 관점에서 `template`을 가이드의 형태로 기록하기 위해 생성하였다.

## 목차
- [Python Project Template by LonelyWolf](#python-project-template-by-lonelywolf)
  - [목차](#목차)
  - [시작하기 전, 작성목표](#시작하기-전-작성목표)
  - [계속하기 전, 참고사항](#계속하기-전-참고사항)
  - [이어서 계속하기](#이어서-계속하기)
    - [프로젝트 기본 구조 잡기](#프로젝트-기본-구조-잡기)
    - [프로젝트 환경 설정하기 : 검증 자동화를 위한 패키지 설치](#프로젝트-환경-설정하기--검증-자동화를-위한-패키지-설치)
      - [1. Black](#1-black)
      - [2. Ruff](#2-ruff)
      - [3. Mypy](#3-mypy)
      - [검증 스크립트로 통합](#검증-스크립트로-통합)

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

## 이어서 계속하기

### 프로젝트 기본 구조 잡기

- `root`            - 프로젝트 기본 폴더
  - `scripts/`          - 프로젝트 편의를 위한 스크립트 모음 폴더
    - `setup.sh`            - 프로젝트 초기 셋업을 위한 설정 및 패키지 다운로드 스크립트
    - `check.sh`            - 지속적 품질 검사를 수행하기 위한 스크립트
    - `start.sh`            - 프로그램 실행을 위한 스크립트
    - `watch.sh`            - 프로젝트 변경을 감지하여 피드백을 주기 위한 스크립트
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

### 프로젝트 환경 설정하기 : 검증 자동화를 위한 패키지 설치

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

검증 편의를 위해서 위의 3개 검증 패키지를 순서대로 호출하는 스크립트를 작성해서 사용하면 편하다.

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
```
