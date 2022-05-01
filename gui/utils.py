from enum import Enum
from pathlib import Path
import os
import subprocess
from typing import List, Tuple

redirect_print_func = None

class Command(Enum):
    # traffic collection
    INSTALL_ANTMONITOR = 0
    CLEAR_ANTMONITOR_DATA = 1
    GET_FRIDA_LIBS = 2
    ADB_CONNECT_TCP_IP = 3
    MOVE_UNITY_SOS = 4
    APK_BLACKLIST = 5
    APK_DOWNLOAD = 6

class PathManager:

    NETWORK_TRAFFIC = Path("network_traffic")
    POST_PROCESSING = NETWORK_TRAFFIC / "post-processing"
    TRAFFIC_COLLECTION = NETWORK_TRAFFIC / "traffic_collection"
    APK_PROCESSING = TRAFFIC_COLLECTION / "apk_processing"
    CERT_VALIDATION_BYPASS = TRAFFIC_COLLECTION / "cert_validation_bypass"

    PRIVACY_POLICY = Path("privacy_policy")
    NETWORK_TO_POLICY_CONSISTENCY = PRIVACY_POLICY / Path("network-to-privacy_consistency")
    GRAPHS = NETWORK_TO_POLICY_CONSISTENCY / Path("ext") / Path("plots")
    PURPOSE_EXTRACTION = PRIVACY_POLICY / Path("purpose_extraction")

    def __combine_outputs(self, *outputs: Tuple[str, str]):
        sum_stdout = ""
        sum_stderr = ""
        for stdout, stderr in list(outputs):
            sum_stdout += stdout + "\n"
            sum_stderr += stderr + "\n"

    def run_command(self, cmd: Command, args: List[str] = []):
        if cmd == Command.INSTALL_ANTMONITOR:
            return self.exec(["adb", "install", *args])
        elif cmd == Command.CLEAR_ANTMONITOR_DATA:
            return self.exec(["adb", "shell"])
        elif cmd == Command.GET_FRIDA_LIBS:
            if not self.chdir_relative(PathManager.APK_PROCESSING):
                return None
            if (self._ovrseen_path / PathManager.APK_PROCESSING / "all_libs").exists():
                redirect_print_func("cleaning old libs")
                self.exec(["rm -rf all_libs"])
            if (self._ovrseen_path / PathManager.APK_PROCESSING / "appmon.keystore").exists():
                redirect_print_func("cleaning old keystore")
                self.exec(["rm appmon.keystore"])
            output_1 = self.exec(["./getlibs.sh"])
            output_2 = self.exec(["keytool", "-genkey", "-v", "-keystore", "appmon.keystore", "-alias", "mykeyaliasname", "-keyalg", "RSA", "-keysize", "2048", "-validity", "10000"], inputs=["password", "password", "a", "a", "a", "a", "a", "a", "y"])
            return self.__combine_outputs(output_1, output_2)
        elif cmd == Command.ADB_CONNECT_TCP_IP:
            stdout, stderr = self.exec(["adb shell", "'ip addr show'"])
            if len(stdout) > 0:
                wlan = stdout.find("wlan0")
                if wlan != -1:
                    inet = stdout.find("inet", wlan)
                    slash = stdout.find("/", inet)
                    ip = stdout[inet + 5:slash]
                    self.exec(["adb tcpip 5555"])
                    self.exec(["adb connect", ip + ":5555"])
            else:
                redirect_print_func("connection couldn't be established")
        elif cmd == Command.MOVE_UNITY_SOS:
            if not self.chdir_relative(PathManager.CERT_VALIDATION_BYPASS):
                return None
            stdout, stderr = self.exec(["mv", args[0], "unity_so_files"])
            redirect_print_func("moved unity_so_files into: ", self.sptb(PathManager.CERT_VALIDATION_BYPASS / "unity_so_files"), "\nmove other unity libs in as needed.")
        elif cmd == Command.APK_BLACKLIST:
            if not self.chdir_relative(PathManager.APK_PROCESSING):
                return None
            self.exec(["sudo adb start-server"])
            redirect_print_func("PLEASE confirm the prompt on your oculus as well")

        self.chdir_base()

    def sptb(self, path: Path):
        if self._ovrseen_path is not None:
            return str((self._ovrseen_path / path).absolute())

    def exec(self, args: List[str], inputs: List[str] = None) -> Tuple[str, str]:
        redirect_print_func("running command: ", " ".join(args))
        if inputs is None:
            result = subprocess.run(" ".join(args), shell=True, check=False, capture_output=True)
        else:
            result = subprocess.run(" ".join(args), shell=True, check=False, input="\n".join(inputs) + "\n", text=True, capture_output=True)
        stdout = result.stdout if type(result.stdout) == str else result.stdout.decode()
        stderr = result.stderr if type(result.stderr) == str else result.stderr.decode()
        if len(stdout) > 0:
            redirect_print_func("stdout: ")
            redirect_print_func(stdout)
        if len(stderr) > 0:
            redirect_print_func("stderr: ")
            redirect_print_func(stderr)
        return stdout, stderr

    def chdir_relative(self, to: Path):
        if self._ovrseen_path is not None:
            os.chdir(self._ovrseen_path / to)
            return True
        else:
            redirect_print_func("WARNING: Set the ovrseen directory in the first tab")
            return False

    def chdir_base(self):
        if self._ovrseen_path is not None:
            os.chdir(self._ovrseen_path)
        else:
            redirect_print_func("WARNING: Set the ovrseen directory in the first tab")

    def __init__(self) -> None:
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
