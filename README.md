# Python API Template by LonelyWolf
본 `repository`는 Python 에서 `API Server`를 구축하는 예제를 토대로 `setup/develop/test/deploy/observabillity` `template`을 가이드의 형태로 기록하기 위해 생성하였다.

## 목차
- [Python API Template by LonelyWolf](#python-api-template-by-lonelywolf)
  - [목차](#목차)
  - [시작하기 전, 작성목표](#시작하기-전-작성목표)
  - [계속하기 전, 참고사항](#계속하기-전-참고사항)

## 시작하기 전, 작성목표

개인적인 경험에 의해, 개발 전에 결정하고 세팅 해야 이후 비즈니스 로직에 집중하기 좋다고 생각 되는 부분에 대한 `Python Template` 을 작성하는 것을 목적으로 하고 있다. 또한 Template 의 각 구성요소마다 작성 내용 및 설명을 같이 작성하도록 한다.

개발을 하는 매 순간마다, 아래의 고민을 반복해서 하게 된다.

- 나는 언어의 `language conventions`에 맞춰서 잘 개발하고 있는가?
- 개발시 필요한 `environment`는 개발 단계에 따라 유동적으로 설정 할 수 있는가?
- 내가 작성하고 있는 코드에는 잠재적 `bug` 또는 `version`에 맞지 않는 코드가 있지는 않은가?
- 현재 작성하고 있는 코드는 이전에 작성한 코드의 기능들을 망가뜨리지 않도록 `test` 되었는가?
- `deploy`는 배포 환경에 독립적이고 확장성 있는 사용을 위해 잘 구성 되었는가?
- 프로그램의 `logging`, `metric`과 같은 `observabillity`는 어떻게 확보 할 수 있는가?

이런 고민들은 개발의 템포를 떨어뜨리고, 비즈니스 로직에 집중 할 수 없게 하는 주된 원인이 되기 때문에 대안이 필요하다. 그래서 기술이 선택되면 확정되는 것들(deploy, observabillity)을 미리 정형화여 작성하고, 개발 하는 동안에 계속 고민을 해야하는 부분(conventions, environment, test)은 개발하는 동안 지속적으로 확인 할 수 있는 구성을 설정하여 자동으로 확인 할 수 있도록 한다.

본 가이드의 말미에 `API Server` 서버의 구축과 이를 `Docker`를 사용하여 확장성 있게 배포하기 위한 간단한 가이드를 제시한다.

## 계속하기 전, 참고사항
- 현재 가이드는 `Python 3.13` 버전을 기반으로 `macOS` 에서 작성 되었다. 본 가이드 내용을 토대로 각자 환경에 맞게 구성해야 한다.
- 프로젝트 설정을 위해 [`virtualenv`](https://virtualenv.pypa.io/en/latest/) 등을 사용하여 독립적인 환경을 갖추고 적용한다. `macOS`의 예시는 다음과 같다.
    ```sh
    virtualenv venv --python=python3.13
    source venv/bin/activate
    ```
- `pip` 의 업그레이드는 말하지 않아도 알아서 수행 하도록 한다. 아래 예시를 참고하자.
    ```sh
    pip install --upgrade pip
    ```
- `.gitignore`는 알아서 잘 작성 하도록 한다. 특히 `IDE 설정`과도 같은 개인화된 파일은 꼭 빼주도록 한다.
- 의존성은 알아서 주기적으로 정리해준다. 특별한 사유가 없으면 소스 기반으로 최소한의 의존성만 넣도록 한다. 버전이 중요하지 않다면 아래의 예시로 일괄 적용하는 것도 생각해보자.
    ```sh
    pip install --upgrade pipreqs
    pipreqs --force .
    ```
- `API Server`는 `FastAPI` 를 사용하여 구축할 예정이다.

