from dotenv import load_dotenv

load_dotenv(dotenv_path=".env.template")

from runner import Runner

runner = Runner()
runner.run()



