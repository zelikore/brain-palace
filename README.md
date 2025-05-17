# Brain Palace

Brain Palace is a knowledge base organized with the **Brain Palace System (BPS)**. It stores notes about a wide range of topics and provides a command-line interface to help manage them.

## Repository overview

- **BPS-root/** – Markdown files for each concept and `BPS.data.json` describing all topics and concepts.
- **BPS-client/** – Python sources for the `bps` CLI.
- **ideas/**, **learn/** and **teach/** – Additional folders for notes, learning material and teaching resources.

## Installing and running the CLI

1. Create a virtual environment and install dependencies:

```bash
pip install -r BPS-client/src/requirement.txt
```

2. Navigate to a directory you wish to manage with BPS and initialize it:

```bash
python BPS-client/src/core.py init
```

   This command creates `BPS.data.json`, which stores metadata about topics and concepts.

3. Use the CLI to add topics or concepts:

```bash
python BPS-client/src/core.py add topic
python BPS-client/src/core.py add concept
```

   You will be prompted for details such as maintainers, summary, and tags.

4. Display existing entries, search, or view a concept:

```bash
python BPS-client/src/core.py list topic
python BPS-client/src/core.py list concept
python BPS-client/src/core.py search "keyword"
python BPS-client/src/core.py view "ConceptName"
```

5. Edit a concept file with your text editor:

```bash
python BPS-client/src/core.py editConcept "ConceptName"
```

The CLI keeps `BPS.data.json` in sync with your concept markdown files.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
