from enum import Enum
from pathlib import Path
import os
import shutil
import subprocess
from typing import List, Tuple

from network_traffic.traffic_collection.apk_processing import apk_builder
from network_traffic.traffic_collection.apk_processing import apk_download_utility
from gui import globals
from network_traffic.post_processing.process_pcaps import run as run_process_pcaps
from privacy_policy.network_to_policy_consistency.process_zipped_policies import run as run_process_zipped_policies
from privacy_policy.network_to_policy_consistency.make_plots import run as run_make_plots

class Command(Enum):
    # traffic collection
    INSTALL_ANTMONITOR = 0
    CLEAR_ANTMONITOR_DATA = 1
    GET_FRIDA_LIBS = 2
    ADB_CONNECT_TCP_IP = 3
    MOVE_UNITY_SOS = 4
    APK_BLACKLIST = 5
    APK_DOWNLOAD = 6
    # policheck
    SETUP_ANALYSIS = 7
    ANALYZE_DATA = 8
    CREATE_GRAPHS = 9
    POST_PROCESSING = 10
    # PP_GRAPHS = 11
    # frida/testing
    FRIDA_SELECT_APK = 11
    FRIDA_REINSTALL_APK = 12
    FRIDA_BYPASS = 13
    FRIDA_COLLECT = 14
    FRIDA_COLLECT_UNINSTALL = 15

    
