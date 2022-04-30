from enum import Enum
from pathlib import Path
import os
import subprocess
from typing import List, Tuple

class Command(Enum):
    # traffic collection
    INSTALL_ANTMONITOR = 0
    CLEAR_ANTMONITOR_DATA = 1
    GET_FRIDA_LIBS = 2
    ADB_CONNECT_TCP_IP = 3

class PathManager:

    NETWORK_TRAFFIC = Path("network_traffic")
    POST_PROCESSING = NETWORK_TRAFFIC / "post-processing"
    TRAFFIC_COLLECTION = NETWORK_TRAFFIC / "traffic_collection"
    APK_PROCESSING = TRAFFIC_COLLECTION / "apk_processing"
    CERT_VALIDATION_BYPASS = TRAFFIC_COLLECTION / "cert_validation_bypass"

    PRIVACY_POLICY = Path("privacy_policy")
    NETWORK_TO_POLICY_CONSISTENCY = Path("network-to-privacy_consistency")
    PURPOSE_EXTRACTION = Path("purpose_extraction")

    def __combine_outputs(*outputs: Tuple[str, str]):
        sum_stdout = ""
        sum_stderr = ""
        for stdout, stderr in list(outputs):
            sum_stdout += stdout + "\n"
            sum_stderr += stderr + "\n"

    def run_command(self, cmd: Command, args: List[str]):
        if cmd == Command.INSTALL_ANTMONITOR:
            return self.exec(["adb", "install", *args])
        elif cmd == Command.CLEAR_ANTMONITOR_DATA:
            return self.exec(["adb", "shell", '"rm -rf /sdcard/antmonitor/*"'])
        elif cmd == Command.GET_FRIDA_LIBS:
            self.chdir_relative(PathManager.APK_PROCESSING)
            output_1 = self.exec(["./getlibs.sh"])
            output_2 = self.exec(["keytool", "-genkey", "-v", "-keystore", "appmon.keystore", "-alias", "mykeyaliasname", "-keyalg", "RSA", "-keysize", "2048", "-validity", "10000"])
            return self.__combine_outputs(output_1, output_2)
        elif cmd == Command.ADB_CONNECT_TCP_IP:
            pass
    
    def exec(args: List[str], inputs: List[str] = None) -> Tuple[str, str]:
        if input is None:
            result = subprocess.run(args, shell=True, check=False, capture_output=True)
        else:
            result = subprocess.run(args, shell=True, check=False, input="\n".join(input) + "\n", text=True, capture_output=True)
        return result.stdout.decode(), result.stderr.decode()

    def chdir_relative(self, to: Path):
        if self._ovrseen_path is not None:
            os.chdir(self._ovrseen_path / to)
    
    def chdir_base(self):
        if self._ovrseen_path is not None:
            os.chdir(self._ovrseen_path)

    def __init__(self) -> None:
        with open("ovrseen_directory.txt", "r") as f:
            tmp = Path(f.readline())
            if tmp.exists() and tmp.is_dir():
                self._ovrseen_path = tmp
            else:
                self._ovrseen_path = None
    
    @property
    def ovrseen_path(self):
        if self._ovrseen_path is None:
            return Path.cwd().absolute()
        else:
            return self._ovrseen_path.absolute()

    @ovrseen_path.setter
    def ovrseen_path(self, value):
        self._ovrseen_path = Path(value)
    
    def close(self):
        with open("ovrseen_directory.txt", "w") as f:
            if self._ovrseen_path is not None:
                f.write(str(self._ovrseen_path.absolute()))
    