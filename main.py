from src.app import App, create_app

app: App = create_app()

if __name__ == "__main__":
    app.logger.info("Python Project Template by LonelyWolf")
    app.run()
