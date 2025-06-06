from blocktype import BlockType

def markdown_to_blocks(markdown):
    split_string = [block.strip() for block in markdown.split("\n\n")]
    blocks = []
    for block in split_string:
        if block != "":
            blocks.append(block)
    return blocks

def block_to_blocktype(block):
    
    if block == "":
        return BlockType.PARAGRAPH
    heading_prefix = ("# ", "## ", "### ", "#### ", "##### ", "###### ")
    unordered_list_prefix = ("- ")
    code_prefix = ("```")
    quote_prefix = (">")
    is_quote = True
    is_unordered_list = True
    is_ordered_list = True
    count = 0
    split_block = block.split("\n")

    if block.startswith(heading_prefix): 
        return BlockType.HEADING
    
    if block.startswith(code_prefix) and block.endswith(code_prefix):
        return BlockType.CODE
    
    for line in split_block:
        if not line.startswith(quote_prefix):
            is_quote = False
    if is_quote is True:
        return BlockType.QUOTE
    
    for line in split_block:
        if not line.startswith(unordered_list_prefix):
            is_unordered_list = False
    if is_unordered_list is True:
        return BlockType.UNORDERED_LIST
        
    for line in split_block:
        count += 1
        ordered_list_prefix = (f"{count}. ")
        if not line.startswith(ordered_list_prefix):
            return BlockType.PARAGRAPH

    return BlockType.ORDERED_LIST
            


