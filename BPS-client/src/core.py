import time
from yaspin import yaspin
import pyfiglet
import typer
import inquirer
import sys
import os
import json
from markdown_editor import web_edit
from markdown_editor.editor import MarkdownDocument

# used to store all information for files within a BPS directory.
BPSConfigFile = "./BPS.data.json"
app = typer.Typer()


# This code is a cli built for the brain palace system (BPS). the BPS is a way to organize documents and knowledge files
# into a GIT like system.

class BPSclient:
    def __init__(self):
        try:
            f = open(BPSConfigFile, 'rb')
        except OSError:
            print('You are not in a BPS directory')
            sys.exit()

        with f:
            try:
                self.bpsconfig = json.load(f)
                # verification logic
            except json.decoder.JSONDecodeError:
                print('BPS.data.json is not a valid json file')
                sys.exit()

    def updateConfig(self):
        with open(BPSConfigFile, 'w') as f:
            json.dump(self.bpsconfig, f)

    def addTopic(self):
        addTopicquestions = [
            inquirer.Text('topic', message="What is the name of the topic you want to add?"),
            inquirer.Text('description', message="What is the description of this topic?"),
        ]
        answers = inquirer.prompt(addTopicquestions)
        self.bpsconfig['topics'].append(answers)
        self.updateConfig()

    # this function removes or adds a tag or maintainer to a concept
    def editConcept(self, concept, tag, maintainer, remove):
        if remove:
            if tag:
                self.bpsconfig['concepts'][concept]['tags'].remove(tag)
            if maintainer:
                self.bpsconfig['concepts'][concept]['maintainers'].remove(maintainer)
        else:
            if tag:
                self.bpsconfig['concepts'][concept]['tags'].append(tag)
            if maintainer:
                self.bpsconfig['concepts'][concept]['maintainers'].append(maintainer)
        self.updateConfig()

    def addConcept(self):
        topic_choices = []
        topics = self.bpsconfig['topics']
        for topic in topics:
            topic_choices.append(topic['topic'])
        addConceptsquestions = [
            inquirer.Text('concept', message="What is the concept you want to add?"),
            inquirer.Text('maintainers', message="Who are the maintainers of this concept? seperate by commas."),
            inquirer.Text('summary', message="What is the summary of this concept?"),
            inquirer.List('topic',
                          message="What is the topic of this concept?",
                          choices=topic_choices,
                          ),
        ]
        answers = inquirer.prompt(addConceptsquestions)
        maintainers = answers['maintainers'].split(',')
        answers['maintainers'] = maintainers
        concept = {
            'concept': answers['concept'],
            'maintainers': maintainers,
            'summary': answers['summary'],
            'topic': answers['topic'],
            'tags': [],
        }
        self.bpsconfig['concepts'].append(concept)
        self.updateConfig()
        # create concept file with create date and other info into a [concept].md
        file_content = '''# {concept}'''.format(concept=concept['concept'])
        with open(concept['concept'] + '.md', 'w') as f:
            f.write(file_content)

    def removeConcept(self, concept):
        self.bpsconfig['concepts'].remove(concept)
        self.updateConfig()
        # remove concept file
        os.remove(concept['concept'] + '.md')

    def removeTopic(self, topic):
        self.bpsconfig['topics'].remove(topic)
        self.updateConfig()

    def getConcepts(self):
        return self.bpsconfig['concepts']

    def getTopics(self):
        return self.bpsconfig['topics']

    def getConcept(self, concept):
        for c in self.bpsconfig['concepts']:
            if c['concept'] == concept:
                return c
        return None

    def getTopic(self, topic):
        for t in self.bpsconfig['topics']:
            if t['topic'] == topic:
                return t
        return None

def viewConcept(concept):
    # open concept file in editor
    web_edit.edit(concept['concept'] + '.md')


# this function is used to print the summary of a concept
def printConcept(concept):
    print('\033[1m' + concept['concept'] + '\033[0m')
    print(concept['summary'])
    print('maintainers: ' + str(concept['maintainers']))
    print('tags: ' + str(concept['tags']))
    print('topic: ' + str(concept['topic']))
    print('\n')


# this function is used to print the summary of a topic
def printTopic(topic):
    print('\033[1m' + topic['topic'] + '\033[0m')
    print(topic['description'])
    print('\n')

def viewConcept(concept):
    MY_HTML_HEAD = 'Editor title'
    mdFile = concept['concept'] + '.md'
    # open concept file in editor
    web_edit.start(
        MarkdownDocument(infile=mdFile, outfile=mdFile),
        title=MY_HTML_HEAD)

@app.command()
def init():
    """
    Initialize a BPS directory.
    """
    # create BPS.data.json
    bpsconfig = {
        'topics': [],
        'concepts': [],
    }
    with open(BPSConfigFile, 'w') as f:
        json.dump(bpsconfig, f)


@app.command()
def add(type: str):
    """
    Add a topic or concept to the BPS directory.
    """
    bps = BPSclient()
    if type == 'topic':
        bps.addTopic()
    elif type == 'concept':
        bps.addConcept()
    else:
        print('invalid type')


@app.command()
def remove(type: str, name: str):
    """
    Remove a topic or concept from the BPS directory.
    """
    bps = BPSclient()
    if type == 'topic':
        topic = bps.getTopic(name)
        if topic:
            bps.removeTopic(topic)
        else:
            print('topic not found')
    elif type == 'concept':
        concept = bps.getConcept(name)
        if concept:
            bps.removeConcept(concept)
        else:
            print('concept not found')
    else:
        print('invalid type')


@app.command()
def edit(type: str, name: str, tag: str = None, maintainer: str = None, remove: bool = False):
    """
    Edit a topic or concept in the BPS directory.
    """
    bps = BPSclient()
    if type == 'concept':
        concept = bps.getConcept(name)
        if concept:
            bps.editConcept(concept, tag, maintainer, remove)
        else:
            print('concept not found')
    else:
        print('invalid type')


@app.command()
def list(type: str):
    """
    List all topics or concepts in the BPS directory.
    """
    bps = BPSclient()
    if type == 'topic':
        topics = bps.getTopics()
        for topic in topics:
            printTopic(topic)
    elif type == 'concept':
        concepts = bps.getConcepts()
        for concept in concepts:
            printConcept(concept)
    else:
        print('invalid type')


@app.command()
def search(query: str):
    """
    Search for a topic or concept in the BPS directory.
    """
    bps = BPSclient()
    concepts = bps.getConcepts()
    for concept in concepts:
        if query in concept['concept'] or query in concept['summary'] or query in concept['maintainers'] or query in \
                concept['tags']:
            printConcept(concept)


@app.command()
def view(concept: str):
    """
    View a concept in the BPS directory.
    """
    bps = BPSclient()
    concept = bps.getConcept(concept)
    if concept:
        printConcept(concept)
    else:
        print('concept not found')


@app.command()
def help():
    """
    View help for the BPS CLI.
    """
    print(app.get_help())


@app.command()
def version():
    """
    View the version of the BPS CLI.
    """
    print('BPS CLI version 0.1')


@app.command()
def editConcept(concept: str):
    """
    Edit a concept in the BPS directory.
    """
    bps = BPSclient()
    concept = bps.getConcept(concept)
    if concept:
        viewConcept(concept)
    else:
        print('concept not found')

def welcome():
    # print welcome message
    print(pyfiglet.figlet_format('BPS CLI', font='slant'))
    print('Welcome to the BPS CLI version 0.1')
    print('\n')
    print('Type "bps --help" to get started')
    print('\n')

if __name__ == "__main__":
    if len(sys.argv) == 1:
        welcome()
    else:
        app()