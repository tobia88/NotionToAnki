import yaml
import os

class AnkiConfigData:
    output_deck_name: str
    output_package_name: str

    def __init__(self, config_data: any):
        self.output_deck_name = config_data['output_deck_name']
        self.output_package_name = config_data['output_package_name']
        print(f'ConfigLoader:::AnkiConfigData:::Output Deck Name: {self.output_deck_name}')


class OpenAIConfigData:
    prompt_system_content: str
    prompt_image_format: str

    def __init__(self, config_data: any):
        self.prompt_system_content = config_data['prompt_system_content']
        self.prompt_image_format = config_data['prompt_image_format']
        print('ConfigLoader:::OpenAIConfigData:::Successfully loaded OpenAI config data')


class ConfigLoader:
    language: str
    anki: AnkiConfigData
    openai: OpenAIConfigData
    output_dir: str

    def __init__(self):
        self.load_config()

    def load_config(self) -> None:
        try:
            with open('config.yaml') as f:
                self.config = yaml.safe_load(f)
        except FileNotFoundError:
            print("ConfigLoader:::File not found")
            return

        self.language: str = self.config['language']
        print(f'ConfigLoader:::Language: {self.language}')

        language_lower: str = self.language.lower()

        self.anki = AnkiConfigData(self.config[language_lower]['anki'])
        self.openai = OpenAIConfigData(self.config[language_lower]['openai'])
        self.output_dir = f'output\\{language_lower}'


config_loader = ConfigLoader()

# ensure output directory exists
os.makedirs(config_loader.output_dir, exist_ok=True)

# os.system(f'explorer {config_loader.output_dir}')