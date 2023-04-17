import os
import argparse
import subprocess
import json


def runner(composer_config, extra_args):
    """
    Runs the argument stack through docker compose.
    """
    arg_stack = ['docker', 'compose', *composer_config, *extra_args] 
    subprocess.run(
        arg_stack,
        env=os.environ
    )


def flag_parse(key, value) -> list:
    """
    Checks the keys/values and allocates into a list of flags to be sent
    to the output
    """
    config = []
    keystr = "--" + key if len(key) > 1 else "-" + key
    value_list = value if isinstance(value, list) else [value]

    for item in value_list: 
        config.append(keystr)
        config.append(item)
    
    return config


def parse_config():
    """
    Takes the config file and breaks it down into parts
    for running with docker compose. 
    """
    config = load_config()
    docker_configs = {}
    for key, value in config.items():
        tmp_config = []

        for config_flag, config_value, in value.items(): 
            if config_flag == 'env-file': 
                #load_dotenv(config_value)
                continue

            results = flag_parse(config_flag, config_value)
            tmp_config.extend(results)

        docker_configs[key] = tmp_config
    
    return docker_configs


def load_config(file_name="composer.json"):
    """
    Reads the config file
    """
    with open(file_name, "r") as f:
        config = json.load(f)
        return config


def cli_parser():
    parser = argparse.ArgumentParser(    
        description='Welcome to meta-compse! A wrapper to run docker compose environments easier.',
        epilog='Contribute here: https://github.com/dtaivpp/meta-compose')

    parser.add_argument("environment", type=str, help="The name of the environment you want to run")
    parser.add_argument("docker_args", nargs=argparse.REMAINDER)

    args = parser.parse_args()
    docker_configs = parse_config()
    runner(docker_configs[args.environment], args.docker_args)


if __name__=="__main__":
    cli_parser()