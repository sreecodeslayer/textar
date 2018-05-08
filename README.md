# textar
A simple textar archiver CLI

### Installation

```bash
pip install git+https://github.com/sreecodeslayer/textar.git
```

or build from source after cloning

```bash
git clone https://github.com/sreecodeslayer/textar.git
cd textar
python setup.py install
```

### Usage
1. Archive

```bash
textar <out_file> <input_file> [... <input_file>]
```

2. List contents in an archive

```bash
textar -l <txr_file>
```

3. Extract to current working directory

```bash
textar -x <txr_file>
```