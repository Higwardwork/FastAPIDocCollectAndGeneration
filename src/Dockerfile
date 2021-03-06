FROM mcr.microsoft.com/windows/servercore:1809 as python
ENV PYTHON_VERSION 3.7.4
ENV PYTHON_RELEASE 3.7.4

# if this is called "PIP_VERSION", pip explodes with "ValueError: invalid truth value '<VERSION>'"
ENV PYTHON_PIP_VERSION 20.0.2

# https://github.com/pypa/get-pip
ENV PYTHON_GET_PIP_URL https://github.com/pypa/get-pip/raw/d59197a3c169cef378a22428a3fa99d33e080a5d/get-pip.py

WORKDIR C:\\Temp
SHELL ["powershell", "-Command", "$ErrorActionPreference = 'Stop'; $ProgressPreference = 'Continue'; $verbosePreference='Continue';"]

RUN [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]::Tls12; \
    Invoke-WebRequest -UseBasicParsing -Uri "https://www.python.org/ftp/python/$env:PYTHON_RELEASE/python-$env:PYTHON_VERSION-embed-amd64.zip" -Out 'Python.zip'; \
    Expand-Archive -Path "Python.zip"; \
    Invoke-WebRequest -UseBasicParsing -Uri "$env:PYTHON_GET_PIP_URL" -OutFile 'Python\get-pip.py';

RUN [String]::Format('@set PYTHON_PIP_VERSION={0}', $env:PYTHON_PIP_VERSION) | Out-File -FilePath 'Python\pipver.cmd' -Encoding ASCII; \
    $FileVer = [System.Version]::Parse([System.Diagnostics.FileVersionInfo]::GetVersionInfo('Python\python.exe').ProductVersion); \
    $Postfix = $FileVer.Major.ToString() + $FileVer.Minor.ToString(); \
    Remove-Item -Path "Python\python$Postfix._pth"; \
    Expand-Archive -Path "Python\python$Postfix.zip" -Destination "Python\Lib"; \
    Remove-Item -Path "Python\python$Postfix.zip"; \
    New-Item -Type Directory -Path "Python\DLLs";

FROM mcr.microsoft.com/windows/nanoserver:1809 as nano_python
COPY --from=python C:\\Temp\\Python C:\\Python
USER ContainerAdministrator

ENV PYTHONPATH C:\\Python;C:\\Python\\Scripts;C:\\Python\\DLLs;C:\\Python\\Lib;C:\\Python\\Lib\\plat-win;C:\\Python\\Lib\\site-packages
RUN setx.exe /m PATH %PATH%;%PYTHONPATH% && \
    setx.exe /m PYTHONPATH %PYTHONPATH% && \
    setx.exe /m PIP_CACHE_DIR C:\Users\ContainerUser\AppData\Local\pip\Cache && \
    reg.exe ADD HKLM\SYSTEM\CurrentControlSet\Control\FileSystem /v LongPathsEnabled /t REG_DWORD /d 1 /f

RUN assoc .py=Python.File && \
    assoc .pyc=Python.CompiledFile && \
    assoc .pyd=Python.Extension && \
    assoc .pyo=Python.CompiledFile && \
    assoc .pyw=Python.NoConFile && \
    assoc .pyz=Python.ArchiveFile && \
    assoc .pyzw=Python.NoConArchiveFile && \
    ftype Python.ArchiveFile="C:\Python\python.exe" "%1" %* && \
    ftype Python.CompiledFile="C:\Python\python.exe" "%1" %* && \
    ftype Python.File="C:\Python\python.exe" "%1" %* && \
    ftype Python.NoConArchiveFile="C:\Python\pythonw.exe" "%1" %* && \
    ftype Python.NoConFile="C:\Python\pythonw.exe" "%1" %*

RUN call C:\Python\pipver.cmd && \
    %COMSPEC% /s /c "echo Installing pip==%PYTHON_PIP_VERSION% ..." && \
    %COMSPEC% /s /c "C:\Python\python.exe C:\Python\get-pip.py --disable-pip-version-check --no-cache-dir pip==%PYTHON_PIP_VERSION%" && \
    echo Removing ... && \
    del /f /q C:\Python\get-pip.py C:\Python\pipver.cmd && \
    echo Verifying install ... && \
    echo   python --version && \
    python --version && \
    echo Verifying pip install ... && \
    echo   pip --version && \
    pip --version && \
    echo Complete.

WORKDIR C:\\FastAPI

RUN pip install --upgrade pip

COPY requirements.txt ./requirements.txt

# `;` over `&&` becose windows
RUN pip install --no-cache-dir -r requirements.txt

USER ContainerUser
VOLUME C:/Template_Data
COPY . .
