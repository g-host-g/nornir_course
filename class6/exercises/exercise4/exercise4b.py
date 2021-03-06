import os
from nornir import InitNornir
from nornir.core.filter import F
from nornir.plugins.tasks import networking


PASSWORD = os.environ.get("NORNIR_PASSWORD", "bogus")


def log_send_command(task):
    log_file = f"{task.host}_session.log"
    # Obtain the group object using the "refs" attribute
    group = task.host.groups.refs[0]
    group.connection_options["netmiko"].extras["session_log"] = log_file
    task.run(
        task=networking.netmiko_send_command, command_string="show mac address-table"
    )


def main():
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(F(groups__contains="nxos"))
    for hostname, host_obj in nr.inventory.hosts.items():
        host_obj.password = PASSWORD
    nr.run(task=log_send_command)


if __name__ == "__main__":
    main()
