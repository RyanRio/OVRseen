from enum import Enum
from pathlib import Path
import os
import subprocess
from typing import List, Tuple

from network_traffic.traffic_collection.apk_processing import apk_builder
from network_traffic.traffic_collection.apk_processing import apk_download_utility
from gui import globals

class Command(Enum):
    # traffic collection
    INSTALL_ANTMONITOR = 0
    CLEAR_ANTMONITOR_DATA = 1
    GET_FRIDA_LIBS = 2
    ADB_CONNECT_TCP_IP = 3
    MOVE_UNITY_SOS = 4
    APK_BLACKLIST = 5
    APK_DOWNLOAD = 6
    SETUP_ANALYSIS = 7
    ANALYZE_DATA = 8
    CREATE_GRAPHS = 9
    POST_PROCESSING = 10
    # PP_GRAPHS = 11

class PathManager:

    NETWORK_TRAFFIC = Path("network_traffic")
    POST_PROCESSING = NETWORK_TRAFFIC / "post-processing"
    TRAFFIC_COLLECTION = NETWORK_TRAFFIC / "traffic_collection"
    APK_PROCESSING = TRAFFIC_COLLECTION / "apk_processing"
    CERT_VALIDATION_BYPASS = TRAFFIC_COLLECTION / "cert_validation_bypass"
    POSTPROC_GRAPHS = POST_PROCESSING / "figs_and_tables"

    PRIVACY_POLICY = Path("privacy_policy")
    NETWORK_TO_POLICY_CONSISTENCY = PRIVACY_POLICY / Path("network_to_privacy_consistency")
    PRIPOL_GRAPHS = NETWORK_TO_POLICY_CONSISTENCY / Path("ext") / Path("plots")
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
            return self.exec(["adb", "shell", "'rm -rf /sdcard/anteater/*'"])
        elif cmd == Command.GET_FRIDA_LIBS:
            if not self.chdir_relative(PathManager.APK_PROCESSING):
                return None
            if (self._ovrseen_path / PathManager.APK_PROCESSING / "all_libs").exists():
                globals.redirect_print_func("cleaning old libs")
                self.exec(["rm -rf all_libs"])
            if (self._ovrseen_path / PathManager.APK_PROCESSING / "appmon.keystore").exists():
                globals.redirect_print_func("cleaning old keystore")
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
                globals.redirect_print_func("connection couldn't be established")
        elif cmd == Command.MOVE_UNITY_SOS:
            if not self.chdir_relative(PathManager.CERT_VALIDATION_BYPASS):
                return None
            stdout, stderr = self.exec(["mv", args[0], "unity_so_files"])
            globals.redirect_print_func("moved unity_so_files into: ", self.sptb(PathManager.CERT_VALIDATION_BYPASS / "unity_so_files"), "\nmove other unity libs in as needed.")
        elif cmd == Command.APK_BLACKLIST:
            if not self.chdir_relative(PathManager.APK_PROCESSING):
                return None
            self.exec(["sudo adb start-server"])
            globals.redirect_print_func("PLEASE confirm the prompt on your oculus as well")
            apk_download_utility.run("InstalledAPKs", "APKs")
        elif cmd == Command.APK_DOWNLOAD:
            if not self.chdir_relative(PathManager.APK_PROCESSING):
                return None
            globals.redirect_print_func("Installing apks that have been installed since creating the blacklist")
            apk_download_utility.run("InstalledAPKs", "APKs")
        elif cmd == Command.SETUP_ANALYSIS:
            if not self.chdir_relative(PathManager.NETWORK_TO_POLICY_CONSISTENCY):
                return None
            os.makedirs("ext", exist_ok=True)
            os.makedirs("ext/data", exist_ok=True)
            self.exec(["cp", "ontology/*.{gml,yml}", "ext/data/"])
            self.exec(["python3", "process_zipped_policies.py", "privacy_policies", "ext/html_policies"])
            self.exec(["cp", "../../network_traffic/post-processing/all-merged-with-esld-engine-privacy-developer-party.csv", "."])
            self.exec(["python3", "preprocess_policheck_flows.py", "all-merged-with-esld-engine-privacy-developer-party.csv", "ext/data/policheck_flows.csv"])
        elif cmd == Command.ANALYZE_DATA:
            if not self.chdir_relative(PathManager.NETWORK_TO_POLICY_CONSISTENCY):
                return None
            self.exec(["python3", "Preprocessor.py", "-i", "ext/html_policies", "-o", "ext/plaintext_policies"])
            self.exec(["awk", "-F,", "'NR", ">", "1", "{", "print", "$1", "}'", "ext/data/policheck_flows.csv", "|", "sort", "-u", "|", "xargs", "-i", "touch", "ext/plaintext_policies/{}.txt"])
            self.exec(["python3", "PatternExtractionNotebook.py", "ext/"])
            self.exec(["python3", "CollectFirstPartyNames.py", "ext/"])
            self.exec(["cp", "-r", "ext/", "ext2/"])
            self.exec(["python3", "detect_third_party_policies.py", "ext/"])
            self.exec(["python3", "ConsistencyAnalysis.py", "ext/"])
            self.exec(["python3", "RemoveSameSentenceContradictions.py", "ext/"])
            self.exec(["python3", "DisclosureClassification.py", "ext/"])
            self.exec(["python3", "detect_third_party_policies.py", "ext2/", "append"])
            self.exec(["python3", "ConsistencyAnalysis.py", "ext2/"])
            self.exec(["python3", "RemoveSameSentenceContradictions.py", "ext2/"])
            self.exec(["python3", "DisclosureClassification.py", "ext2/"])
        elif cmd == Command.CREATE_GRAPHS:
            if not self.chdir_relative(PathManager.NETWORK_TO_POLICY_CONSISTENCY):
                return None
            self.exec(["python3", "make_plots.py", "ext/", "ext2/"])
        elif cmd == Command.POST_PROCESSING:
            if not self.chdir_relative(PathManager.POST_PROCESSING):
                return None
            self.exec(["rm", "-r", "PCAPs/*.csv;", "rm", "-r", "PCAPs/temp_output"])
            self.exec(["python3", "process_pcaps.py", "PCAPs", "."])
        # elif cmd == Command.PP_GRAPHS:
        #     if not self.chdir_relative(PathManager.POST_PROCESSING / Path("figs_and_tables")):
        #         return None
        #     self.exec(["python3", "create_data_for_tables_and_figures.py", "--csv_file_path", "../all-merged-with-esld-engine-privacy-developer-party.csv", "--output_directory", "."])

        self.chdir_base()

    def sptb(self, path: Path):
        if self._ovrseen_path is not None:
            return str((self._ovrseen_path / path).absolute())

    def exec(self, args: List[str], inputs: List[str] = None) -> Tuple[str, str]:
        if not self.has_sudoed and "sudo" in " ".join(args):
            # execute a harmless sudo to provide password
            result = subprocess.run("sudo -S echo 'setting up sudo'", shell=True, check=False, capture_output=False, input="ovrseen\n", text=True)
            self.has_sudoed = True
        globals.redirect_print_func("running command: ", " ".join(args))
        if inputs is None:
            result = subprocess.run(" ".join(args), shell=True, check=False, capture_output=True)
        else:
            result = subprocess.run(" ".join(args), shell=True, check=False, input="\n".join(inputs) + "\n", text=True, capture_output=True)
        stdout = result.stdout if type(result.stdout) == str else result.stdout.decode()
        stderr = result.stderr if type(result.stderr) == str else result.stderr.decode()
        if len(stdout) > 0:
            globals.redirect_print_func("stdout: ")
            globals.redirect_print_func(stdout)
        if len(stderr) > 0:
            globals.redirect_print_func("stderr: ")
            globals.redirect_print_func(stderr)
        return stdout, stderr

    def chdir_relative(self, to: Path):
        if self._ovrseen_path is not None:
            os.chdir(self._ovrseen_path / to)
            return True
        else:
            globals.redirect_print_func("WARNING: Set the ovrseen directory in the first tab")
            return False

    def chdir_base(self):
        if self._ovrseen_path is not None:
            os.chdir(self._ovrseen_path)
        else:
            globals.redirect_print_func("WARNING: Set the ovrseen directory in the first tab")

    def __init__(self) -> None:
        self._ovrseen_path = Path(os.path.dirname(__file__)).parent
        self.has_sudoed = False

    @property
    def ovrseen_path(self):
        return self._ovrseen_path.absolute()

    def close(self):
        with open("ovrseen_directory.txt", "w") as f:
            if self._ovrseen_path is not None:
                f.write(str(self._ovrseen_path.absolute()))
