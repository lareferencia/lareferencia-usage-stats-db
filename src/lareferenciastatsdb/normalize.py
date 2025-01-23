import re

# pattern for an OAI identifier of the form oai:identifier_prefix:unique_part, the indentifier prefix could have https:// or http:// prefixes, 
# and trailing slashes folowed by subfolders, so we remove want to have separted groups for the identifier prefix and the unique part, 
# we will use the groups to normalize the identifier, removing the prefix https and trailing parts after the slashes, also the unique part 
OAI_IDENTIFIER_PATTERN =        re.compile(r"^(oai:)(?:https?://)?([^/]+)(?:/[^:]+)*(:.*)$")
OAI_IDENTIFIER_PREFIX_PATTERN = re.compile(r"^(oai:)(?:https?://)?([^/:]+)(?:/.+)?")


# normalize an oai-pmh identifier of the form oai:identifier_prefix:identifier removing https:// and http:// prefixes, and trailing slashes
def extract_oai_identifier_prefix(identifier):
    
    # match the identifier against the pattern
    match = OAI_IDENTIFIER_PREFIX_PATTERN.match(identifier)

    if match:
        # return the identifier prefix
        return match.group(1) + match.group(2)
    else:
        return identifier
    
def normalize_oai_identifier(identifier):

    match = OAI_IDENTIFIER_PATTERN.match(identifier)

    if match:
        return match.group(1) + match.group(2) + match.group(3)
    else:
        return identifier

def normalize_oai_identifier_prefix(identifier):

    match = OAI_IDENTIFIER_PREFIX_PATTERN.match(identifier)

    if match:
        return match.group(1) + match.group(2)
    else:
        return None


# if main test the function

if __name__ == "__main__":

    # create an array with test cases, with http://, https://, and without prefix
    test_cases = [
        "oai:example.com",
        "oai:example.com:123",
        "oai:http://example.com:123",
        "oai:https://example.com:123.2344daa",
        "oai:example.com/subfolder:123",
        "oai:http://example.com/subfolder:123",
        "oai:https://example.com/subfolder:123",
        "oai:repositorio.imdeananociencia.org/rest:20.500.12614/3703"
    ]


    # iterate over the test cases
    for test_case in test_cases:
        # print the original identifier
        print( "Test case: ", test_case, " ---> "," Normalized: ", normalize_oai_identifier(test_case), " Extracted prefix: ", extract_oai_identifier_prefix(test_case) )
        
