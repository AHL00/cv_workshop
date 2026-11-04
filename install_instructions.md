# CV Workshop 2026 Set-up Instructions
This guide explains how to install the small set of packages and set things
up for the CV workshop. **If you have any questions, you can text @kha0024 on Telegram.**

We will use **Visual Studio Code (VS Code)** throughout this guide. Install
VS Code first from <https://code.visualstudio.com/>. These instructions use
the VS Code editor and its built-in terminal.

This guide does **not** install the packages used for actual espdet-pico training or quantization.

## What you need

Before starting, make sure you have:

- A Windows, macOS, or Linux computer
- A working USB or built-in camera
- The workshop files sent to you

Python **3.11, 3.12, 3.13 or 3.14** is recommended. Newer versions have not been tested with this workshop.

## 1. Install Python

If you already have Python 3.11, 3.12, 3.13 or 3.14 installed, you can skip this step. To check, open a terminal and run `python3 --version` (macOS/Linux) or `py --version` (Windows).

### Windows

1. Open a web browser and go to <https://www.python.org/downloads/>.
2. Download Python **3.11, 3.12, 3.13, or 3.14**.
3. Run the downloaded installer.
4. On the first installer screen, check **Add python.exe to PATH**.
5. Click **Install Now**.
6. When the installation finishes, close the installer.

### macOS

Go to <https://www.python.org/downloads/> and download Python **3.11, 3.12, 3.13 or 3.14**.

### Linux

Use your Linux distribution's package manager to install Python 3 and its virtual-environment package. For Ubuntu, for example:

```bash
sudo apt update
sudo apt install python3 python3-venv
```

## 2. Open the workshop folder in VS Code

1. Start VS Code.
2. Select **File > Open Folder**.
3. Find and select the workshop folder.
4. Click **Select Folder** on Windows, or **Open** on macOS and Linux.
5. Look at the **Explorer** panel on the left.

You should see files such as `inference.py`, `train_simple.py`, `best.pt`, the
`dataset` folder, and the `nn` folder.

If VS Code asks whether you trust the folder, choose **Yes, I trust the
authors** because this is your workshop folder. If you see restricted mode on top, click manage and trust.

## 3. Install the VS Code Python extension

1. Click the **Extensions** icon on the left side of VS Code. It looks like
   four small squares.
2. Search for **Python**.
3. Install the extension named **Python** published by **Microsoft**.

This extension helps VS Code find the correct Python installation and virtual
environment.

## 4. Open the VS Code terminal

From the top menu, select **Terminal > New Terminal**.

A terminal panel opens at the bottom of VS Code. It should already be
connected to the workshop folder. To check, run:

### Windows

```powershell
dir
```

### macOS or Linux

```bash
ls
```

You should see `inference.py` in the output. If you do not, go
back to **File > Open Folder** and open the correct workshop folder.

## 5. Create a private Python environment

A virtual environment keeps this project's packages separate from other
Python projects.

In the VS Code terminal, run the command for your computer.

### Windows

```powershell
py -3 -m venv .venv
```

If you have several Python versions installed, `py -0` lists them. To pick a
specific one, replace `-3` with the version, for example `py -3.12 -m venv .venv`.

### macOS or Linux

```bash
python3 -m venv .venv
```

## 6. Select the Python environment in VS Code

1. Press **Ctrl+Shift+P** on Windows/Linux, or **Cmd+Shift+P** on macOS.
2. Type **Python: Select Interpreter**.
3. Select the interpreter inside `.venv`.

On Windows it is usually:

```text
.venv\Scripts\python.exe
```

On macOS/Linux it is usually:

```text
.venv/bin/python
```

The selected environment should appear in the bottom-right corner of VS
Code.

## 7. Turn on the environment in the terminal

VS Code often activates the environment automatically when you open a new
terminal. If the terminal prompt does not begin with `(.venv)`, activate it
manually or just open a new vscode terminal instance.

### Windows PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell says that running scripts is disabled, run this once and then
repeat the activation command:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

### Windows Command Prompt

```bat
.venv\Scripts\activate.bat
```

### macOS or Linux

```bash
source .venv/bin/activate
```

When activation works, the terminal usually shows `(.venv)` at the beginning
of the command line.

### Check your Python version

With `(.venv)` active, run:

```text
python --version
```

You should see Python **3.11, 3.12, 3.13 or 3.14**. If not, it might still work, but not guaranteed.

## 8. Install the required packages

First update the package installer:

```text
python -m pip install --upgrade pip
```

### 8a. Install PyTorch

Choose **one** of the following PyTorch installations.

#### Option A: CPU only (recommended)

This is the simplest option. It works on computers without an NVIDIA graphics
card and is the fastest option to install:

```text
python -m pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

#### Option B: NVIDIA GPU with CUDA

Choose this option only if your computer has an NVIDIA graphics card and
working NVIDIA drivers. This makes PyTorch use your GPU for training and
inference.

The CUDA version uses about **1 GB of additional storage** and takes longer to
download and install than the CPU-only version. Do not install both options in
the same environment. If you already installed the CPU version, create a new
environment or uninstall it before using the CUDA version.

For a CUDA-enabled installation, run:

```text
python -m pip install torch torchvision --index-url https://download.pytorch.org/whl/cu126
```

This above command should support **nvidia's 20 series and above**. If your GPU is older, either find the last compatible version or just install the CPU version.

If this command does not work with your NVIDIA drivers, use the command shown
by the official PyTorch installer selector at <https://pytorch.org/get-started/locally/>.

### 8b. Install OpenCV and Ultralytics (everyone)

Whichever PyTorch option you chose, now run:

```text
python -m pip install opencv-python ultralytics
```

The installation can take several minutes. Leave the terminal open until it
finishes without an error.

## 9. Check the installation

With `(.venv)` still active, run:

```text
python -c "import cv2, torch, ultralytics; print('Installation works'); print('OpenCV:', cv2.__version__); print('PyTorch:', torch.__version__); print('Ultralytics:', ultralytics.__version__); print('CPU only:', not torch.cuda.is_available())"
```

You should see `Installation works`. For the CPU option, the final line should
say `CPU only: True`. For the CUDA option, it should say `CPU only: False`.

If you chose the CUDA option but it says `CPU only: True`, update your NVIDIA
drivers and try again, or switch to the CPU option (Option A) in a fresh environment.

## 10. You're done installing
👍