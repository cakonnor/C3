import yamale
import yaml

# validate config file based on yamale schema
def validateSchema(configPath):
    schema = yamale.make_schema('./schema/schema.yaml')
    try:
        data = yamale.make_data(configPath)
    except FileNotFoundError as err:
        print('Unable to Locate config.yaml file!\n%s' % str(err))
        exit(1)

    try:
        yamale.validate(schema, data)
        return True
    except ValueError as e:
        print('Fatal Error Validation failed!\n%s' % str(e))
        exit(1)


def openFileYaml(path):
    try:
        with open(path, 'r') as stream:
            return True, yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print('Unable to parse ', path)
        return False, ''
    except FileNotFoundError as err:
        print('Unable to locate and or parse', path)
        return False, ''