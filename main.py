import json
import sys
from antlr4 import *
from ExpressoesLexer import ExpressoesLexer
from ExpressoesParser import ExpressoesParser

NEW_FORM = {}

def executeStmt(stmt):
    if stmt.titleStmt():
        executeTitle(stmt.titleStmt())
    elif stmt.descriptionStmt(): 
        executeDescription(stmt.descriptionStmt())
    elif stmt.insertItemTextStmt():
        executeInsertText(stmt.insertItemTextStmt())
    elif stmt.insertItemMultipleChoicetStmt():
        executeInsertMultipleChoice(stmt.insertItemMultipleChoicetStmt())
    elif stmt.insertItemSectionHeadertStmt():
        executeInsertSectionHeader(stmt.insertItemSectionHeadertStmt())
    elif stmt.showStmt():
        executeShow(stmt.showStmt())
    elif stmt.exportStmt():
        executeExport(stmt.exportStmt())
    else:
        raise Exception("Nao identificado")

# OK
def executeTitle(stmt):
    title = stmt.value().getText().replace("'", "")
    if 'info' not in NEW_FORM.keys():
        dict_aux = {'title' : title}
        NEW_FORM['info'] = dict_aux
        print(f"Titulo criado: {title}")
    else:
        raise Exception(f"O formulario ja possui um titulo: {title}")

def executeDescription(stmt): 
    description = stmt.value().getText().replace("'", "")
    if 'info' not in NEW_FORM.keys():
        dict_aux = {'description': description}
        NEW_FORM['info'] = dict_aux
        print(f"Descricao criada: {description}")
    elif 'description' not in NEW_FORM['info'].keys():
        NEW_FORM['info']['description'] = description
        print(f"Descricao criada: {description}")
    else: 
        raise Exception(f"O formulario ja possui uma descricao: {description}")

# OK
def executeInsertText(stmt):
    itemKeys = [col.getText() for col in stmt.itemKeys().ID()]
    values = [val.getText() for val in stmt.values().value()]

    if 'info' in NEW_FORM:
        if 'items' in NEW_FORM.keys():
            NEW_FORM['items'].append({"type": "TEXT",
                                      itemKeys[0].replace("'", ""): values[0].replace("'", ""),
                                      itemKeys[1].replace("'", ""): values[1].replace("'", ""),
                                      "index": len(NEW_FORM['items'])
                                      })
            print(f"Item criado: {values[0].replace("'", "")}")
        else:
            NEW_FORM['items'] = []
            NEW_FORM['items'].append({"type": "TEXT",
                                      itemKeys[0].replace("'", ""): values[0].replace("'", ""),
                                      itemKeys[1].replace("'", ""): values[1].replace("'", ""),
                                      "index": len(NEW_FORM['items'])
                                      })
            print(f"Item criado: {values[0].replace("'", "")}")
    else:
        raise Exception(f"Formulario nao iniciado, e necessario um titulo")

# OK
def executeInsertMultipleChoice(stmt):
    itemKeys = [col.getText() for col in stmt.itemKeys().ID()]
    values = [val.getText() for val in stmt.values().value()]

    if 'info' in NEW_FORM:
        if 'items' in NEW_FORM.keys():
            choices = []
            for i in range(0, len(values)):
                if i != 0 and i != 1:
                    choices.append(values[i].replace("'", ""))

            NEW_FORM['items'].append({"type": "MULTIPLE_CHOICE",
                                      itemKeys[0].replace("'", ""): values[0].replace("'", ""),
                                      itemKeys[1].replace("'", ""): values[1].replace("'", ""),
                                      itemKeys[2].replace("'", ""): choices,
                                      "index": len(NEW_FORM['items'])
                                      })
            print(f"Item criado: {values[0].replace("'", "")}")
        else:
            NEW_FORM['items'] = []

            choices = []
            for i in range(0, len(values)):
                if i != 0 and i != 1:
                    choices.append(values[i].replace("'", ""))

            NEW_FORM['items'].append({"type": "MULTIPLE_CHOICE",
                                      itemKeys[0].replace("'", ""): values[0].replace("'", ""),
                                      itemKeys[1].replace("'", ""): values[1].replace("'", ""),
                                      itemKeys[2].replace("'", ""): choices, "index": len(NEW_FORM['items'])
                                      })
            print(f"Item criado: {values[0].replace("'", "")}")
    else:
        raise Exception(f"Formulario nao iniciado, e necessario um titulo")

# OK
def executeInsertSectionHeader(stmt):
    itemKeys = [col.getText() for col in stmt.itemKeys().ID()]
    values = [val.getText() for val in stmt.values().value()]

    if 'info' in NEW_FORM:
        if 'items' in NEW_FORM.keys():
            NEW_FORM['items'].append({"type": "SECTION_HEADER",
                                      itemKeys[0].replace("'", ""): values[0].replace("'", ""),
                                      itemKeys[1].replace("'", ""): values[1].replace("'", ""),
                                      "index": len(NEW_FORM['items'])})
            print(f"Item criado: {values[0].replace("'", "")}")
        else:
            NEW_FORM['items'] = []
            NEW_FORM['items'].append({"type": "SECTION_HEADER",
                                      itemKeys[0].replace("'", ""): values[0].replace("'", ""),
                                      itemKeys[1].replace("'", ""): values[1].replace("'", ""),
                                      "index": len(NEW_FORM['items'])})
            print(f"Item criado: {values[0].replace("'", "")}")
    else:
        raise Exception(f"Formulario nao iniciado, e necessario um titulo")


# OK
def executeShow(stmt):
    if bool(NEW_FORM):
        json_dict = json.dumps(NEW_FORM, indent=4)
        print(json_dict)
    else:
        raise Exception(f"O formulario vazio")

# OK
def executeExport(stmt):
    if bool(NEW_FORM):
        json_dict = json.dumps(NEW_FORM, indent=4)
        with open('output.json', 'w') as f:
            f.write(json_dict)
        print(f"Arquivo exportado com sucesso")
    else:
        raise Exception(f"O formulario vazio")

# COMMANDS EXAMPLES:
# TITLE 'Cadastro pessoal';
# ITEM TEXT (title, isRequired) VALUES ('Insira seu nome', 'true');
# ITEM PARAGRAPH_TEXT (title, isRequired) VALUES ('Endereco', 'true');
# ITEM MULTIPLE_CHOICE (title, isRequired, choices) VALUES ('Escolha uma opcao', 'false', 'Option 1', 'Option 2', 'Option 3');
# ITEM SECTION_HEADER (title, helpText) VALUES ('This is a title', 'No questions here');
# SHOW;
# EXPORT;

def main():
    input_text = sys.stdin.read()
    input_stream = InputStream(input_text)
    lexer = ExpressoesLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = ExpressoesParser(stream)
    tree = parser.prog()

    # Verifica se houve erro sintático
    if parser.getNumberOfSyntaxErrors() > 0:
        print("erro sintático")
        sys.exit(1)

    for stmt in tree.stmt():
        executeStmt(stmt)

if __name__ == "__main__":
    main()