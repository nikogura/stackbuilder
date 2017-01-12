import re
import types

def replaceTokens(project, text):
    if text == None:
        return text

    # import project.locations level tokens
    text = __replDictTokens(project.locations, text)

    # replace project level tokens
    text = __replObjectTokens(project, text)

    return text

def __replDictTokens(data, text):
    for key, value in data.items():
        if isinstance(value, types.StringType):
            token = '\$\{' + key + '\}'
            text = re.sub(token, value, text)

    return text

def __replObjectTokens(object, text):
    if text == None:
        return text

    for key, value in object.__dict__.iteritems():
        if isinstance(value, types.StringType):
            token = '\$\{' + key + '\}'
            text = re.sub(token, value, text)
        elif isinstance(value, types.InstanceType):
            None
        else:
            #print "Type: " + str(type(value))
            token = '\$\{' + key + '\}'
            #print "Value: " + str(value)
            text = re.sub(token, str(value), text)

    return text