class PathManager:

    NETWORK_TRAFFIC = Path("network_traffic")
    POST_PROCESSING = NETWORK_TRAFFIC / "post_processing"
    TRAFFIC_COLLECTION = NETWORK_TRAFFIC / "traffic_collection"
    APK_PROCESSING = TRAFFIC_COLLECTION / "apk_processing"
    CERT_VALIDATION_BYPASS = TRAFFIC_COLLECTION / "cert_validation_bypass"
    POSTPROC_GRAPHS = POST_PROCESSING / "figs_and_tables"

    PRIVACY_POLICY = Path("privacy_policy")
    NETWORK_TO_POLICY_CONSISTENCY = PRIVACY_POLICY / Path("network_to_policy_consistency")
    PRIPOL_GRAPHS = NETWORK_TO_POLICY_CONSISTENCY / Path("ext") / Path("plots")
    PURPOSE_EXTRACTION = PRIVACY_POLICY / Path("purpose_extraction")

    def __combine_outputs(self, *outputs: Tuple[str, str]):
        sum_stdout = ""
        sum_stderr = ""
        for stdout, stderr in list(outputs):
            sum_stdout += stdout + "\n"
            sum_stderr += stderr + "\n"
    
    def check_device_connection(self, tcpip_mode):
        stdout, stderr = self.exec(["adb devices"])
        lines = stdout.split("\n")
        device = lines[1]
        if len(lines) > 2:
            second_device = lines[2]
            if second_device != "":
                if not tcpip_mode:
                    tcp_device = device if "5555" in device else second_device
                    ip = tcp_device.split()[0]
                    self.exec(["adb disconnect", ip])
                    return not tcpip_mode
                else:
                    globals.redirect_print_func("disconnect from usb to use ip device")
                    return None
        if device == '':
            return None
        if "5555" in device:
            if "unauthorized" in device:
                return None
            return tcpip_mode # connected with tcpip mode
        else:
            return not tcpip_mode


    def run_command(self, cmd: Command, args: List[str] = []):
        device_connection = self.check_device_connection(self._tcpip_mode)
        if cmd not in self.allows_tcpip and self._tcpip_mode:
            # try to enter usb mode and quit if fails
            stdout, stderr = self.exec(["adb usb"])
            self._tcpip_mode = False
            if device_connection is None or device_connection is False:
                globals.redirect_print_func("couldn't run command because usb device not connected")
                return None
        elif cmd in self.allows_tcpip and self._tcpip_mode:
            # make sure we are connected
            if device_connection is None:
                if self._tcpip_ip is not None:
                    self.exec(["adb connect", self._tcpip_ip])
                    retry_connection = self.check_device_connection(self._tcpip_mode)
                    if retry_connection is not True:
                        globals.redirect_print_func("couldnt connect by ip")
                        return None
                else:
                    globals.redirect_print_func(["please connect the oculus by usb and then click 'Connect Oculus'"])
            elif device_connection is False:
                globals.redirect_print_func(["please click 'Connect Oculus'"])
        elif device_connection is None:
            globals.redirect_print_func("device is not connected")
            globals.redirect_print_func("please plug in the device and then accept the prompt")
            return None     
        # command handling
        if cmd == Command.INSTALL_ANTMONITOR:
            return self.exec(["adb", "install", *args])
        elif cmd == Command.CLEAR_ANTMONITOR_DATA:
            return self.exec(["adb", "shell", "'rm -rf /sdcard/anteater/*'"])
        elif cmd == Command.GET_FRIDA_LIBS:
            if not self.chdir_relative(PathManager.APK_PROCESSING):
                return None
            if (self._ovrseen_path / PathManager.APK_PROCESSING / "all_libs").exists():
                globals.redirect_print_func("cleaning old libs")
                shutil.rmtree("all_libs")
                lib_zips = filter(lambda file: file.startswith("lib-") and file.endswith(".zip") ,os.listdir())
                for lib in lib_zips:
                    Path(lib).unlink()
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
                    self._tcpip_ip = ip + ":5555"
                    self._tcpip_mode = True
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
            if Path("ext").exists():
                shutil.rmtree(Path("ext"))
            if Path("ext2").exists():
                shutil.rmtree(Path("ext2"))
            if Path("privacy_policies").exists():
                shutil.rmtree("privacy_policies")
            if Path("privacy_policies.zip").exists():
                self.exec(["unzip privacy_policies.zip -d ./"])
            os.makedirs("ext", exist_ok=True)
            self.exec(["tar xvf NlpFinalModel.tar.gz -C ext/"])
            os.makedirs("ext/data", exist_ok=True)
            shutil.copytree(Path("ontology"), Path("ext/data"), dirs_exist_ok=True)
            run_process_zipped_policies("privacy_policies", "ext/html_policies", args[0])
            shutil.copy2(self._ovrseen_path / PathManager.POST_PROCESSING / "PCAPs/all-merged-with-esld-engine-privacy-developer-party.csv", "./")
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
            globals.redirect_print_func("making plots")
            run_make_plots("ext/", "ext2/")
            globals.redirect_print_func(f"finished plots, check {PathManager.NETWORK_TO_POLICY_CONSISTENCY / 'ext/plots'}")
        elif cmd == Command.FRIDA_SELECT_APK:
            if len(args) != 1:
                return None
            if not self.chdir_relative(PathManager.APK_PROCESSING):
                return None
            # first run apk builder
            globals.redirect_print_func("installing apk if it doesnt exist")
            apk_file = args[0]
            frida_apk_path = "_" + apk_file
            pkg_name = self.get_package_name(frida_apk_path)
            if len(pkg_name) == 0:
                # then need to install it
                self.install_apk_to_oculus(frida_apk_path)
                pkg_name = self.get_package_name(frida_apk_path)
            else:
                globals.redirect_print_func("apk is already downloaded onto the oculus")
            with open(self._ovrseen_path / PathManager.CERT_VALIDATION_BYPASS / "current_apk", "w") as f:
                f.write(pkg_name)
            return pkg_name
        elif cmd == Command.FRIDA_REINSTALL_APK:
            if len(args) != 1:
                return None
            if not self.chdir_relative(PathManager.APK_PROCESSING):
                return None
            globals.redirect_print_func("reinstalling and rebuilding frida apk")
            apk_file = args[0]
            frida_apk_path = "_" + apk_file
            pkg_name = self.get_package_name(frida_apk_path)
            self.uninstall_package(pkg_name)
            self.install_apk_to_oculus(frida_apk_path)
        elif cmd == Command.FRIDA_BYPASS:
            if len(args) != 1:
                return None
            if not self.chdir_relative(PathManager.CERT_VALIDATION_BYPASS):
                return None
            if not Path("unity_so_files").exists():
                globals.redirect_print_func("make sure unity libraries are installed in the first tab")
                return None
            self.exec(["./bypass_all_ssl_pinnings.sh -l unity_so_files -a ../apk_processing/APKs/"])
        elif cmd == Command.FRIDA_COLLECT:
            if not self.chdir_relative(PathManager.CERT_VALIDATION_BYPASS):
                return None
            self.collect_frida_pcaps()
        elif cmd == Command.FRIDA_COLLECT_UNINSTALL:
            if not self.chdir_relative(PathManager.CERT_VALIDATION_BYPASS):
                return None
            self.collect_frida_pcaps(uninstall=True)
        elif cmd == Command.POST_PROCESSING:
            if not self.chdir_relative(PathManager.POST_PROCESSING):
                return None
            if Path("PCAPs").exists():
                # remove all csv files
                shutil.rmtree(Path("PCAPs"))
            shutil.copytree(self._ovrseen_path / PathManager.CERT_VALIDATION_BYPASS / "pcaps", "PCAPs")
            if Path("PCAPs/temp_output").exists():
                shutil.rmtree("PCAPs/temp_output")
            run_process_pcaps("PCAPs", ".")
        
        # elif cmd == Command.PP_GRAPHS:
        #     if not self.chdir_relative(PathManager.POST_PROCESSING / Path("figs_and_tables")):
        #         return None
        #     self.exec(["python3", "create_data_for_tables_and_figures.py", "--csv_file_path", "../all-merged-with-esld-engine-privacy-developer-party.csv", "--output_directory", "."])

        self.chdir_base()
    
    def collect_frida_pcaps(self, uninstall=False):
        destination = Path("pcaps")
        if not Path("current_apk").exists():
            globals.redirect_print_func("no apk is selected yet")
            return None
        pkg_name = None
        with open(Path("current_apk"), "r") as f:
            pkg_name = f.readline()
        if pkg_name is None:
            globals.redirect_print_func("no apk is selected yet")
            return None
        globals.redirect_print_func("===> Pulling captured PCAP files...")
        if not destination.exists():
            destination.mkdir()
        self.exec(["adb -d pull /sdcard/antmonitor"])
        globals.redirect_print_func(f"===> PCAP files are stored in {destination / pkg_name}...")
        pkg_destination = destination / pkg_name
        if pkg_destination.exists():
            shutil.rmtree(pkg_destination)
        shutil.move("antmonitor", pkg_destination)
        # delete pcap files on device
        self.exec(["adb -d shell 'rm -rf /sdcard/antmonitor/*'"])
        globals.redirect_print_func(f"===> Saving logcat output info into {pkg_destination}...")
        self.exec([f"adb -d logcat -d > {pkg_destination / 'logcat_output.log'}"])
        if uninstall:
            globals.redirect_print_func(f"===> Uninstalling {pkg_name}...")
            self.exec([f"adb -d uninstall {pkg_name}"])

    def create_frida_apk(self, apk_path):
        repackageApk = apk_builder.ApkBuilder(apk_path="APKs/" + apk_path, keystore_pw="password", inject_frida=True, downgrade_api=True, inject_internet_perm=True)
        repackageApk.run()

    def install_apk_to_oculus(self, apk_path: str):
        """Takes the frida apk, ie '_' + apk"""
        if not Path(apk_path).exists():
            self.create_frida_apk(apk_path.lstrip("_"))
        self.exec(["adb -d install", apk_path])
        # copy obb file
        pkg_name = self.get_package_name(apk_path)
        if ((Path("APKs/obb/") / pkg_name).exists()):
            self.exec(["adb -d push APKs/obb/" + pkg_name, "/sdcard/Android/obb/"])

    def get_package_name(self, apk_path):
        stdout, stderr = self.exec(["aapt dump badging", apk_path])
        start_ind = 15 # skip package: name =
        end_ind = stdout.find("' versionCode")
        pkg_name = stdout[start_ind:end_ind]
        return pkg_name
    
    def has_package(self, apk):
        stdout, stderr = self.exec(["adb shell pm list packages", apk])
        return len(stdout) > 0
    
    def uninstall_package(self, apk: str):
        if self.has_package(apk):
            self.exec(["adb -d uninstall", apk])

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
        self._tcpip_mode = False
        self.allows_tcpip = [Command.FRIDA_BYPASS]
        self._tcpip_ip = None

    @property
    def ovrseen_path(self):
        return self._ovrseen_path.absolute()

    def close(self):
        with open("ovrseen_directory.txt", "w") as f:
            if self._ovrseen_path is not None:
                f.write(str(self._ovrseen_path.absolute()))
