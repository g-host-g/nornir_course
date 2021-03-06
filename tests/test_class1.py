import subprocess
from nornir import InitNornir
import nornir

NORNIR_LOGGING = {"enabled": False}


def gen_inventory_dict(base_path):
    """Dynamically create an inventory dictionary using exercise path."""
    # BASE_PATH = "../class1/exercises/exercise1/"
    NORNIR_HOSTS = f"{base_path}/hosts.yaml"
    NORNIR_GROUPS = f"{base_path}/groups.yaml"
    NORNIR_DEFAULTS = f"{base_path}/defaults.yaml"
    NORNIR_INVENTORY = {
        "plugin": "nornir.plugins.inventory.simple.SimpleInventory",
        "options": {
            "host_file": NORNIR_HOSTS,
            "group_file": NORNIR_GROUPS,
            "defaults_file": NORNIR_DEFAULTS,
        },
    }
    return NORNIR_INVENTORY


def subprocess_runner(cmd_list, exercise_dir):
    with subprocess.Popen(
        cmd_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=exercise_dir
    ) as proc:
        std_out, std_err = proc.communicate()
    return (std_out.decode(), std_err.decode(), proc.returncode)


def test_class1_ex1():
    base_path = "../class1/exercises/exercise1/"
    nornir_inventory = gen_inventory_dict(base_path)
    nr = InitNornir(inventory=nornir_inventory, logging=NORNIR_LOGGING)
    assert isinstance(nr, nornir.core.Nornir)
    assert isinstance(nr.inventory.hosts, nornir.core.inventory.Hosts)
    assert isinstance(nr.inventory.hosts["my_host"], nornir.core.inventory.Host)
    assert nr.inventory.hosts["my_host"].hostname == "localhost"


def test_class1_ex2():
    base_path = "../class1/exercises/exercise2/"
    cmd_list = ["python", "exercise2.py"]

    nornir_inventory = gen_inventory_dict(base_path)
    nr = InitNornir(inventory=nornir_inventory, logging=NORNIR_LOGGING)
    assert len(nr.inventory.hosts) == 2
    for host_name, host_obj in nr.inventory.hosts.items():
        assert host_obj.hostname is not None
        assert len(host_obj.groups) == 1
        assert host_obj.groups[0] == "ios"
        assert host_obj.platform == "cisco_ios"
        assert host_obj.username == "pyclass"
        assert host_obj.password == "cisco123"
        assert host_obj.port == 22

    my_group = nr.inventory.groups["ios"]
    assert my_group.hostname is None
    assert my_group.platform == "cisco_ios"
    assert my_group.username == "pyclass"
    assert my_group.password == "cisco123"
    assert my_group.port == 22

    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert "cisco3" in std_out
    assert "cisco_ios" in std_out
    assert std_err == ""


def test_class1_ex3():
    base_path = "../class1/exercises/exercise3/"
    cmd_list = ["python", "exercise3.py"]

    nornir_inventory = gen_inventory_dict(base_path)
    nr = InitNornir(inventory=nornir_inventory, logging=NORNIR_LOGGING)
    assert len(nr.inventory.hosts) == 2
    for host_name, host_obj in nr.inventory.hosts.items():
        assert host_obj.hostname is not None
        assert len(host_obj.groups) == 1
        assert host_obj.groups[0] == "ios"
        assert host_obj.platform == "cisco_ios"
        assert host_obj.username == "pyclass"
        assert host_obj.password == "cisco123"
        assert host_obj.port == 22

    my_group = nr.inventory.groups["ios"]
    assert my_group.hostname is None
    assert my_group.platform == "cisco_ios"
    assert my_group.port == 22

    defaults = nr.inventory.defaults
    assert defaults.username == "pyclass"
    assert defaults.password == "cisco123"

    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert "cisco3" in std_out
    assert "cisco_ios" in std_out
    assert std_err == ""


def test_class1_ex4():
    base_path = "../class1/exercises/exercise4/"
    cmd_list = ["python", "exercise4.py"]

    nornir_inventory = gen_inventory_dict(base_path)
    nr = InitNornir(inventory=nornir_inventory, logging=NORNIR_LOGGING)
    assert len(nr.inventory.hosts) == 2
    for host_name, host_obj in nr.inventory.hosts.items():
        assert host_obj.hostname is not None
        assert len(host_obj.groups) == 1
        assert host_obj.groups[0] == "ios"
        assert host_obj.platform == "cisco_ios"
        assert host_obj.username == "pyclass"
        assert host_obj.password == "cisco123"
        assert host_obj.port == 22

    my_group = nr.inventory.groups["ios"]
    assert my_group.hostname is None
    assert my_group.platform == "cisco_ios"
    assert my_group.port == 22

    defaults = nr.inventory.defaults
    assert defaults.username == "pyclass"
    assert defaults.password == "cisco123"

    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert "cisco3.lasthop.io" in std_out
    assert "cisco4.lasthop.io" in std_out
    assert "These aren't the droids you're looking for" in std_out
    assert std_err == ""


def test_class1_ex5():
    base_path = "../class1/exercises/exercise5/"
    cmd_list = ["python", "exercise5.py"]

    nornir_inventory = gen_inventory_dict(base_path)
    nr = InitNornir(inventory=nornir_inventory, logging=NORNIR_LOGGING)

    assert len(nr.inventory.hosts) == 2
    for host_name, host_obj in nr.inventory.hosts.items():
        assert host_obj.hostname is not None
        assert len(host_obj.groups) == 1
        assert host_obj.groups[0] == "ios"
        assert host_obj.platform == "cisco_ios"
        assert host_obj.username == "pyclass"
        assert host_obj.password == "cisco123"
        assert host_obj.port == 22
        if host_name == "cisco3":
            assert host_obj["dns1"] == "8.8.8.8"

    my_group = nr.inventory.groups["ios"]
    assert my_group.hostname is None
    assert my_group.platform == "cisco_ios"
    assert my_group.port == 22

    defaults = nr.inventory.defaults
    assert defaults.username == "pyclass"
    assert defaults.password == "cisco123"
    assert defaults.data["dns1"] == "1.1.1.1"
    assert defaults.data["dns2"] == "1.0.0.1"

    std_out, std_err, return_code = subprocess_runner(cmd_list, exercise_dir=base_path)
    assert return_code == 0
    assert "cisco3.lasthop.io" in std_out
    assert "cisco4.lasthop.io" in std_out
    assert "8.8.8.8" in std_out
    assert "1.1.1.1" in std_out
    assert "1.0.0.1" in std_out
    assert std_err == ""
